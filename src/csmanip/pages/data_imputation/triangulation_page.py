from ..utils import *
from ..tooltip import CreateToolTip

if typing.TYPE_CHECKING:
    from .imputation_techniques_page import ImputationTechniquesPage

class TriangulationPage(ttk.Frame):
    """Tela para configurar e executar a imputação por triangulação."""
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        i18n = controller.i18n

        self.graph_canvas = None
        self.toolbar = None

        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        self.back_button = ttk.Button(top_frame, text="", command=self.go_to_imputation_techniques)
        self.back_button.pack(side=tk.LEFT)

        self.page_title = ttk.Label(top_frame, text="", font=("Verdana", 16, "bold"))
        self.page_title.pack(side=tk.LEFT, expand=True)

        # --- Layout Principal de Duas Colunas ---
        main_container = ttk.Frame(self)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        main_container.grid_columnconfigure(0, weight=1, minsize=250)
        main_container.grid_columnconfigure(1, weight=3)
        main_container.grid_rowconfigure(0, weight=1)
        
        # --- PAINEL DA ESQUERDA ---
        left_panel = ttk.Frame(main_container)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        self.method_label = ttk.Label(left_panel, text="")
        self.method_label.pack(anchor="w", pady=(0, 2), padx=5)
        
        self.method_combo = ttk.Combobox(left_panel, state="readonly", 
                                         values=['Arithmetic Average', 'Inverse Distance Weighted', 
                                                 'Regional Weight', 'Optimized Normal Ratio'])
        self.method_combo.pack(fill=tk.X, pady=(0, 15), padx=5)
        self.method_hint = CreateToolTip(self.method_combo, text=i18n.get('method_triang_hint'))

        self.parameter_label = ttk.Label(left_panel, text="")
        self.parameter_label.pack(anchor="w", pady=(0, 2), padx=5)

        self.parameter_combo = ttk.Combobox(left_panel, state="readonly",
                                            values=["Precipitation", 'Maximum temperature', "Minimum temperature"])
        self.parameter_combo.pack(fill=tk.X, pady=(0, 15), padx=5)
        self.param_hint = CreateToolTip(self.parameter_combo, text=i18n.get('param_triang_hint'))

        self.run_triangulation_btn = ttk.Button(left_panel, text="", command=self.run_triangulation_analysis)
        self.run_triangulation_btn.pack(pady=20, padx=5)
        self.run_btn_hint = CreateToolTip(self.run_triangulation_btn, text=i18n.get('btn_triang_hint'))


        # --- PAINEL DA DIREITA ---
        self.right_panel = ttk.Frame(main_container, relief="solid", borderwidth=1)
        self.right_panel.grid(row=0, column=1, sticky="nsew")
        
        self.update_texts()

    def go_to_imputation_techniques(self):
        """Importa e navega para a página inicial."""
        from .imputation_techniques_page import ImputationTechniquesPage
        self.controller.show_frame(ImputationTechniquesPage)

    def run_triangulation_analysis(self):
        """Pega os dados dos combos, executa a triangulação e plota o gráfico."""
        if self.graph_canvas:
            self.graph_canvas.get_tk_widget().destroy()
        if self.toolbar:
            self.toolbar.destroy()

        met = self.method_combo.get()
        ind = self.parameter_combo.get()

        if not met:
            self.controller.show_translated_message(
                msg_type='warning',
                title_key='missing_method_title',
                message_key='select_a_triang_method_msg'
                )
            return
        if not ind:
            self.controller.show_translated_message(
                msg_type='warning',
                title_key='missing_parameter_title',
                message_key='select_a_parameter_msg'
                )
            return

        trian = Triangulation() 

        if ind == "Precipitation":
            focus = 1
            y_label = "Precipitation (mm)"
        elif ind == 'Maximum temperature':
            focus = 2
            y_label = "Temperature(°C)"
        else: # Minimum temperature
            focus = 3
            y_label = "Temperature(°C)"

        if met == 'Arithmetic Average':
            trian.avg(focus)
            eixo_x, eixo_y_tri, eixo_y_exato, media_ea, media_er, _ = trian.get_avg()
        elif met == 'Inverse Distance Weighted':
            trian.idw(focus)
            eixo_x, eixo_y_tri, eixo_y_exato, media_ea, media_er, _ = trian.get_idw()
        elif met == 'Regional Weight':
            trian.rw(focus)
            eixo_x, eixo_y_tri, eixo_y_exato, media_ea, media_er, _ = trian.get_rw()
        else: # Optimized Normal Ratio
            trian.onr(focus)
            eixo_x, eixo_y_tri, eixo_y_exato, media_ea, media_er, _ = trian.get_onr()

        # 4. Criação e Plotagem da Figura Matplotlib
        media_ea = round(media_ea, 4)
        media_er = round(media_er, 4)
        texto_titulo = f'Mean Absolute Error: {media_ea} | Mean Relative Error: {media_er}'
        
        figura = Figure(figsize=(8, 6), dpi=100)
        plot = figura.add_subplot(111)
        plot.plot(eixo_x, eixo_y_exato, label='Exact', color='green')
        plot.plot(eixo_x, eixo_y_tri, label=f'Triangulated ({met})', color='red')
        plot.legend()
        plot.grid(True)
        plot.set_ylabel(y_label)
        plot.set_xlabel("Comparisons")
        plot.set_title(texto_titulo, fontsize=10)
        figura.tight_layout()

        self.graph_canvas = FigureCanvasTkAgg(figura, master=self.right_panel)
        self.graph_canvas.draw()
        self.graph_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.toolbar = NavigationToolbar2Tk(self.graph_canvas, self.right_panel)
        self.toolbar.update()
        self.toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def update_texts(self):
        """Atualiza os textos APENAS para esta tela."""
        i18n = self.controller.i18n
        
        self.back_button.config(text=i18n.get('back_btn'))
        self.page_title.config(text=i18n.get('triangulation_page_title'))
        self.method_label.config(text=i18n.get('triangulation_method_label'))
        self.parameter_label.config(text=i18n.get('climatic_parameter_label'))
        self.run_triangulation_btn.config(text=i18n.get('run_triangulation_btn'))
        self.method_hint.text = i18n.get('method_triang_hint')
        self.param_hint.text = i18n.get('param_triang_hint')
        self.run_btn_hint.text = i18n.get('btn_triang_hint')