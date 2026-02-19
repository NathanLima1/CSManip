import tkinter as tk
from tkinter import ttk, messagebox as msg, filedialog, scrolledtext
import typing
import os
import threading
import webbrowser
import folium
import sys

from ...data_processing.era5_download import download_and_process_era_data
from ...data_processing.noaa_download import *
from ..tooltip import CreateToolTip

if typing.TYPE_CHECKING:
    from ..start_page import StartPage

class StationChoicePopup(tk.Toplevel):
    """
    Uma janela pop-up modal para o usuário selecionar uma estação de uma lista.
    """
    def __init__(self, parent, controller, stations):
        super().__init__(parent)
        self.controller = controller
        self.stations = stations
        self.chosen_station = None

        self.title(controller.i18n.get('choose_station_title'))
        self.geometry("600x400")
        
        # bloqueia a janela principal
        self.grab_set()
        self.transient(parent)

        i18n = self.controller.i18n

        # UI
        prompt_label = ttk.Label(self, text=controller.i18n.get('choose_station_prompt'), wraplength=580)
        prompt_label.pack(pady=10, padx=10)

        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("name", "id", "enddate"),
            show="headings",
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree.yview)

        # Cabeçalhos
        i18n_name = controller.i18n.get('station_name_header')
        i18n_id = controller.i18n.get('station_id_header')
        i18n_date = controller.i18n.get('station_end_date_header')
        
        self.tree.heading("name", text=i18n_name)
        self.tree.heading("id", text=i18n_id)
        self.tree.heading("enddate", text=i18n_date)
        self.tree.column("name", width=300, anchor="w")
        self.tree.column("id", width=150, anchor="w")
        self.tree.column("enddate", width=100, anchor="center")

        for i, station in enumerate(self.stations):
            self.tree.insert("", "end", iid=i, values=(station['name'], station['id'], station['maxdate']))

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.tree.bind("<Double-1>", self.on_choice)

    def on_choice(self, event=None):
        """Chamado quando o usuário clica duas vezes em um item."""
        try:
            selected_iid = self.tree.selection()[0]
            self.chosen_station = self.stations[int(selected_iid)]
            self.destroy()
        except (IndexError, ValueError):
            pass

class DownloadDataPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        i18n = self.controller.i18n

        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        self.back_button = ttk.Button(top_frame, text="", command=self.go_to_start_page)
        self.back_button.pack(side=tk.LEFT)

        self.page_title = ttk.Label(top_frame, text="", font=("Verdana", 16, "bold"))
        self.page_title.pack(side=tk.LEFT, expand=True)

        main_container = ttk.Frame(self)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        main_container.grid_columnconfigure(0, weight=1, minsize=280) # Painel esquerdo
        main_container.grid_columnconfigure(1, weight=3) # Painel direito
        main_container.grid_rowconfigure(0, weight=1)
        
        # --- PAINEL ESQUERDO ---
        left_panel = ttk.Frame(main_container)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        self.method_label = ttk.Label(left_panel, text="")
        self.method_label.pack(anchor="w", padx=5)
        self.method_combo = ttk.Combobox(left_panel, values=["NOAA", "ECMWF"], state="readonly")
        self.method_combo.pack(fill=tk.X, padx=5, pady=(0, 10))
        self.method_hint = CreateToolTip(self.method_combo, text=i18n.get('download_method_hint'))
        self.method_combo.bind("<<ComboboxSelected>>", self._on_method_selected)

        self.city_label = ttk.Label(left_panel, text="")
        self.city_label.pack(anchor="w", padx=5)
        self.city_entry = ttk.Entry(left_panel)
        self.city_entry.pack(fill=tk.X, padx=5, pady=(0, 10))
        self._add_placeholder(self.city_entry, "City, Country")
        self.city_hint = CreateToolTip(self.city_entry, text=i18n.get('city_download_entry_hint'))

        self.period_frame = ttk.LabelFrame(left_panel, text="")
        self.period_frame.pack(fill=tk.X, padx=5, pady=(0, 10))
        self.period_frame.grid_columnconfigure(0, weight=1)
        self.period_frame.grid_columnconfigure(1, weight=1)

        self.start_label = ttk.Label(self.period_frame, text="")
        self.start_label.grid(row=0, column=0, sticky="w", padx=5)
        self.start_entry = ttk.Entry(self.period_frame)
        self.start_entry.grid(row=1, column=0, sticky="ew", padx=5, pady=(0, 5))
        self._add_placeholder(self.start_entry, "YYYY-MM-DD")
        self.start_hint = CreateToolTip(self.start_entry, text=i18n.get('start_date_download_hint'))

        self.end_label = ttk.Label(self.period_frame, text="")
        self.end_label.grid(row=0, column=1, sticky="w", padx=5)
        self.end_entry = ttk.Entry(self.period_frame)
        self.end_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=(0, 5))
        self._add_placeholder(self.end_entry, "YYYY-MM-DD")
        self.end_hint = CreateToolTip(self.end_entry, text=i18n.get('end_date_download_hint'))

        # --- Frame Condicional para o Radius ---
        self.radius_frame = ttk.Frame(left_panel)

        self.radius_label = ttk.Label(self.radius_frame, text="")
        self.radius_label.pack(anchor="w", padx=5)
        self.radius_entry = ttk.Entry(self.radius_frame)
        self.radius_entry.pack(fill=tk.X, padx=5, pady=(0, 10))
        self.radius_hint = CreateToolTip(self.radius_entry, text=i18n.get('radius_download_hint'))

        self.download_btn = ttk.Button(left_panel, text="", command=self._on_start_download)
        self.download_btn.pack(fill=tk.X, padx=5, pady=20)

        # --- PAINEL DIREITO ---
        self.right_panel = ttk.Frame(main_container, relief="solid", borderwidth=1)
        self.right_panel.grid(row=0, column=1, sticky="nsew")
        
        self.log_label = ttk.Label(self.right_panel, text="", font=("Verdana", 10, "bold"))
        self.log_label.pack(anchor="w", padx=10, pady=(0, 5))
        
        self.log_text = scrolledtext.ScrolledText(self.right_panel, state="disabled", height=10)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        self.update_texts()
        self._on_method_selected(None)

    def _add_placeholder(self, entry, placeholder_text, color='grey'):
        default_fg = 'black'

        def on_focus_in(event):
            if entry.get() == placeholder_text and str(entry.cget('foreground')) == color:
                entry.delete(0, tk.END)
                entry.config(foreground=default_fg)

        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, placeholder_text)
                entry.config(foreground=color)

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

        entry.insert(0, placeholder_text)
        entry.config(foreground=color)

    def _on_method_selected(self, event=None):
        """Chamado quando a combobox de método é alterada."""
        selected_method = self.method_combo.get()
        
        if selected_method == "NOAA":
            self.radius_frame.pack(fill=tk.X, padx=5, pady=(0, 10), before=self.download_btn)
        else:
            self.radius_frame.pack_forget()

    def _log(self, message):
        """Adiciona uma mensagem à caixa de log na UI, de forma segura entre threads."""
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.config(state="disabled")
        self.log_text.see(tk.END)

    def _on_start_download(self):
        """Função chamada pelo botão 'Iniciar download'."""
        #   Coleta os dados e chama sua lógica de download
        method = self.method_combo.get()
        raw_city = self.city_entry.get()
        start = self.start_entry.get()
        end = self.end_entry.get()

        if raw_city == "City, Country":
            city = ""
        else:
            city = raw_city

        if start == "YYYY-MM-DD":
            start = ""
        if end == "YYYY-MM-DD":
            end = ""

        i18n = self.controller.i18n
        
        if not all([method, city, start, end]):
             msg.showwarning(
                 title=i18n.get('missing_fields_title'),
                 message=i18n.get('all_fields_required_msg')
             )
             return

        radius = None
        if method == "NOAA":
            radius_str = self.radius_entry.get()
            if not radius_str:
                self.controller.show_translated_message('warning', 'missing_fields_title', 'radius_required_msg')
                return
            try:
                radius = float(radius_str)
            except ValueError:
                 self.controller.show_translated_message('error', 'value_error_title', 'invalid_radius_msg') # Crie esta chave JSON
                 return
        
        # Limpa o log e desabilita o botão
        self.log_text.config(state="normal")
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state="disabled")
        self.download_btn.config(state="disabled", text=i18n.get('download_in_progress'))
        
        threading.Thread(
            target=self._download_thread_target,
            args=(method, city, start, end, radius),
            daemon=True
        ).start()

    def _run_noaa_download(self, city, start_date, end_date, radius):
        """Lógica específica do NOAA, agora adaptada para a UI."""
        i18n = self.controller.i18n
        required_types = ["TMIN", "TMAX", "PRCP"]
        
        self.after(0, self._log, f"Buscando coordenadas para '{city}'...")
        lat, lon = get_city_coords(city)
        if lat is None or lon is None:
            self.after(0, self.controller.show_translated_message, 'error', 'coords_error_title', 'coords_error_msg', city=city)
            raise Exception("Coordenadas não encontradas.")
        
        self.after(0, self._log, f"Coordenadas encontradas: {lat:.4f}, {lon:.4f}")
        self.after(0, self._log, f"Buscando estações (Raio: {radius})...")

        candidate_stations = find_stations(lat, lon, 50, required_types, radius)
        if not candidate_stations:
            self.after(0, self.controller.show_translated_message, 'warning', 'no_stations_found_title', 'no_stations_found_msg')
            raise Exception("Nenhuma estação candidata encontrada.")

        valid_stations = []
        self.after(0, self._log, "Verificando dados das estações...")
        for station in candidate_stations:
            if check_station_data_types(station['id'], required_types, start_date, end_date):
                valid_stations.append(station)
                self.after(0, self._log, f"  ✔️ Estação válida: {station['name']} ({station['id']})")
            else:
                self.after(0, self._log, f"  ❌ Estação incompleta: {station['name']} ({station['id']})")

        if not valid_stations:
            self.after(0, self.controller.show_translated_message, 'warning', 'no_stations_found_title', 'no_stations_found_msg')
            raise Exception("Nenhuma estação válida encontrada.")

        # Abre o mapa e a janela pop-up
        map_file = self._create_map(valid_stations)
        webbrowser.open('file://' + os.path.realpath(map_file))
        
        popup = StationChoicePopup(self, self.controller, valid_stations)
        self.wait_window(popup) # Pausa esta thread
        
        chosen_station = popup.chosen_station

        if not chosen_station:
            self.after(0, self.controller.show_translated_message, 'info', 'no_station_chosen_title', 'no_station_chosen') # Crie 'no_station_chosen_title'
            raise Exception("Nenhuma estação escolhida.")

        self.after(0, self._log, f"Estação escolhida: '{chosen_station['name']}' ({chosen_station['id']})")
        self.after(0, self._log, "Baixando dados climáticos...")
        
        station_info = {
            'nome': chosen_station['name'], 'id': chosen_station['id'],
            'latitude': chosen_station.get('latitude', lat), 'longitude': chosen_station.get('longitude', lon),
            'elevation': chosen_station.get('elevation', 'N/A'),
            'data_inicial': start_date, 'data_final': end_date
        }
        
        data = get_dly_climate_data_for_station(chosen_station['id'], start_date, end_date, verbose=False) # verbose=False para não poluir log

        if data:
            temp_name = city.split(",")[0].replace(" ", "")
            file_name = f"{temp_name}_{chosen_station['id'].replace(':', '_')}.csv"
            
            # Salva na pasta de dados da aplicação
            base_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
            output_path = os.path.join(base_dir, file_name) # Salva na raiz do projeto
            
            salvar_dados_climaticos_csv(data, output_path, station_info)
            self.after(0, self._log, f"Dados salvos com sucesso em: {output_path}")
        else:
            raise Exception(f"Erro ao baixar os dados da estação: {chosen_station['id']}")

    def _download_thread_target(self, method, city, start, end, radius):
        """A função que roda na thread separada para não congelar a UI."""
        i18n = self.controller.i18n

        base_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
        output_dir = os.path.join(base_dir, "downloaded_data") # Salva tudo numa pasta 'downloaded_data'
        os.makedirs(output_dir, exist_ok=True)

        def gui_logger(message):
            self.after(0, self._log, message)

        try:
            if method == "NOAA":
                self._run_noaa_download(city, start, end, radius)
            else:
                gui_logger("Iniciando download do ECMWF...")

                download_and_process_era_data(
                    city, 
                    start, 
                    end, 
                    output_dir,  # Passa o diretório de saída
                    logger=gui_logger # Passa a nossa função de log
                )
            
            self.after(0, self.download_btn.config, {"state": "normal", "text": i18n.get('start_download_btn')})
            self.after(0, self.controller.show_translated_message, 'info', 'success_title', 'download_complete')

        except Exception as e:
            # Mostra o erro no log e reabilita o botão
            self.after(0, self._log, f"ERRO: {e}")
            self.after(0, self.download_btn.config, {"state": "normal", "text": i18n.get('start_download_btn')})
            self.after(0, self.controller.show_translated_message, 'error', 'download_failed_title', 'download_failed') # Crie 'download_failed_title'

    def _create_map(self, stations):
        """Cria e salva o mapa Folium. Retorna o caminho do arquivo."""
        map_center = [stations[0]['latitude'], stations[0]['longitude']]
        m = folium.Map(location=map_center, zoom_start=10)
        
        for i, station in enumerate(stations):
            station_id_display = i + 1 # Usa o índice + 1 para o ID de escolha
            popup_html = (f"<b>ID de Escolha: {station_id_display} (Use o pop-up)</b><br>"
                          f"Nome: {station['name']}<br>"
                          f"ID Oficial: {station['id']}")
            
            folium.Marker(
                location=[station['latitude'], station['longitude']],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=f"Escolha #{station_id_display}"
            ).add_to(m)
        
        map_file = 'stations_map.html' # Salva na raiz do projeto
        m.save(map_file)
        return map_file

    def go_to_start_page(self):
        """Importa e navega para a página inicial."""
        from ..start_page import StartPage
        self.controller.show_frame(StartPage)
        
    def update_texts(self):
        """Atualiza os textos APENAS para esta tela."""
        i18n = self.controller.i18n
        self.controller.title(i18n.get('app_main_title'))
        self.back_button.config(text=i18n.get('back_btn'))
        self.page_title.config(text=i18n.get('download_data_title'))
        self.method_label.config(text=i18n.get('download_method_label'))
        self.city_label.config(text=i18n.get('city_label'))
        self.period_frame.config(text=i18n.get('time_period_label'))
        self.start_label.config(text=i18n.get('start_label'))
        self.end_label.config(text=i18n.get('end_label'))
        self.radius_label.config(text=i18n.get('radius_label'))
        self.download_btn.config(text=i18n.get('start_download_btn'))
        self.method_hint.text = i18n.get('download_method_hint')
        self.city_hint.text = i18n.get('city_download_entry_hint')
        self.start_hint.text = i18n.get('start_date_download_hint')
        self.end_hint.text = i18n.get('end_date_download_hint')
        self.radius_hint = i18n.get('radius_download_hint')