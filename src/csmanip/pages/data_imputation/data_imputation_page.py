# Importações necessárias no topo do seu arquivo
import tkinter as tk
import threading

# Supondo que essas importações estejam corretas para a sua estrutura de projeto
from ..utils import *
if typing.TYPE_CHECKING:
    from ..start_page import StartPage
    from .view_data_page import ViewDataPage
    from .imputation_techniques_page import ImputationTechniquesPage

class DataImputationPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        # --- Atributos para a lógica ---
        self.city_path_list = [] # Vai guardar [nome_cidade, caminho_arquivo]
        self.loading = False     # Flag para a animação do botão

        # --- Widgets ---
        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        self.back_button = ttk.Button(top_frame, text="", command=self.go_to_start_page)
        self.back_button.pack(side=tk.LEFT)

        self.page_title = ttk.Label(top_frame, text="", font=("Verdana", 16, "bold"))
        self.page_title.pack(side=tk.LEFT, expand=True)

        # Layout principal de duas colunas
        main_container = ttk.Frame(self)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=3)
        main_container.grid_rowconfigure(0, weight=1)
        
        left_panel = ttk.Frame(main_container, relief="groove", borderwidth=2)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        # --- Selecionar dados ---
        self.select_data_frame = ttk.LabelFrame(left_panel, text="")
        self.select_data_frame.pack(fill=tk.X, pady=(0, 20))

        combobox_grid = ttk.Frame(self.select_data_frame)
        combobox_grid.pack(pady=10, padx=10)

        # Labels e Comboboxes criados aqui, e serão apenas atualizados depois
        self.label_combo1 = ttk.Label(combobox_grid, text="")
        self.combo1 = ttk.Combobox(combobox_grid, state="readonly")
        self.label_combo1.grid(row=0, column=0, sticky="w", padx=5)
        self.combo1.grid(row=1, column=0, padx=5, pady=5)

        self.label_combo2 = ttk.Label(combobox_grid, text="")
        self.combo2 = ttk.Combobox(combobox_grid, state="readonly")
        self.label_combo2.grid(row=0, column=1, sticky="w", padx=5)
        self.combo2.grid(row=1, column=1, padx=5, pady=5)

        self.label_combo3 = ttk.Label(combobox_grid, text="")
        self.combo3 = ttk.Combobox(combobox_grid, state="readonly")
        self.label_combo3.grid(row=2, column=0, sticky="w", padx=5)
        self.combo3.grid(row=3, column=0, padx=5, pady=5)

        self.label_combo4 = ttk.Label(combobox_grid, text="")
        self.combo4 = ttk.Combobox(combobox_grid, state="readonly")
        self.label_combo4.grid(row=2, column=1, sticky="w", padx=5)
        self.combo4.grid(row=3, column=1, padx=5, pady=5)
        
        # --- Botões de Ações ---
        # Botão para selecionar os dados (pasta com .csv)
        self.select_data_btn = ttk.Button(self.select_data_frame, text="Selecionar Pasta de Dados", command=self.list_cities)
        self.select_data_btn.pack(pady=(10, 5))

        # Botão para confirmar o grupo, agora com a animação
        self.confirm_group_btn = ttk.Button(self.select_data_frame, text="", command=self.on_click)
        self.confirm_group_btn.pack(pady=(5, 10))

        # Botões de navegação
        self.visualize_data_btn = ttk.Button(left_panel, text="", command=self.go_to_view_data)
        self.visualize_data_btn.pack(fill=tk.X, pady=5)

        self.imputation_tech_btn = ttk.Button(left_panel, text="", command=self.go_to_imputation_techiniques)
        self.imputation_tech_btn.pack(fill=tk.X, pady=5)
        
        triang = Triangulation()
        self.show_location_btn = ttk.Button(left_panel, text="", command=triang.show_map)
        self.show_location_btn.pack(fill=tk.X, pady=5)

        right_panel = ttk.Frame(main_container, relief="solid", borderwidth=1)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        
        self.update_texts()

    def go_to_start_page(self):
        """Importa e navega para a página inicial."""
        from ..start_page import StartPage
        self.controller.show_frame(StartPage)

    def go_to_imputation_techiniques(self):
        """Importa e navega para a página de tecnicas imputação de dados."""
        from .imputation_techniques_page import ImputationTechniquesPage
        self.controller.show_frame(ImputationTechniquesPage)

    def go_to_view_data(self):
        """Importa e navega para a página de visualização dos dados."""
        from .view_data_page import ViewDataPage
        self.controller.show_frame(ViewDataPage)

    def get_info(self, directory):
        # Esta função está ótima, não precisa de mudanças.
        raw_data = []
        with open(directory, 'r') as file:
            for line in file:
                raw_data.append(line.replace('\n', ''))
        if raw_data:
            del raw_data[-1]
        name = raw_data[0][6:]
        latitude = float(raw_data[2][10:])
        longitude = float(raw_data[3][10:])
        altitude = float(raw_data[4][10:])
        return name, latitude, longitude, altitude, directory

    def list_cities(self):
        # MUDANÇA: Esta função agora APENAS busca os dados e ATUALIZA os comboboxes existentes.
        db_location = dlg.askdirectory()
        if not db_location: # Se o usuário cancelar a seleção da pasta
            return

        file_name_list = os.listdir(db_location)
        file_path_list = [f"{db_location}/{file_name}" for file_name in file_name_list]

        all_city_names = []
        self.city_path_list.clear() # Limpa a lista anterior

        for file_path in file_path_list:
            try:
                name, lat, lon, alt, address = self.get_info(file_path)
                all_city_names.append(name)
                self.city_path_list.append([name, address])
            except (IOError, IndexError, ValueError) as e:
                print(f"Erro ao processar o arquivo {file_path}: {e}")
                continue # Pula para o próximo arquivo se houver erro

        all_city_names.sort()

        # MUDANÇA: Atualiza os valores dos comboboxes criados no __init__
        self.combo1['values'] = all_city_names
        self.combo2['values'] = all_city_names
        self.combo3['values'] = all_city_names
        self.combo4['values'] = all_city_names
        msg.showinfo("Sucesso", f"{len(all_city_names)} cidades carregadas com sucesso!")

    # --- Lógica de Animação (Adaptada) ---
    def on_click(self):
        # MUDANÇA: Agora opera no self.confirm_group_btn
        self.confirm_group_btn.config(command=()) # Desabilita o botão temporariamente
        self.loading = True
        self.loading_step = 0
        self.animate_loading()
        threading.Thread(target=self.run_process).start()

    def animate_loading(self):
        if self.loading:
            dots = '.' * (self.loading_step % 4)
            # MUDANÇA: Atualiza o texto do botão correto
            i18n = self.controller.i18n
            loading_text = i18n.get('loading_text', default="Carregando") # Adicionar "loading_text" ao JSON
            self.confirm_group_btn.config(text=f"{loading_text}{dots}")
            self.loading_step += 1
            self.after(500, self.animate_loading)

    def run_process(self):
        self.process_selection()
        # Garante que a atualização da UI ocorra na thread principal
        self.after(0, self.reset_button)

    def reset_button(self):
        self.loading = False
        i18n = self.controller.i18n
        # MUDANÇA: Reseta o botão correto
        self.confirm_group_btn.config(text=i18n.get('confirm_group_btn'), command=self.on_click)

    def process_selection(self):
        # MUDANÇA: Obtém os valores diretamente dos comboboxes existentes
        target_city_name = self.combo1.get()
        neighbor_a_name = self.combo2.get()
        neighbor_b_name = self.combo3.get()
        neighbor_c_name = self.combo4.get()

        if not all([target_city_name, neighbor_a_name, neighbor_b_name, neighbor_c_name]):
            msg.showerror(title='Dados Incompletos', message="Alguma(s) cidade(s) não foi(ram) selecionada(s)")
            return

        # A lógica para encontrar os caminhos permanece a mesma
        paths = {}
        names_to_find = {
            "target": target_city_name, 
            "neighborA": neighbor_a_name, 
            "neighborB": neighbor_b_name, 
            "neighborC": neighbor_c_name
        }

        for key, name_to_find in names_to_find.items():
            found = False
            for city_name, path in self.city_path_list:
                if city_name == name_to_find:
                    paths[key] = path
                    found = True
                    break
            if not found:
                msg.showerror("Erro", f"Caminho não encontrado para a cidade: {name_to_find}")
                return

        data_processor = DataProcessing()
        data_processor.target = paths["target"]
        data_processor.neighborA = paths["neighborA"]
        data_processor.neighborB = paths["neighborB"]
        data_processor.neighborC = paths["neighborC"]
        data_processor.download_path = os.getcwd()

        data_processor.get_processed_data()
        msg.showinfo(title="Sucesso!", message="Arquivos selecionados com sucesso!")
        
    def update_texts(self):
        i18n = self.controller.i18n
        self.controller.title(i18n.get('app_main_title'))
        self.back_button.config(text=i18n.get('back_btn'))
        self.page_title.config(text=i18n.get('data_imputation_title'))
        self.select_data_frame.config(text=i18n.get('select_data_label'))
        self.confirm_group_btn.config(text=i18n.get('confirm_group_btn'))
        self.visualize_data_btn.config(text=i18n.get('visualize_data_btn'))
        self.imputation_tech_btn.config(text=i18n.get('imputation_techniques_btn'))
        self.show_location_btn.config(text=i18n.get('show_location_btn')) # Corrigido para uma chave genérica
        self.label_combo1.config(text=i18n.get('target_label'))
        self.label_combo2.config(text=i18n.get('neighbor1_label'))
        self.label_combo3.config(text=i18n.get('neighbor2_label'))
        self.label_combo4.config(text=i18n.get('neighbor3_label'))