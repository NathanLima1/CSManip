import tkinter as tk
from tkinter import ttk, messagebox as msg
import typing
import os
from ...data_processing.era5_download import download_and_process_era_data
from ...data_processing.noaa_download import download_noaa_data

if typing.TYPE_CHECKING:
    from ..start_page import StartPage

class DownloadDataPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        # --- Frame Superior ---
        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        self.back_button = ttk.Button(top_frame, text="", command=self.go_to_start_page)
        self.back_button.pack(side=tk.LEFT)

        self.page_title = ttk.Label(top_frame, text="", font=("Verdana", 16, "bold"))
        self.page_title.pack(side=tk.LEFT, expand=True)

        # --- Layout Principal de Duas Colunas ---
        main_container = ttk.Frame(self)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        main_container.grid_columnconfigure(0, weight=1, minsize=280) # Painel esquerdo
        main_container.grid_columnconfigure(1, weight=3) # Painel direito
        main_container.grid_rowconfigure(0, weight=1)
        
        # --- PAINEL ESQUERDO ---
        left_panel = ttk.Frame(main_container)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # --- Método de Download ---
        self.method_label = ttk.Label(left_panel, text="")
        self.method_label.pack(anchor="w", padx=5)
        self.method_combo = ttk.Combobox(left_panel, values=["NOAA", "ECMWF"], state="readonly")
        self.method_combo.pack(fill=tk.X, padx=5, pady=(0, 10))
        # ✨ Vincula o evento de seleção à nossa função de lógica
        self.method_combo.bind("<<ComboboxSelected>>", self._on_method_selected)

        # --- Cidade ---
        self.city_label = ttk.Label(left_panel, text="")
        self.city_label.pack(anchor="w", padx=5)
        self.city_entry = ttk.Entry(left_panel)
        self.city_entry.pack(fill=tk.X, padx=5, pady=(0, 10))

        # --- Período de Tempo ---
        self.period_frame = ttk.LabelFrame(left_panel, text="")
        self.period_frame.pack(fill=tk.X, padx=5, pady=(0, 10))
        # Usa grid dentro deste frame para alinhar Início e Fim
        self.period_frame.grid_columnconfigure(0, weight=1)
        self.period_frame.grid_columnconfigure(1, weight=1)

        self.start_label = ttk.Label(self.period_frame, text="")
        self.start_label.grid(row=0, column=0, sticky="w", padx=5)
        self.start_entry = ttk.Entry(self.period_frame)
        self.start_entry.grid(row=1, column=0, sticky="ew", padx=5, pady=(0, 5))

        self.end_label = ttk.Label(self.period_frame, text="")
        self.end_label.grid(row=0, column=1, sticky="w", padx=5)
        self.end_entry = ttk.Entry(self.period_frame)
        self.end_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=(0, 5))

        # --- Frame Condicional para o Radius ---
        # Este frame conterá os widgets de Radius
        self.radius_frame = ttk.Frame(left_panel)
        # Não usamos .pack() aqui; ele será adicionado/removido dinamicamente

        self.radius_label = ttk.Label(self.radius_frame, text="")
        self.radius_label.pack(anchor="w", padx=5)
        self.radius_entry = ttk.Entry(self.radius_frame)
        self.radius_entry.pack(fill=tk.X, padx=5, pady=(0, 10))

        # --- Botão Iniciar Download ---
        self.download_btn = ttk.Button(left_panel, text="", command=self._on_start_download)
        self.download_btn.pack(fill=tk.X, padx=5, pady=20)

        # --- PAINEL DIREITO ---
        self.right_panel = ttk.Frame(main_container, relief="solid", borderwidth=1)
        self.right_panel.grid(row=0, column=1, sticky="nsew")
        
        # Inicializa os textos
        self.update_texts()
        # Chama a função de lógica uma vez para definir o estado inicial (esconder o raio)
        self._on_method_selected(None)

    def _on_method_selected(self, event=None):
        """Chamado quando a combobox de método é alterada."""
        selected_method = self.method_combo.get()
        
        if selected_method == "NOAA":
            self.radius_frame.pack(fill=tk.X, padx=5, pady=(0, 10), before=self.download_btn)
        else:
            self.radius_frame.pack_forget()

    def _on_start_download(self):
        """Função chamada pelo botão 'Iniciar download'."""
        # Aqui você coleta os dados e chama sua lógica de download
        method = self.method_combo.get()
        city = self.city_entry.get()
        start = self.start_entry.get()
        end = self.end_entry.get()
        
        if not all([method, city, start, end]):
             i18n = self.controller.i18n
             msg.showwarning(
                 title=i18n.get('missing_fields_title'),
                 message=i18n.get('all_fields_required_msg')
             )
             return

        radius = None
        if method == "NOAA":
            radius = self.radius_entry.get()
            if not radius:
                i18n = self.controller.i18n
                msg.showwarning(
                     title=i18n.get('missing_fields_title'),
                     message=i18n.get('radius_required_msg')
                 )
                return
            download_noaa_data(city, start, end, radius)
        else:
            download_and_process_era_data(city, start, end)

        # (Insira sua lógica de download aqui)
        print(f"Iniciando download com: Método={method}, Cidade={city}, Início={start}, Fim={end}, Raio={radius}")


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
        
        # Atualiza os novos widgets
        self.method_label.config(text=i18n.get('download_method_label'))
        self.city_label.config(text=i18n.get('city_label'))
        self.period_frame.config(text=i18n.get('time_period_label'))
        self.start_label.config(text=i18n.get('start_label'))
        self.end_label.config(text=i18n.get('end_label'))
        self.radius_label.config(text=i18n.get('radius_label'))
        self.download_btn.config(text=i18n.get('start_download_btn'))