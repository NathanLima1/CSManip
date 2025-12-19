import tkinter as tk
import threading

from ..tooltip import CreateToolTip

from ..utils import *
if typing.TYPE_CHECKING:
    from ..start_page import StartPage
    from .view_data_page import ViewDataPage
    from .imputation_techniques_page import ImputationTechniquesPage

class DataImputationPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        i18n = self.controller.i18n

        self.city_path_list = []
        self.loading = False     

        # --- Widgets ---
        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        self.back_button = ttk.Button(top_frame, text="", command=self.go_to_start_page)
        self.back_button.pack(side=tk.LEFT)

        self.page_title = ttk.Label(top_frame, text="", font=("Verdana", 16, "bold"))
        self.page_title.pack(side=tk.LEFT, expand=True)

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

        self.label_combo1 = ttk.Label(combobox_grid, text="")
        self.combo1 = ttk.Combobox(combobox_grid, state="readonly")
        self.label_combo1.grid(row=0, column=0, sticky="w", padx=5)
        self.combo1.grid(row=1, column=0, padx=5, pady=5)
        self.combo1_hint = CreateToolTip(self.combo1, text=i18n.get('alvo_data_hint'))

        self.label_combo2 = ttk.Label(combobox_grid, text="")
        self.combo2 = ttk.Combobox(combobox_grid, state="readonly")
        self.label_combo2.grid(row=0, column=1, sticky="w", padx=5)
        self.combo2.grid(row=1, column=1, padx=5, pady=5)
        self.combo2_hint = CreateToolTip(self.combo2, text=i18n.get('viz1_data_hint'))

        self.label_combo3 = ttk.Label(combobox_grid, text="")
        self.combo3 = ttk.Combobox(combobox_grid, state="readonly")
        self.label_combo3.grid(row=2, column=0, sticky="w", padx=5)
        self.combo3.grid(row=3, column=0, padx=5, pady=5)
        self.combo3_hint = CreateToolTip(self.combo3, text=i18n.get('viz2_data_hint'))

        self.label_combo4 = ttk.Label(combobox_grid, text="")
        self.combo4 = ttk.Combobox(combobox_grid, state="readonly")
        self.label_combo4.grid(row=2, column=1, sticky="w", padx=5)
        self.combo4.grid(row=3, column=1, padx=5, pady=5)
        self.combo4_hint = CreateToolTip(self.combo4, text=i18n.get('viz3_data_hint'))
        
        # --- Botões de Ações ---
        self.select_data_btn = ttk.Button(self.select_data_frame, text="Selecionar Pasta de Dados", command=self.list_cities)
        self.select_data_btn.pack(pady=(10, 5))
        self.select_data_hint = CreateToolTip(self.select_data_btn, text=i18n.get('select_dir_data_hint'))

        self.confirm_group_btn = ttk.Button(self.select_data_frame, text="", command=self.on_click)
        self.confirm_group_btn.pack(pady=(5, 10))
        self.confirm_group_hint = CreateToolTip(self.confirm_group_btn, text=i18n.get('confirm_group_data_hint'))

        self.visualize_data_btn = ttk.Button(left_panel, text="", command=self.go_to_view_data)
        self.visualize_data_btn.pack(fill=tk.X, pady=5)
        self.visualize_data_hint = CreateToolTip(self.visualize_data_btn, text=i18n.get('visualize_data_hint'))

        self.imputation_tech_btn = ttk.Button(left_panel, text="", command=self.go_to_imputation_techiniques)
        self.imputation_tech_btn.pack(fill=tk.X, pady=5)
        self.imputation_tech_hint = CreateToolTip(self.imputation_tech_btn, text=i18n.get('imputation_data_hint'))
        
        triang = Triangulation()
        self.show_location_btn = ttk.Button(left_panel, text="", command=triang.show_map)
        self.show_location_btn.pack(fill=tk.X, pady=5)
        self.show_location_hint = CreateToolTip(self.show_location_btn, text=i18n.get('show_location_data_hint'))

        right_panel = ttk.Frame(main_container, relief="solid", borderwidth=1)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        
        self.autofill_combos_from_coordinates()
        self.update_texts()

    def reset_city_combos(self):
        combos = [self.combo1, self.combo2, self.combo3, self.combo4]

        for combo in combos:
            combo.set('')        
            combo['values'] = [] 

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
    
    def load_cities_from_coordinates(self, filename="Coordinates.txt"):
        if not os.path.exists(filename):
            return []

        cities = []

        try:
            with open(filename, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]

            for i in range(0, len(lines), 4):
                city_name = lines[i]
                cities.append(city_name)

        except Exception as e:
            print(f"Erro ao ler {filename}: {e}")
            return []

        return cities
    
    def autofill_combos_from_coordinates(self):
        cities = self.load_cities_from_coordinates()

        if len(cities) < 4:
            return 

        self.combo1['values'] = cities
        self.combo2['values'] = cities
        self.combo3['values'] = cities
        self.combo4['values'] = cities

        self.combo1.set(cities[0])  
        self.combo2.set(cities[1])  
        self.combo3.set(cities[2]) 
        self.combo4.set(cities[3]) 

    def list_cities(self):
        self.reset_city_combos()
        db_location = dlg.askdirectory()
        if not db_location:
            return

        file_name_list = os.listdir(db_location)
        file_path_list = [f"{db_location}/{file_name}" for file_name in file_name_list]

        all_city_names = []
        self.city_path_list.clear()

        for file_path in file_path_list:
            try:
                name, lat, lon, alt, address = self.get_info(file_path)
                all_city_names.append(name)
                self.city_path_list.append([name, address])
            except (IOError, IndexError, ValueError) as e:
                print(f"Erro ao processar o arquivo {file_path}: {e}")
                continue

        all_city_names.sort()

        self.combo1['values'] = all_city_names
        self.combo2['values'] = all_city_names
        self.combo3['values'] = all_city_names
        self.combo4['values'] = all_city_names
        self.controller.show_translated_message(
            msg_type='info',
            title_key='success_title',
            message_key='cities_loaded_msg',
            all_city_names=len(all_city_names)
            )

    def on_click(self):
        self.confirm_group_btn.config(command=())
        self.loading = True
        self.loading_step = 0
        self.animate_loading()
        threading.Thread(target=self.run_process).start()

    def animate_loading(self):
        if self.loading:
            dots = '.' * (self.loading_step % 4)
            i18n = self.controller.i18n
            loading_text = i18n.get('loading_text', default="Carregando")
            self.confirm_group_btn.config(text=f"{loading_text}{dots}")
            self.loading_step += 1
            self.after(500, self.animate_loading)

    def run_process(self):
        self.process_selection()
        self.after(0, self.reset_button)

    def reset_button(self):
        self.loading = False
        i18n = self.controller.i18n
        self.confirm_group_btn.config(text=i18n.get('confirm_group_btn'), command=self.on_click)

    def process_selection(self):
        target_city_name = self.combo1.get()
        neighbor_a_name = self.combo2.get()
        neighbor_b_name = self.combo3.get()
        neighbor_c_name = self.combo4.get()

        if not all([target_city_name, neighbor_a_name, neighbor_b_name, neighbor_c_name]):
            self.controller.show_translated_message(
            msg_type='error',
            title_key='incomplete_data_title',
            message_key='cities_not_selected_msg',
            )
            return

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
                self.controller.show_translated_message(
                    msg_type='error',
                    title_key='error_title',
                    message_key='path_not_found_msg',
                    name_to_find=name_to_find
                    )
                return

        data_processor = DataProcessing()
        data_processor.target = paths["target"]
        data_processor.neighborA = paths["neighborA"]
        data_processor.neighborB = paths["neighborB"]
        data_processor.neighborC = paths["neighborC"]
        data_processor.download_path = os.getcwd()

        data_processor.get_processed_data()
        self.controller.show_translated_message(
            msg_type='info',
            title_key='succes_title',
            message_key='files_selected_msg'
            )
        
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
        self.combo1_hint.text = i18n.get('alvo_data_hint')
        self.combo2_hint.text = i18n.get('viz1_data_hint')
        self.combo3_hint.text = i18n.get('viz2_data_hint')
        self.combo4_hint.text = i18n.get('viz3_data_hint')
        self.select_data_hint.text = i18n.get('select_dir_data_hint')
        self.confirm_group_hint.text = i18n.get('confirm_group_data_hint')
        self.visualize_data_hint.text = i18n.get('visualize_data_hint')
        self.imputation_tech_hint.text = i18n.get('imputation_data_hint')
        self.show_location_hint.text = i18n.get('show_location_data_hint')
