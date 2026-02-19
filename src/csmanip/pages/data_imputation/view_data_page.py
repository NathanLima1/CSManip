from ..utils import *
import numpy as np
import datetime as dt
from ..tooltip import CreateToolTip
import matplotlib.dates as mdates
if typing.TYPE_CHECKING:
    from ..data_imputation.data_imputation_page import DataImputationPage

class ViewDataPage(ttk.Frame):
    """Tela de visualização de dados dentro de imputação de dados"""
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        i18n = self.controller.i18n

        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        self.back_button = ttk.Button(top_frame, text="", command=self.go_to_data_imputation)
        self.back_button.pack(side=tk.LEFT)

        self.page_title = ttk.Label(top_frame, text="", font=("Verdana", 16, "bold"))
        self.page_title.pack(side=tk.LEFT, expand=True)

        main_container = ttk.Frame(self)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        main_container.grid_columnconfigure(0, weight=1, minsize=280)
        main_container.grid_columnconfigure(1, weight=3)
        main_container.grid_rowconfigure(0, weight=1)
        
        # --- PAINEL DA ESQUERDA ---
        left_panel = ttk.Frame(main_container)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        self.view_data_section = ttk.LabelFrame(left_panel, text="")
        self.view_data_section.pack(fill=tk.X, pady=(0, 20))

        view_inputs_grid = ttk.Frame(self.view_data_section)
        view_inputs_grid.pack(pady=10, padx=10)

        self.lbl_view_data = ttk.Label(view_inputs_grid, text="")
        self.lbl_view_param = ttk.Label(view_inputs_grid, text="")
        self.var_view_city = tk.StringVar()
        
        #self.var_view_city.trace("w", self.on_city_change)
        self.combo_view_data = ttk.Combobox(
            view_inputs_grid, 
            state="readonly", 
            values=["Target city", "Neighbor A", "Neighbor B", "Neighbor C", "Common data"],
            textvariable=self.var_view_city
        )
        self.combo_view_param = ttk.Combobox(view_inputs_grid, state="readonly", values=["Precipitation", 'Maximum temperature', "Minimum temperature"])

        self.lbl_view_data.grid(row=0, column=0, sticky="w")
        self.combo_view_data.grid(row=1, column=0, padx=(0, 5))
        self.lbl_view_param.grid(row=0, column=1, sticky="w")
        self.combo_view_param.grid(row=1, column=1, padx=(5, 0))
        self.data_view_hint = CreateToolTip(self.combo_view_data, text=i18n.get('combo_data_view_hint'))
        self.view_param_hint = CreateToolTip(self.combo_view_param, text=i18n.get('parameter_view_hint'))

        self.lbl_time_period = ttk.Label(view_inputs_grid, text="")
        self.lbl_time_period.grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky="w")

        self.lbl_view_start = ttk.Label(view_inputs_grid, text="")
        self.lbl_view_end = ttk.Label(view_inputs_grid, text="")
        self.combo_view_start = ttk.Combobox(view_inputs_grid, state="disabled")
        self.combo_view_end = ttk.Combobox(view_inputs_grid, state="disabled")

        self.lbl_view_start.grid(row=3, column=0, sticky="w")
        self.combo_view_start.grid(row=4, column=0, padx=(0, 5))
        self.lbl_view_end.grid(row=3, column=1, sticky="w")
        self.combo_view_end.grid(row=4, column=1, padx=(5, 0))
        self.view_start_hint = CreateToolTip(self.combo_view_start, text=i18n.get('start_view_hint'))
        self.view_end_hint = CreateToolTip(self.combo_view_end, text=i18n.get('end_view_hint'))

        actions_frame = ttk.Frame(self.view_data_section)
        actions_frame.pack(fill=tk.X, padx=10, pady=(5, 10))

        self.btn_select = ttk.Button(
            actions_frame,
            text="",  # texto vem do i18n
            command=self.common_graphs
        )
        self.btn_select.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))

        self.btn_def_range = ttk.Button(
            actions_frame,
            text="",  # texto vem do i18n
            command=self.range_graphs
        )
        self.btn_def_range.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0))

        # --- Gerar Gráfico ---
        self.graph_section = ttk.LabelFrame(left_panel, text="")
        self.graph_section.pack(fill=tk.X)

        graph_inputs_grid = ttk.Frame(self.graph_section)
        graph_inputs_grid.pack(pady=10, padx=10)

        self.data_hist = StringVar()
        self.paramt_hist = StringVar()
        self.lbl_graph_data = ttk.Label(graph_inputs_grid, text="")
        self.lbl_graph_param = ttk.Label(graph_inputs_grid, text="")
        self.combo_graph_data = ttk.Combobox(graph_inputs_grid, state="readonly", values=["Target city", "Neighbor A", "Neighbor B", "Neighbor C"], textvariable=self.data_hist)
        self.combo_graph_param = ttk.Combobox(graph_inputs_grid, state="readonly", values=["Precipitation", 'Maximum temperature', "Minimum temperature"], textvariable=self.paramt_hist)

        self.lbl_graph_data.grid(row=0, column=0, sticky="w")
        self.combo_graph_data.grid(row=1, column=0, padx=(0, 5))
        self.lbl_graph_param.grid(row=0, column=1, sticky="w")
        self.combo_graph_param.grid(row=1, column=1, padx=(5, 0))
        self.graph_data_hint = CreateToolTip(self.combo_graph_data, text=i18n.get('graph_data_10_view_hint'))
        self.graph_param_hint = CreateToolTip(self.combo_graph_param, text=i18n.get('graph_param_10_view_hint'))
        
        self.histogram_btn = ttk.Button(self.graph_section, text="", command=self.histogram)
        self.histogram_btn.pack(fill=tk.X, pady=5, padx=10)
        self.boxplot_btn = ttk.Button(self.graph_section, text="", command=self.boxplot_graph)
        self.boxplot_btn.pack(fill=tk.X, pady=(0,10), padx=10)
        self.histogram_hint = CreateToolTip(self.histogram_btn, text=i18n.get('histogram_view_hint'))
        self.boxplot_hint = CreateToolTip(self.boxplot_btn, text=i18n.get('boxplot_view_hint'))


        # --- PAINEL DA DIREITA ---
        self.right_panel = ttk.Frame(main_container, relief="solid", borderwidth=1)
        self.right_panel.grid(row=0, column=1, sticky="nsew")
        
        self.update_texts()

    def go_to_data_imputation(self):
        """Importa e navega para a página inicial."""
        from .data_imputation_page import DataImputationPage
        self.controller.show_frame(DataImputationPage)

    def separa_estacao(self, dados, est):
        print("Entrou Principal separa_estacao")
        if est == 1:
            mes1 = 12
            mes2 = 1
            mes3 = 2

        sazonal = list()
        aux = list()
        flag = 0
        for i in range(len(dados)):
            try:
                if mes1 == dados[i][1] or mes2 == dados[i][1] or mes3 == dados[i][1]:
                    aux.append(dados[i])
                    flag = 0
                elif dados[i+1][1] == mes3 + 1 and flag == 0:
                    sazonal.append(aux)
                    aux = list()
                    flag = 1
                
            except IndexError:
                sazonal.append(aux)
                aux = list()
        return sazonal
    
    def preparar_eixos(self, mat, foco):
        print("Entrou Principal preparar_eixos")
        x = list()
        y = list()

        for i in range(len(mat)):
            y.append(mat[i][foco])
            text = str(mat[i][1]) + '/' + str(mat[i][2]) + '/' + str(mat[i][0])
            x.append(dt.datetime.strptime(text,"%m/%d/%Y").date())
    
        return x, y

    def prepara_mat(self, dados, foco):
        print("Entrou principal prepara_mat")
        mat = list()
        for i in range(len(dados)):
            mat.append([int(dados[i][0]), int(dados[i][1]), int(dados[i][2]), float(dados[i][foco])])
        return mat

    def histogram(self):
        t = DataProcessing()
        data_hist = self.data_hist.get()
        if data_hist == '':
            self.controller.show_translated_message(
                msg_type='warning',
                title_key='missing_city_title',
                message_key='select_a_city_msg'
                )

        data = t.load_data_file(data_hist)
        if self.paramt_hist.get() == "Precipitation":
            col = 3
        elif self.paramt_hist.get() == "Maximum temperature":
            col = 4
        elif self.paramt_hist.get() == "Minimum temperature":
            col = 5
        else:
            self.controller.show_translated_message(
                msg_type='warning',
                title_key='missing_parameter_title',
                message_key='select_a_parameter_msg'
                )

        mat = self.prepara_mat(data, col)
        
        saz = self.separa_estacao(mat,1)
        del saz[0]
        
        ultimo = len(saz) - 2
        
        x1, y1 = self.preparar_eixos(saz[ultimo-9], 3)
        x2, y2 = self.preparar_eixos(saz[ultimo-8], 3)
        x3, y3 = self.preparar_eixos(saz[ultimo-7], 3)
        x4, y4 = self.preparar_eixos(saz[ultimo-6], 3)
        x5, y5 = self.preparar_eixos(saz[ultimo-5], 3)
        x6, y6 = self.preparar_eixos(saz[ultimo-4], 3)
        x7, y7 = self.preparar_eixos(saz[ultimo-3], 3)
        x8, y8 = self.preparar_eixos(saz[ultimo-2], 3)
        x9, y9 = self.preparar_eixos(saz[ultimo-1], 3)
        x10, y10 = self.preparar_eixos(saz[ultimo], 3)

        
        x = list()
        cont = 17
        
        for i in range(17, 50):
            x.append(cont)
            cont += 0.5
        max_lim = max(max(y1), max(y2), max(y3), max(y4), max(y5), max(y6), max(y7), max(y8), max(y9), max(y10)) +0.5
        min_lim = min(min(y1), min(y2), min(y3), min(y4), min(y5), min(y6), min(y7), min(y8), min(y9), min(y10)) -0.5

        
        y1 = np.array(y1)
        y2 = np.array(y2)
        y3 = np.array(y3)
        y4 = np.array(y4)
        y5 = np.array(y5)
        y6 = np.array(y6)
        y7 = np.array(y7)
        y8 = np.array(y8)
        y9 = np.array(y9)
        y10 = np.array(y10)


        fig = Figure(figsize=(14.5,9.5), dpi=100)
        fig.subplots_adjust(left=0.05, bottom=0.08, right=0.98, top=0.93)
        plot1 = fig.add_subplot(2,5,1)
        plot1.set_title(saz[ultimo-9][len(saz[ultimo-9])-1][0])
        plot1.hist(y1, bins=40, linewidth=0.5, edgecolor="white")
        plot1.set_xlim((min_lim, max_lim))
        plot1.axvline(y1.mean(), color='red')
        

        plot2 = fig.add_subplot(2,5,2)
        plot2.set_title(saz[ultimo-8][len(saz[ultimo-8])-1][0])
        plot2.hist(y2, bins=40, linewidth=0.5, edgecolor="white")
        plot2.set_xlim((min_lim, max_lim))
        plot2.axvline(y2.mean(), color='red')

        plot3 = fig.add_subplot(2,5,3)
        plot3.set_title(saz[ultimo-7][len(saz[ultimo-7])-1][0])
        plot3.hist(y3, bins=40, linewidth=0.5, edgecolor="white")
        plot3.set_xlim((min_lim, max_lim))
        plot3.axvline(y3.mean(), color='red')


        plot4 = fig.add_subplot(2,5,4)
        plot4.set_title(saz[ultimo-6][len(saz[ultimo-6])-1][0])
        plot4.hist(y4, bins=40, linewidth=0.5, edgecolor="white")
        plot4.set_xlim((min_lim, max_lim))
        plot4.axvline(y4.mean(), color='red')


        plot5 = fig.add_subplot(2,5,5)
        plot5.set_title(saz[ultimo-5][len(saz[ultimo-5])-1][0])
        plot5.hist(y5, bins=40, linewidth=0.5, edgecolor="white")
        plot5.set_xlim((min_lim, max_lim))
        plot5.axvline(y5.mean(), color='red')


        plot6 = fig.add_subplot(2,5,6)
        plot6.set_title(saz[ultimo-4][len(saz[ultimo-4])-1][0])
        plot6.hist(y6, bins=40, linewidth=0.5, edgecolor="white")
        plot6.set_xlim((min_lim, max_lim))
        plot6.axvline(y6.mean(), color='red')


        plot7 = fig.add_subplot(2,5,7)
        plot7.set_title(saz[ultimo-3][len(saz[ultimo-3])-1][0])
        plot7.hist(y7, bins=40, linewidth=0.5, edgecolor="white")
        plot7.set_xlim((min_lim, max_lim))
        plot7.axvline(y7.mean(), color='red')


        plot8 = fig.add_subplot(2,5,8)
        plot8.set_title(saz[ultimo-2][len(saz[ultimo-2])-1][0])
        plot8.hist(y8, bins=40, linewidth=0.5, edgecolor="white")
        plot8.set_xlim((min_lim, max_lim))
        plot8.axvline(y8.mean(), color='red')


        plot9 = fig.add_subplot(2,5,9)
        plot9.set_title(saz[ultimo-1][len(saz[ultimo-1])-1][0])
        plot9.hist(y9, bins=40, linewidth=0.5, edgecolor="white")
        plot9.set_xlim((min_lim, max_lim))
        plot9.axvline(y9.mean(), color='red')


        plot10 = fig.add_subplot(2,5,10)
        plot10.set_title(saz[ultimo][len(saz[ultimo])-1][0])
        plot10.hist(y10, bins=40, linewidth=0.5, edgecolor="white")
        plot10.set_xlim((min_lim, max_lim))
        plot10.axvline(y10.mean(), color='red')


        for widget in self.right_panel.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.right_panel)
        canvas.draw()
        
        toolbar = NavigationToolbar2Tk(canvas, self.right_panel)
        toolbar.update()
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)

        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def boxplot_graph(self):
        t = DataProcessing()
        data_hist = self.data_hist.get()
        if data_hist == '':
            self.controller.show_translated_message(
                msg_type='warning',
                title_key='missing_city_title',
                message_key='select_a_city_msg'
                )

        data = t.load_data_file(data_hist)
        if self.paramt_hist.get() == "Precipitation":
            col = 3
        elif self.paramt_hist.get() == "Maximum temperature":
            col = 4
        elif self.paramt_hist.get() == "Minimum temperature":
            col = 5
        else:
            self.controller.show_translated_message(
                msg_type='warning',
                title_key='missing_parameter_title',
                message_key='select_a_parameter_msg'
                )

        mat = self.prepara_mat(data, col)
        
        saz = self.separa_estacao(mat,1)
        del saz[0]
        
        ultimo = len(saz) - 2
        
        x1, y1 = self.preparar_eixos(saz[ultimo-9], 3)
        x2, y2 = self.preparar_eixos(saz[ultimo-8], 3)
        x3, y3 = self.preparar_eixos(saz[ultimo-7], 3)
        x4, y4 = self.preparar_eixos(saz[ultimo-6], 3)
        x5, y5 = self.preparar_eixos(saz[ultimo-5], 3)
        x6, y6 = self.preparar_eixos(saz[ultimo-4], 3)
        x7, y7 = self.preparar_eixos(saz[ultimo-3], 3)
        x8, y8 = self.preparar_eixos(saz[ultimo-2], 3)
        x9, y9 = self.preparar_eixos(saz[ultimo-1], 3)
        x10, y10 = self.preparar_eixos(saz[ultimo], 3)

        
        x = list()
        cont = 17
        
        for i in range(17, 50):
            x.append(cont)
            cont += 0.5
        max_lim = max(max(y1), max(y2), max(y3), max(y4), max(y5), max(y6), max(y7), max(y8), max(y9), max(y10)) +0.5
        min_lim = min(min(y1), min(y2), min(y3), min(y4), min(y5), min(y6), min(y7), min(y8), min(y9), min(y10)) -0.5

        boxplot = list()
        boxplot.append(y1)
        boxplot.append(y2)
        boxplot.append(y3)
        boxplot.append(y4)
        boxplot.append(y5)
        boxplot.append(y6)
        boxplot.append(y7)
        boxplot.append(y8)
        boxplot.append(y9)
        boxplot.append(y10)


        fig = Figure(figsize=(14.5,9.5), dpi=100)
        fig.subplots_adjust(left=0.05, bottom=0.08, right=0.98, top=0.93)
     
        plot1 = fig.add_subplot(1,1,1)
        plot1.set_title("Boxplot for Maximum temperature [10 Years]")
        plot1.boxplot(boxplot)
        plot1.set_xlabel('Year')
        plot1.set_ylabel(self.data_hist.get())
        

        for widget in self.right_panel.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.right_panel)
        canvas.draw()

        toolbar = NavigationToolbar2Tk(canvas, self.right_panel)
        toolbar.update()
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)

        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
    def update_texts(self):
        """Atualiza os textos APENAS para esta tela."""
        i18n = self.controller.i18n
        
        self.back_button.config(text=i18n.get('back_btn'))
        self.page_title.config(text=i18n.get('view_data_page_title'))

        self.view_data_section.config(text=i18n.get('view_data_title'))
        self.lbl_view_data.config(text=i18n.get('data_label'))
        self.lbl_view_param.config(text=i18n.get('parameter_label'))
        self.lbl_time_period.config(text=i18n.get('define_time_period_subtitle'))
        self.lbl_view_start.config(text=i18n.get('start_label'))
        self.lbl_view_end.config(text=i18n.get('end_label'))

        self.graph_section.config(text=i18n.get('last_10_years_graph_title'))
        self.lbl_graph_data.config(text=i18n.get('data_label'))
        self.lbl_graph_param.config(text=i18n.get('parameter_label'))
        self.histogram_btn.config(text=i18n.get('histogram_btn'))
        self.boxplot_btn.config(text=i18n.get('boxplot_btn'))
        self.btn_select.config(text=i18n.get('select_btn'))
        self.btn_def_range.config(text=i18n.get('def_range_btn'))

        self.data_view_hint.text = i18n.get('combo_data_view_hint')
        self.view_param_hint.text = i18n.get('param_view_hint')
        self.view_start_hint.text = i18n.get('start_view_hint')
        self.view_end_hint.text = i18n.get('end_view_hint')
        self.graph_data_hint.text = i18n.get('graph_data_10_view_hint')
        self.graph_param_hint.text = i18n.get('graph_param_10_view_hint')
        self.histogram_hint.text = i18n.get('histogram_view_hint')
        self.boxplot_hint.text = i18n.get('boxplot_view_hint')

    def get_col(self):
        print("Entrou Principal get_col")
        if self.combo_view_param.get() == "Precipitation":
            y_name = "Precipitation (mm)"
            col = 3
        elif self.combo_view_param.get() == "Maximum temperature":
            col = 4
            y_name = "Temperature (°C)"
        elif self.combo_view_param.get() == "Minimum temperature":
            y_name = "Temperature (°C)"
            col = 5
        else:
            msg.showwarning(title="Parameter Missing!", message="You must select a parameter!")
        return y_name, col

    def common_graphs(self):
        print("Entrou Principal common_graphs")
        data_processor = DataProcessing()
        type_data = self.combo_view_data.get()
        if type_data == '':
            msg.showwarning(title="City Missing!", message="You must select a city!")

        analyzed_data = data_processor.load_data_file(type_data)

        self.generate_range()

        y_label, col_index = self.get_col()

        city_names = data_processor.get_city_names()

        x_axis = []
        if self.combo_view_data.get() == 'Common data':
            y_axis_1, y_axis_2, y_axis_3, y_axis_4 = [], [], [], []
            common_count, target_count, va_count, vb_count, vc_count = data_processor.get_quantities()
            bar_y_values = [common_count, target_count, va_count, vb_count, vc_count]
            bar_x_labels = ['Common', city_names[0], city_names[1], city_names[2], city_names[3]]
        else:
            y_axis = []

        data_table = []
        for row in analyzed_data:
            data_table.append(row)
            year, month, day = str(row[0]), str(row[1]), str(row[2])
            date_str = f"{month}/{day}/{year}"

            try:
                date_obj = dt.datetime.strptime(date_str, "%m/%d/%Y").date()
            except ValueError:
                continue

            if self.combo_view_data.get() == 'Common data':
                try:
                    y_axis_1.append(float(row[col_index].replace(',', '.')))
                    y_axis_2.append(float(row[col_index + 3].replace(',', '.')))
                    y_axis_3.append(float(row[col_index + 6].replace(',', '.')))
                    y_axis_4.append(float(row[col_index + 9].replace(',', '.')))
                    x_axis.append(date_obj)
                except ValueError:
                    continue
            else:
                try:
                    y_axis.append(float(row[col_index]))
                    x_axis.append(date_obj)
                except ValueError:
                    continue

        fig = Figure(figsize=(14.5, 9.5), dpi=100)
        fig.subplots_adjust(left=0.05, bottom=0.08, right=0.98, top=0.93)

        if self.combo_view_data.get() == 'Common data':
            plot1 = fig.add_subplot(321)
            plot2 = fig.add_subplot(322)
            plot3 = fig.add_subplot(323)
            plot4 = fig.add_subplot(324)
            plot5 = fig.add_subplot(325)
            plot6 = fig.add_subplot(326)

            plot1.plot(x_axis, y_axis_1, label=city_names[0])
            plot2.plot(x_axis, y_axis_2, label=city_names[1], color="red")
            plot3.plot(x_axis, y_axis_3, label=city_names[2], color='green')
            plot4.plot(x_axis, y_axis_4, label=city_names[3], color='orange')

            plot5.scatter(x_axis, y_axis_1, s=2, alpha=1, color='blue')
            plot5.scatter(x_axis, y_axis_2, s=2, alpha=1, color='red')
            plot5.scatter(x_axis, y_axis_3, s=2, alpha=1, color='green')
            plot5.scatter(x_axis, y_axis_4, s=2, alpha=1, color='orange')

            plot6.bar(bar_x_labels, bar_y_values)

            for plot in [plot1, plot2, plot3, plot4, plot5]:
                plot.set_xticklabels(x_axis, rotation=15, ha='right')
                plot.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y"))
                plot.grid(True)
                plot.set_ylabel(y_label)
                plot.legend()

            plot6.set_ylabel('Data Count')
        else:
            plot1 = fig.add_subplot(111)
            plot1.plot(x_axis, y_axis)
            plot1.set_xticklabels(x_axis, rotation=15, ha='right')
            plot1.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y"))
            plot1.grid(True)
            plot1.set_ylabel(y_label)
            plot1.set_title(self.combo_view_param.get())

        for widget in self.right_panel.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.right_panel)
        canvas.draw()

        toolbar = NavigationToolbar2Tk(canvas, self.right_panel)
        toolbar.update()
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)

        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def range_graphs(self):
        print("Entrou Principal range_graphs")
        my_data = DataProcessing()
        data_ana = my_data.load_data_file(self.combo_view_data.get())
        
        nome_y, col = self.get_col()

        ano_inicio = int(self.var_ini.get())
        ano_final = int(self.var_fim.get())
        if ano_final < ano_inicio:
            msg.showerror(title='Invalid', message='The entered range is invalid')
            return
        if self.combo_view_param.get() == 'Common data':
            self.grafico_dc(ano_inicio,ano_final)
            return
        
        eixo_x = list()
        if self.combo_view_data.get() == 'Common data':
            eixo_y1 = list()
            eixo_y2 = list()
            eixo_y3 = list()
            eixo_y4 = list()
            util, tar,t_va, t_vb, t_vc = my_data.get_quantities()
            eixo_y_bar = [util, tar,t_va, t_vb, t_vc]
            eixo_x_bar = ['Common', 'target','Total vA', 'Total vB', 'Total vC']
        else:
            eixo_y = list()

        dados_lb = list()

        for i in data_ana:
            if int(i[0]) >= ano_inicio and int(i[0]) <= ano_final:
                dados_lb.append(i)

                ano = str(i[0])
                
                mes = str(i[1])
                dia = str(i[2])
                text_data = mes + '/' + dia + '/' + ano
                eixo_x.append(dt.datetime.strptime(text_data,"%m/%d/%Y").date())

                if self.combo_view_data.get() == 'Common data':
                    eixo_y1.append(float(i[col]))
                    eixo_y2.append(float(i[col+3]))
                    eixo_y3.append(float(i[col+6]))
                    eixo_y4.append(float(i[col+9]))
                else:
                    eixo_y.append(float(i[col]))
        
        
        fig = Figure(figsize=(14.5,9.5), dpi=100)
        fig.subplots_adjust(left=0.05, bottom=0.08, right=0.98, top=0.93)

        if self.combo_view_data.get() == 'Common data':
            plot1 = fig.add_subplot(321)
            plot2 = fig.add_subplot(322)
            plot3 = fig.add_subplot(323)
            plot4 = fig.add_subplot(324)
            plot5 = fig.add_subplot(325)
            plot6 = fig.add_subplot(326)
            plot1.plot(eixo_x, eixo_y1, label="target")
            plot2.plot(eixo_x, eixo_y2, label="Neighbor_a", color="red")
            plot3.plot(eixo_x, eixo_y3, label="Neighbor_b", color='green')
            plot4.plot(eixo_x, eixo_y4, label="Neighbor_c", color='orange')
            plot5.scatter(eixo_x, eixo_y1, s=2, alpha=1, color='blue')
            plot5.scatter(eixo_x, eixo_y2, s=2, alpha=0.6, color='red')
            plot5.scatter(eixo_x, eixo_y3, s=2, alpha=0.6, color='green')
            plot5.scatter(eixo_x, eixo_y4, s=2, alpha=0.6, color='orange')
            plot6.bar(eixo_x_bar, eixo_y_bar)
            plot1.legend()
            plot2.legend()
            plot3.legend()
            plot4.legend()
            plot1.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y")) 
            plot2.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y")) 
            plot3.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y")) 
            plot4.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y")) 
            plot5.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y")) 
            plot1.grid(True)
            plot2.grid(True)
            plot3.grid(True)
            plot4.grid(True)
            plot5.grid(True)
            plot1.set_ylabel(nome_y)
            plot2.set_ylabel(nome_y)
            plot3.set_ylabel(nome_y)
            plot4.set_ylabel(nome_y)
            plot5.set_ylabel(nome_y)
            plot6.set_ylabel('Data quantity')
            
        else:
            plot1 = fig.add_subplot(111)
            plot1.plot(eixo_x, eixo_y)
            plot1.set_xticklabels(eixo_x, rotation=15, ha='right')   
            plot1.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y"))   
                
            plot1.grid(True)
            plot1.set_ylabel(nome_y)
            plot1.set_title(self.combo_view_param.get())
        
        for widget in self.right_panel.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.right_panel)
        canvas.draw()

        toolbar = NavigationToolbar2Tk(canvas, self.right_panel)
        toolbar.update()
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)

        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    def generate_range(self):
        print("Entrou generate_range")

        data_proc = DataProcessing()
        self.anos = data_proc.get_year_range(self.combo_view_data.get())

        self.var_ini = tk.StringVar()
        self.var_fim = tk.StringVar()

        self.combo_view_start.config(
            state="readonly",
            values=self.anos,
            textvariable=self.var_ini
        )

        self.combo_view_end.config(
            state="readonly",
            values=self.anos,
            textvariable=self.var_fim
        )