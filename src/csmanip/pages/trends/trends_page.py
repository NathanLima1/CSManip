import tkinter as tk
from tkinter import ttk, filedialog, messagebox as msg
import os
import typing
import sys
import subprocess
from datetime import datetime

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from ..utils import *
if typing.TYPE_CHECKING:
    from ..start_page import StartPage
from ...trends.plot_warming_stripes import plot_annual_data, plot_monthly_data, plot_quarterly_data
from ...trends.processing import process_csv
from ...trends.group_data import group_data
from ...trends.identify_trends import analyze_trend
from ...trends.climdex import Climdex
from ..tooltip import CreateToolTip

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
        self.processed_file_hint = CreateToolTip(self.processed_file_entry, text='')

        self.select_process_btn = ttk.Button(left_panel, text="", command=self.choose_and_process_file)
        self.select_process_btn.pack(fill=tk.X, padx=5, pady=5)
        self.select_process_hint = CreateToolTip(self.select_process_btn, text='')

        self.extremes_frame = ttk.LabelFrame(left_panel, text="")
        self.extremes_frame.pack(fill=tk.X, padx=5, pady=(10, 5))
        
        # Frame interno para os combos
        date_frame = ttk.Frame(self.extremes_frame)
        date_frame.pack(fill=tk.X, padx=5, pady=5)
        date_frame.grid_columnconfigure(0, weight=1)
        date_frame.grid_columnconfigure(1, weight=1)

        self.start_year_label = ttk.Label(date_frame, text="")
        self.start_year_label.grid(row=0, column=0, sticky="w")
        self.start_year_combo = ttk.Combobox(date_frame, state="disabled")
        self.start_year_combo.grid(row=1, column=0, sticky="ew", padx=(0, 5))
        self.start_hint = CreateToolTip(self.start_year_combo, text='')

        self.end_year_label = ttk.Label(date_frame, text="")
        self.end_year_label.grid(row=0, column=1, sticky="w")
        self.end_year_combo = ttk.Combobox(date_frame, state="disabled")
        self.end_year_combo.grid(row=1, column=1, sticky="ew", padx=(5, 0))
        self.end_hint = CreateToolTip(self.end_year_combo, text='')

        self.climatic_extremes_btn = ttk.Button(left_panel, text="", command=self.calculate_extreme_indicators)
        self.climatic_extremes_btn.pack(fill=tk.X, padx=5, pady=5)
        self.climatic_extremes_hint = CreateToolTip(self.climatic_extremes_btn, text='')

        self.analyze_trend_frame = ttk.LabelFrame(left_panel, text="")
        self.analyze_trend_frame.pack(fill=tk.X, padx=5, pady=(10, 5))

        self.trend_param_label = ttk.Label(self.analyze_trend_frame, text="")
        self.trend_param_label.pack(anchor="w", padx=5)
        
        self.trend_param_combo = ttk.Combobox(self.analyze_trend_frame, state="readonly", values=["Maximum temperature", "Minimum temperature", "Precipitation", "Mean temperature"])
        self.trend_param_combo.pack(fill=tk.X, padx=5, pady=5)
        self.analyze_trend_param_hint = CreateToolTip(self.trend_param_combo, text=''
                                                )
        self.analyze_trend_btn = ttk.Button(self.analyze_trend_frame, text="", command=self.run_trend_analysis)
        self.analyze_trend_btn.pack(fill=tk.X, padx=5, pady=(5, 10))
        self.analyze_trend_hint = CreateToolTip(self.analyze_trend_btn, text='')

        # Seção de Plotagem de Trends
        self.plot_trends_frame = ttk.LabelFrame(left_panel, text="")
        self.plot_trends_frame.pack(fill=tk.X, padx=5)

        self.plot_param_label = ttk.Label(self.plot_trends_frame, text="")
        self.plot_param_label.pack(anchor="w", padx=5)
        
        self.plot_param_combo = ttk.Combobox(self.plot_trends_frame, state="readonly", values= ["Maximum temperature", "Minimum temperature", "Precipitation", "Mean temperature"])
        self.plot_param_combo.pack(fill=tk.X, padx=5, pady=5)
        self.plot_param_hint = CreateToolTip(self.plot_param_combo, text='')

        self.monthly_btn = ttk.Button(self.plot_trends_frame, text="", command=self.plot_monthly)
        self.monthly_btn.pack(fill=tk.X, expand=True, pady=5, padx=5)
        self.quarterly_btn = ttk.Button(self.plot_trends_frame, text="", command=self.plot_quarterly)
        self.quarterly_btn.pack(fill=tk.X, expand=True, pady=5, padx=5)
        self.annual_btn = ttk.Button(self.plot_trends_frame, text="", command=self.plot_annual)
        self.annual_btn.pack(fill=tk.X, expand=True, pady=5, padx=5)
        self.monthly_hint = CreateToolTip(self.monthly_btn, text='')
        self.quarterly_hint = CreateToolTip(self.quarterly_btn, text='')
        self.annual_hint = CreateToolTip(self.annual_btn, text='')

        # --- PAINEL DA DIREITA ---
        self.right_panel = ttk.Frame(main_container, relief="solid", borderwidth=1)
        self.right_panel.grid(row=0, column=1, sticky="nsew")
        
        self.update_texts()

    def _clear_panel(self, panel):
        """Limpa todos os widgets de um painel."""
        for widget in panel.winfo_children():
            widget.destroy()

    def _get_years_from_file(self, file_path):
        """Lê o arquivo processado e retorna uma lista de anos únicos."""
        available_years = set()
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    if not line.strip(): continue
                    parts = line.split(',')
                    if parts[0].isdigit():
                        available_years.add(int(parts[0]))
        except FileNotFoundError:
            self.controller.show_translated_message(
                'error', 'folder_not_found_title', 'folder_not_found_msg', directory=file_path
            )
            return []
        except Exception as e:
            self.controller.show_translated_message(
                'error', 'years_load_error_title', 'years_load_error_msg', error=str(e)
            )
            return []
        
        if not available_years:
            return []
            
        sorted_years = sorted(list(available_years))
        return [str(year) for year in sorted_years]

    def choose_and_process_file(self):
        print("choose and process file")
        """Abre o diálogo, processa o arquivo e atualiza a UI."""
        caminho_completo = filedialog.askopenfilename(
            parent=self,
            title="Selecione o arquivo CSV de dados brutos",
            filetypes=[("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")]
        )

        if not caminho_completo: return

        self.city_name_raw = os.path.basename(caminho_completo)
        
        city_name_only = self.city_name_raw.split('.')[0]
        self.city_name = city_name_only
        
        self.city_name_raw = os.path.basename(caminho_completo)
        input_dir = os.path.dirname(caminho_completo)
        base_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
        self.output_dir = os.path.join(base_dir, "output_dir")
        os.makedirs(self.output_dir, exist_ok=True)
        self.city = [self.city_name_raw]

        try:
            process_csv(self.city, input_dir, self.output_dir)
            self.processed_file_name = f"{self.city_name_raw}"

            self.processed_file_entry.config(state="normal")
            self.processed_file_entry.delete(0, tk.END)
            self.processed_file_entry.insert(0, self.processed_file_name)
            self.processed_file_entry.config(state="readonly")
            
            processed_path = os.path.join(self.output_dir, self.processed_file_name)
            years_list = self._get_years_from_file(processed_path)
            
            if years_list:
                self.start_year_combo.config(values=years_list, state="readonly")
                self.end_year_combo.config(values=years_list, state="readonly")
                # Define valores padrão (primeiro e último ano)
                self.start_year_combo.set(years_list[0])
                self.end_year_combo.set(years_list[-1])
            else:
                self.start_year_combo.config(values=[], state="disabled")
                self.end_year_combo.config(values=[], state="disabled")

            self.controller.show_translated_message('info', 'success_title', 'file_processed_success_msg')
        
        except Exception as e:
            self.controller.show_translated_message('error', 'processing_error_title', 'processing_error_msg', error=str(e))
    
    def calculate_extreme_indicators(self):
        """Calcula e mostra os indicadores climáticos."""
        print("calculate extreme indicators")
        i18n = self.controller.i18n
        if not self.processed_file_name:
            self.controller.show_translated_message(
                'warning', 'file_not_processed_title', 'file_not_processed_msg'
            )
            return
        
        start_year_str = self.start_year_combo.get()
        end_year_str = self.end_year_combo.get()

        if not start_year_str or not end_year_str:
            self.controller.show_translated_message('warning', 'year_selection_error_title', 'year_selection_error_msg')
            return

        start_year = int(start_year_str)
        end_year = int(end_year_str)

        if end_year < start_year:
            self.controller.show_translated_message('warning', 'year_selection_error_title', 'year_order_error_msg')
            return

        start_date = datetime(start_year, 1, 1)
        end_date = datetime(end_year, 12, 31)
        
        try:
            c = Climdex()
            data = c.read_files_climdex(self.output_dir, self.city)
            city_name_with_ext = self.city[0]
            city_name_only = city_name_with_ext.split('.')[0]
            self.city_name = city_name_only
            df_city = data[city_name_with_ext]

            indices = c.calculate_indices(df_city, (start_date, end_date)) # Usa as datas dos combos
            c.write_indices(indices, self.city_name, self.output_dir)

            pdf_output_path = f"{self.output_dir}/graphs_indices_{self.city_name}.pdf"
            c.plot_and_save_indices(indices, self.city_name, pdf_output_path)

            self._display_file_list(self.output_dir)

        except Exception as e:
            self.controller.show_translated_message('error', 'calc_indices_error_title', 'calc_indices_error_msg', error=str(e))

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

    def _display_file_list(self, directory):
        """Limpa o painel direito e exibe uma lista de arquivos de um diretório."""
        i18n = self.controller.i18n
        
        self._clear_panel(self.right_panel)

        try:
            # Pega a lista de arquivos
            files = os.listdir(directory)
            # Filtra para mostrar apenas arquivos (sem pastas) e talvez tipos específicos
            files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and not f.startswith('.')]
        except FileNotFoundError:
            self.controller.show_translated_message(
                'error', 'folder_not_found_title', 'folder_not_found_msg', directory=directory
            )
            return
        except Exception as e:
            self.controller.show_translated_message(
                'error', 'file_list_error_title', 'file_list_error_msg', error=str(e)
            )
            return

        list_frame = ttk.Frame(self.right_panel)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        label = ttk.Label(list_frame, text=i18n.get('generated_files_label'), font=("Verdana", 10, "bold"))
        label.pack(anchor="w", pady=(0, 5))

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        
        self.file_tree = ttk.Treeview(
            list_frame,
            columns=("filename"),
            show="headings",
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.file_tree.yview)

        self.file_tree.heading("filename", text=i18n.get('filename_header'))
        self.file_tree.column("filename", anchor="w")

        for f in sorted(files):
            self.file_tree.insert("", "end", values=(f,))

        # Empacota os widgets no frame
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Evento de clique duplo para abrir o arquivo
        def open_file_location(event):
            try:
                item_id = self.file_tree.selection()[0]
                filename = self.file_tree.item(item_id, "values")[0]
                full_path = os.path.join(directory, filename)
                
                # Abre o arquivo com o programa padrão do sistema
                if sys.platform == "win32":
                    os.startfile(full_path)
                elif sys.platform == "darwin": # macOS
                    subprocess.run(["open", full_path])
                else: # Linux
                    subprocess.run(["xdg-open", full_path])
            except IndexError:
                pass # Clique duplo fora de um item
            except Exception as e:
                 self.controller.show_translated_message(
                    'error', 'open_file_error_title', 'open_file_error_msg', file=filename, error=str(e)
                )

        self.file_tree.bind("<Double-1>", open_file_location)

    def get_parameter(self, temperature_parameter):
        print("get parameter")
        if temperature_parameter == "Maximum temperature":
            parameter = "tmax"
        elif temperature_parameter == "Minimum temperature":
            parameter = "tmin"
        elif temperature_parameter == "Precipitation":
            parameter = "prec"
        else:
            parameter = "tmean"
        return parameter
    
    def plot_monthly(self):
        print("Entrou entrou plot_monthly")
        city_name = self.city[0].split('.')
        city_name = city_name[0]
        self.city_name = city_name

        group_data(self.city, self.output_dir, self.output_dir)
        
        temperature_parameter = self.plot_param_combo.get()
        if not temperature_parameter:
            self.controller.show_translated_message('warning', 'param_not_selected_title', 'param_not_selected_msg')
            return
        
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
        
        temperature_parameter = self.plot_param_combo.get()
        if not temperature_parameter:
            self.controller.show_translated_message('warning', 'param_not_selected_title', 'param_not_selected_msg')
            return
        
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

        temperature_parameter = self.plot_param_combo.get()
        if not temperature_parameter:
            self.controller.show_translated_message('warning', 'param_not_selected_title', 'param_not_selected_msg')
            return
        
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

    def run_trend_analysis(self):
        """Coleta dados, chama a análise de tendência e exibe os resultados."""
        i18n = self.controller.i18n
        
        if not self.processed_file_name or not self.city_name:
            self.controller.show_translated_message('warning', 'file_not_processed_title', 'file_not_processed_msg')
            return
        
        temperature_parameter = self.trend_param_combo.get()
        if not temperature_parameter:
            self.controller.show_translated_message('warning', 'param_not_selected_title', 'param_not_selected_msg')
            return
        
        try:
            group_data(self.city, self.output_dir, self.output_dir)
            
            csv_file_path = f'{self.output_dir}/{self.city_name}dadosAnuais.csv' # Foco na tendência anual
            column_name = self.get_parameter(temperature_parameter) # ex: 'tmax', 'tmin', 'tmean'
            
            if column_name == "tmax":
                column_name = "Tmax"
            elif column_name == "tmin":
                column_name = "Tmin"
            elif column_name == "tmean":
                column_name = "Tmean"
            elif column_name == "Precipitation" or column_name == "prec":
                column_name = "Chuva"

            if not os.path.exists(csv_file_path):
                 self.controller.show_translated_message('error', 'file_not_found_title', 'annual_data_not_found_msg', file_path=csv_file_path)
                 return

            results = analyze_trend(csv_file_path, column_name)
            
            self._display_trend_results(results, temperature_parameter)

        except ValueError as e:
            self.controller.show_translated_message('error', 'trend_analysis_error_title', 'trend_analysis_value_error_msg', error=str(e))
        except Exception as e:
            self.controller.show_translated_message('error', 'trend_analysis_error_title', 'trend_analysis_error_msg', error=str(e))

    def _display_trend_results(self, results, param_name):
        """Limpa o painel direito e exibe os resultados da análise de tendência."""
        self._clear_panel(self.right_panel)
        i18n = self.controller.i18n

        results_frame = ttk.LabelFrame(self.right_panel, text=i18n.get('trend_results_title'))
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        grid_frame = ttk.Frame(results_frame)
        grid_frame.pack(padx=10, pady=10)

        mk_result = results.get("mann_kendall", {})
        print("MK:", mk_result)
        slope = results.get("sens_slope")

        trend = mk_result.get('trend', 'no trend')
        p_value = mk_result.get('p-value', 1.0)
        tau = mk_result.get('Tau', 0.0)
        z_score = mk_result.get('Z-score', 0.0)
        
        if trend == 'increasing':
            trend_text = i18n.get('trend_increasing')
        elif trend == 'decreasing':
            trend_text = i18n.get('trend_decreasing')
        else: # no trend
            trend_text = i18n.get('trend_no_trend')

        row_num = 0

        # Parâmetro
        ttk.Label(grid_frame, text=f"{i18n.get('parameter_label')}:", font=("Verdana", 10, "bold")).grid(row=row_num, column=0, sticky="w", pady=2); row_num += 1
        ttk.Label(grid_frame, text=param_name).grid(row=0, column=1, sticky="w", pady=2, padx=5)
        
        # Teste Mann-Kendall (Tendência)
        ttk.Label(grid_frame, text=f"{i18n.get('mann_kendall_test_label')}:", font=("Verdana", 10, "bold")).grid(row=row_num, column=0, sticky="w", pady=2); row_num += 1
        ttk.Label(grid_frame, text=trend_text).grid(row=row_num-1, column=1, sticky="w", pady=2, padx=5)

        # p-value
        ttk.Label(grid_frame, text=f"{i18n.get('p_value_label')}:", font=("Verdana", 10, "bold")).grid(row=row_num, column=0, sticky="w", pady=2); row_num += 1
        ttk.Label(grid_frame, text=f"{p_value:.6f}").grid(row=row_num-1, column=1, sticky="w", pady=2, padx=5)

        ttk.Label(grid_frame, text=f"{i18n.get('tau')}:", font=("Verdana", 10, "bold")).grid(row=row_num, column=0, sticky="w", pady=2); row_num += 1
        ttk.Label(grid_frame, text=f"{tau:.6f}").grid(row=row_num-1, column=1, sticky="w", pady=2, padx=5)

        ttk.Label(grid_frame, text=f"{i18n.get('Z-score')}:", font=("Verdana", 10, "bold")).grid(row=row_num, column=0, sticky="w", pady=2); row_num += 1
        ttk.Label(grid_frame, text=f"{z_score:.6f}").grid(row=row_num-1, column=1, sticky="w", pady=2, padx=5)
        
        ttk.Label(grid_frame, text=f"{i18n.get('sens_slope_label')}:", font=("Verdana", 10, "bold")).grid(row=row_num, column=0, sticky="w", pady=2); row_num += 1
        ttk.Label(grid_frame, text=f"{slope:.6f} (unidades/ano)").grid(row=row_num-1, column=1, sticky="w", pady=2, padx=5)
        
        ttk.Separator(grid_frame, orient='horizontal').grid(row=row_num, column=0, columnspan=2, sticky='ew', pady=10); row_num += 1
        explanation = i18n.get('trend_explanation')
        ttk.Label(grid_frame, text=explanation, wraplength=450, justify=tk.LEFT).grid(row=row_num, column=0, columnspan=2, sticky="w")

    def go_to_start_page(self):
        from ..start_page import StartPage
        self.controller.show_frame(StartPage)
        
    def update_texts(self):
        i18n = self.controller.i18n
        self.back_button.config(text=i18n.get('back_btn'))
        self.page_title.config(text=i18n.get('climate_trends_page_title'))
        self.processed_file_label.config(text=i18n.get('processed_file_label'))
        self.select_process_btn.config(text=i18n.get('select_and_process_btn'))
        self.extremes_frame.config(text=i18n.get('climate_extremes_label'))
        self.start_year_label.config(text=i18n.get('start_year_label'))
        self.end_year_label.config(text=i18n.get('end_year_label'))
        self.climatic_extremes_btn.config(text=i18n.get('climatic_extremes_btn'))
        self.analyze_trend_frame.config(text=i18n.get('analyze_trend_label'))
        self.trend_param_label.config(text=i18n.get('trend_parameter_label'))
        self.analyze_trend_btn.config(text=i18n.get('analyse_trend_btn'))
        
        self.plot_trends_frame.config(text=i18n.get('plot_trends_label'))
        self.plot_param_label.config(text=i18n.get('plot_parameter_label'))
        self.analyze_trend_btn.config(text=i18n.get('analyse_trend_btn'))
        self.plot_trends_frame.config(text=i18n.get('plot_trends_label'))
        self.monthly_btn.config(text=i18n.get('monthly_btn'))
        self.quarterly_btn.config(text=i18n.get('quarterly_btn'))
        self.annual_btn.config(text=i18n.get('annual_btn'))

        self.select_process_hint.text = i18n.get('select_process_trends_hint')
        self.processed_file_hint.text = i18n.get('processed_file_trends_hint')
        self.start_hint.text = i18n.get('start_trends_hint')
        self.end_hint.text = i18n.get('end_trends_hint')
        self.climatic_extremes_hint.text = i18n.get('climatic_trends_hint')
        self.analyze_trend_param_hint.text = i18n.get('analyze_param_trends_hint')
        self.analyze_trend_hint.text = i18n.get('analyze_trends_hint')
        self.plot_param_hint.text = i18n.get('param_trends_hint')
        self.monthly_hint.text = i18n.get('monthly_trends_hint')
        self.quarterly_hint.text = i18n.get('quarterly_trends_hint')
        self.annual_hint.text = i18n.get('monthly_trends_hint') 
