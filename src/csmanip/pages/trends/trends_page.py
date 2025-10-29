import tkinter as tk
from tkinter import ttk, filedialog, messagebox as msg
import os
import typing

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from ..utils import *
if typing.TYPE_CHECKING:
    from ..start_page import StartPage
from ...trends.plot_warming_stripes import plot_annual_data, plot_monthly_data, plot_quarterly_data
from ...trends.processing import process_csv
from ...trends.group_data import group_data
from ...trends.climdex import Climdex

class ClimateTrendsPage(ttk.Frame):
    """Tela para análise de tendências climáticas."""
    def __init__(self, parent, controller):
        self.city_name = None
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        self.processed_file_name = None
        self.output_dir = None
        self.city_name_raw = None

        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        self.back_button = ttk.Button(top_frame, text="", command=self.go_to_start_page)
        self.back_button.pack(side=tk.LEFT)

        self.page_title = ttk.Label(top_frame, text="", font=("Verdana", 16, "bold"))
        self.page_title.pack(side=tk.LEFT, expand=True)

        # --- Layout Principal de Duas Colunas ---
        main_container = ttk.Frame(self)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        main_container.grid_columnconfigure(0, weight=1, minsize=280)
        main_container.grid_columnconfigure(1, weight=3)
        main_container.grid_rowconfigure(0, weight=1)
        
        # --- PAINEL DA ESQUERDA ---
        left_panel = ttk.Frame(main_container)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Seção de Processamento de Arquivo
        self.processed_file_label = ttk.Label(left_panel, text="")
        self.processed_file_label.pack(anchor="w", padx=5)

        self.processed_file_entry = ttk.Entry(left_panel, state="readonly")
        self.processed_file_entry.pack(fill=tk.X, padx=5, pady=(0, 5))

        self.select_process_btn = ttk.Button(left_panel, text="", command=self.choose_and_process_file)
        self.select_process_btn.pack(fill=tk.X, padx=5, pady=5)

        self.climatic_extremes_btn = ttk.Button(left_panel, text="", command=self.calculate_extreme_indicators)
        self.climatic_extremes_btn.pack(fill=tk.X, padx=5, pady=5) # Mais espaço abaixo

        self.analyze_trend_btn = ttk.Button(left_panel, text="")
        self.analyze_trend_btn.pack(fill=tk.X, padx=5, pady=(5, 20))

        # Seção de Plotagem de Trends
        self.plot_trends_frame = ttk.LabelFrame(left_panel, text="")
        self.plot_trends_frame.pack(fill=tk.X, padx=5)

        self.parameter_combo = ttk.Combobox(self.plot_trends_frame, state="readonly", values= ["Maximum temperature", "Minimum temperature", "Precipitation"])
        self.parameter_combo.pack(fill=tk.X, padx=5, pady=5)

        self.monthly_btn = ttk.Button(self.plot_trends_frame, text="", command=self.plot_monthly)
        self.monthly_btn.pack(fill=tk.X, expand=True, pady=5, padx=5)

        self.quarterly_btn = ttk.Button(self.plot_trends_frame, text="", command=self.plot_quarterly)
        self.quarterly_btn.pack(fill=tk.X, expand=True, pady=5, padx=5)
        
        self.annual_btn = ttk.Button(self.plot_trends_frame, text="", command=self.plot_annual)
        self.annual_btn.pack(fill=tk.X, expand=True, pady=5, padx=5)

        # --- PAINEL DA DIREITA ---
        self.right_panel = ttk.Frame(main_container, relief="solid", borderwidth=1)
        self.right_panel.grid(row=0, column=1, sticky="nsew")
        
        self.update_texts()

    def choose_and_process_file(self):
        print("choose and process file")
        """Abre o diálogo, processa o arquivo e atualiza a UI."""
        caminho_completo = filedialog.askopenfilename(
            title="Selecione o arquivo CSV de dados brutos",
            filetypes=[("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")]
        )

        if not caminho_completo:
            print("Nenhum arquivo selecionado.")
            return

        self.city_name_raw = os.path.basename(caminho_completo)
        print("city", self.city_name_raw)
        
        input_dir = os.path.dirname(caminho_completo)
        
        base_dir = os.path.dirname(os.path.dirname(__file__))
        self.output_dir = os.path.join(base_dir, "processed_data")
        os.makedirs(self.output_dir, exist_ok=True)
        self.city = []
        self.city.append(self.city_name_raw)


        print(f"Arquivo de entrada: {self.city_name_raw}")
        print(f"Pasta de saída: {self.output_dir}")

        try:
            process_csv(self.city, input_dir, self.output_dir)
            self.processed_file_name = f"processed_{self.city_name_raw}"

            self.processed_file_entry.config(state="normal")
            self.processed_file_entry.delete(0, tk.END)
            self.processed_file_entry.insert(0, self.processed_file_name)
            self.processed_file_entry.config(state="readonly")
            
            msg.showinfo("Sucesso", "Arquivo processado e salvo na pasta 'processed_data'.")
        except Exception as e:
            msg.showerror("Erro de Processamento", f"Ocorreu um erro ao processar o arquivo:\n{e}")

    def calculate_extreme_indicators(self):
        """Calcula e mostra os indicadores climáticos."""
        print("calculate extreme indicators")
        if not self.processed_file_name:
            msg.showwarning("Aviso", "Por favor, selecione e processe um arquivo primeiro.")
            return
        
        c = Climdex()
        data = c.read_files_climdex(self.output_dir, self.city)
        city_name = self.city.split('.')
        city_name = city_name[0]
        self.city_name = city_name

        df_city = data[self.city]

        indices = c.calculate_indices(df_city, (self.start_date, self.end_date))
        c.write_indices(indices, self.city_name, self.output_dir)

        pdf_output_path = f"{self.output_dir}/graphs_indices_{city_name}.pdf"
        c.plot_and_save_indices(indices, self.city_name, self.output_dir)

    def _plot_graph_on_panel(self, fig):
        print("plot graph on panel")
        """Limpa o painel direito e desenha uma nova figura matplotlib nele."""
        for widget in self.right_panel.winfo_children():
            widget.destroy()

        if fig is None:
            return

        canvas = FigureCanvasTkAgg(fig, master=self.right_panel)
        canvas.draw()

        toolbar = NavigationToolbar2Tk(canvas, self.right_panel)
        toolbar.update()
        
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)

    def get_parameter(self, temperature_parameter):
        print("get parameter")
        if temperature_parameter == "Maximum temperature":
            parameter = "tmax"
        elif temperature_parameter == "Minimum temperature":
            parameter = "tmin"
        else:
            parameter = "tmean"
        return parameter
    
    def plot_monthly(self):
        print("Entrou entrou plot_monthly")
        city_name = self.city[0].split('.')
        city_name = city_name[0]
        self.city_name = city_name

        group_data(self.city, self.output_dir, self.output_dir)
        
        temperature_parameter = self.parameter_combo.get()
        parameter_abreviation = self.get_parameter(temperature_parameter)
        
        fig = plot_monthly_data(
            csv_path=f'{self.output_dir}/{self.city_name}DadosMensais.csv',
            index=parameter_abreviation,  # Coluna a ser plotada ('tmax', 'tmin', 'tmean', 'prec')
            file_name=f'tendencia_mensal_{parameter_abreviation}_{self.city_name}.png',
            title_img=f'Tendência da {temperature_parameter} Mensal em {self.city_name}',
            caption_img='',
            embed_mode=True
        )

        self._plot_graph_on_panel(fig)
    
    def plot_quarterly(self):
        city_name = self.city[0].split('.')
        city_name = city_name[0]
        self.city_name = city_name

        group_data(self.city, self.output_dir, self.output_dir)
        
        temperature_parameter = self.parameter_combo.get()
        parameter_abreviation = self.get_parameter(temperature_parameter)
        
        fig = plot_quarterly_data(
            csv_path=f'{self.output_dir}/{self.city_name}dadosTrimestrais.csv',
            index=parameter_abreviation,  # Coluna a ser plotada ('tmax', 'tmin', 'tmean', 'prec')
            file_name=f'tendencia_trimestral_{parameter_abreviation}_{self.city_name}.png',
            title_img=f'Tendência da {temperature_parameter} Trimestral em {self.city_name}',
            caption_img='',
            embed_mode=True
        )

        self._plot_graph_on_panel(fig)

    def plot_annual(self):
        city_name = self.city[0].split('.')
        city_name = city_name[0]
        self.city_name = city_name

        group_data(self.city, self.output_dir, self.output_dir)

        temperature_parameter = self.parameter_combo.get()
        parameter_abreviation = self.get_parameter(temperature_parameter)
        
        fig = plot_annual_data(
            csv_path=f'{self.output_dir}/{self.city_name}dadosAnuais.csv',
            index=parameter_abreviation,  # Coluna a ser plotada ('tmax', 'tmin', 'tmean', 'prec')
            file_name=f'tendencia_anual_{parameter_abreviation}_{self.city_name}.png',
            title_img=f'Tendência da {temperature_parameter} Anual em {self.city_name}',
            caption_img='',
            embed_mode=True
        )
        self._plot_graph_on_panel(fig)
    
    def go_to_start_page(self):
        from ..start_page import StartPage
        self.controller.show_frame(StartPage)
        
    def update_texts(self):
        i18n = self.controller.i18n
        self.back_button.config(text=i18n.get('back_btn'))
        self.page_title.config(text=i18n.get('climate_trends_page_title'))
        self.processed_file_label.config(text=i18n.get('processed_file_label'))
        self.select_process_btn.config(text=i18n.get('select_and_process_btn'))
        self.climatic_extremes_btn.config(text=i18n.get('climatic_extremes_btn'))
        self.analyze_trend_btn.config(text=i18n.get('analyse_trend_btn'))
        self.plot_trends_frame.config(text=i18n.get('plot_trends_label'))
        self.monthly_btn.config(text=i18n.get('monthly_btn'))
        self.quarterly_btn.config(text=i18n.get('quarterly_btn'))
        self.annual_btn.config(text=i18n.get('annual_btn'))