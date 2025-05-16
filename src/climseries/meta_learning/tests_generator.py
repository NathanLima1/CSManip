from meta_learning.meta_learning import MetaLearning
import tkinter as tk
from tkinter import ttk
from tkinter import Label, LabelFrame, Toplevel, StringVar, IntVar, Entry, Button, Checkbutton, CENTER
from tksheet import Sheet
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from styles import colors

class TestsGenerator(Toplevel):
    # antiga MetaLearning
    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)
        self.title('Meta Learning')
        self.geometry("800x800")

        self.configure(background=colors.fundo)

        Label(self, text='META-LEARNING', font='Arial 14 bold', fg='white', bg=colors.fundo).place(x=240, y=20)

        LabelFrame(self, text='TESTE PERSONALIZADO:', width=600, height=450, font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=20, y=60)

        Label(self, text='Base-Learning (Level 0):', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=40, y=90)
        self.ml_lv0_p = StringVar()
        self.ml_lv0_p.set('Decision Trees')
        lista_ml0 =  ['Nenhum','Decision Trees', 'Neural network', 'Nearest Neighbors', 'Support Vector', 'Gaussian Process']
        ttk.Combobox(self, values=lista_ml0, textvariable=self.ml_lv0_p, width=30, font='Arial 11', justify=CENTER, state='readonly').place(x=40, y=120)

        Label(self, text='Triangulation (Level 0):', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=40, y=190)
        self.ml_tr0_p = StringVar()
        self.ml_tr0_p.set('Arithmetic Average')
        lista_tr0 =  ['Nenhum', 'Arithmetic Average', 'Inverse Distance Weighted', 'Regional Weight', 'Optimized Normal Ratio']
        ttk.Combobox(self, values=lista_tr0, textvariable=self.ml_tr0_p, width=30, font='Arial 11', justify=CENTER, state='readonly').place(x=40, y=220)

        Label(self, text='Meta-Learning (Level 1):', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=340, y=145)
        self.ml_lv1 = StringVar()
        self.ml_lv1.set('Decision Trees')
        lista_ml1 =  ['Decision Trees', 'Neural network', 'Nearest Neighbors', 'Support Vector', 'Gaussian Process']
        ttk.Combobox(self, values=lista_ml1, textvariable=self.ml_lv1, width=30, font='Arial 11', justify=CENTER, state='readonly').place(x=340, y=175)

        Label(self, text='Indicador climático:', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=40, y=270)
        self.ind_meta_perso = StringVar()
        self.ind_meta_perso.set('Temperatura máxima')
        lista_ind_meta_p = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
        ttk.Combobox(self, values=lista_ind_meta_p, textvariable=self.ind_meta_perso, width=30, font='Arial 11', justify=CENTER, state='readonly').place(x=40, y=300)

        self.num_teste_mtp = IntVar()
        self.num_teste_mtp.set(1)
        Label(self, text="Número de testes (int):", font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=340, y=270)
        self.ent_num_teste = Entry(self, textvariable=self.num_teste_mtp, width=29, font='Arial 12', justify=CENTER).place(x=340, y=300)

        Label(self, text='Deseja usar alguma ML pré-parametrizada?', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=40, y=340)
        self.pre_para_lv0 = IntVar()
        self.pre_para_lv1 = IntVar()
        Checkbutton(self, text='Level 0', variable=self.pre_para_lv0, bg=colors.fundo, font='Arial 12 bold', activebackground=colors.fundo).place(x=40, y=360)
        Checkbutton(self, text='Level 1', variable=self.pre_para_lv1, bg=colors.fundo, font='Arial 12 bold', activebackground=colors.fundo).place(x=180, y=360)
        
        Label(self, text='Deseja utilizar a janela deslizante?', font='Arial 12 bold', fg='White', bg=colors.fundo).place(x=40, y=400)
        self.type_input = StringVar()
        self.type_input.set('Sim')
        lista_type_input = ['Sim', 'Não']
        ttk.Combobox(self, values=lista_type_input, textvariable=self.type_input, width=30, font='Arial 11', justify=CENTER, state='readonly').place(x=40, y=430)
        
        Button(self, text='Gerar Preview', font='Arial 11 bold', bg=colors.meta_le, fg='white', width=62, command=self.generate_custom_test).place(x=40, y=470)

        '''Teste global'''
        LabelFrame(self, text='TESTE GLOBAL:', width=600, height=210, font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=20, y=520)
        
        Label(self, text='Quais MLs você deseja utilizar?', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=40, y=550)

        self.pre_nn_comb = IntVar()
        self.pre_dt_comb = IntVar()
        self.pre_nneig_comb = IntVar()
        self.pre_sv_comb = IntVar()
        self.pre_gp_comb = IntVar()
        Checkbutton(self, text='NN', variable=self.pre_nn_comb, bg=colors.fundo, font='Arial 12 bold', activebackground=colors.fundo).place(x=40, y=580)
        Checkbutton(self, text='DT', variable=self.pre_dt_comb, bg=colors.fundo, font='Arial 12 bold', activebackground=colors.fundo).place(x=140, y=580)
        Checkbutton(self, text='NNeig.', variable=self.pre_nneig_comb, bg=colors.fundo, font='Arial 12 bold', activebackground=colors.fundo).place(x=240, y=580)
        Checkbutton(self, text='SV', variable=self.pre_sv_comb, bg=colors.fundo, font='Arial 12 bold', activebackground=colors.fundo).place(x=340, y=580)
        Checkbutton(self, text='GP', variable=self.pre_gp_comb, bg=colors.fundo, font='Arial 12 bold', activebackground=colors.fundo).place(x=440, y=580)
        
        Label(self, text='Indicador climático:', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=40, y=620)
        self.ind_meta_comb = StringVar()
        self.ind_meta_comb.set('Temperatura máxima')
        lista_ind_meta_p = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
        ttk.Combobox(self, values=lista_ind_meta_p, textvariable=self.ind_meta_comb, width=30, font='Arial 11', justify=CENTER, state='readonly').place(x=40, y=650)

        self.num_teste_mtc = IntVar()
        self.num_teste_mtc.set(1)
        Label(self, text="Número de testes (int):", font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=340, y=620)
        self.ent_num_teste = Entry(self, textvariable=self.num_teste_mtc, width=29, font='Arial 12', justify=CENTER).place(x=340, y=650)
        
        Button(self, text='Gerar Preview TG', font='Arial 11 bold', bg=colors.meta_le, fg='white', width=62, command=self.gerar_teste_global).place(x=40, y=690)

        #Aviso
        LabelFrame(self, text='ATENÇÃO:', width=600, height=120, font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=20, y=740)
        Label(self, text='Dependendo da combinação feita no "Teste Personalizado" ou no "TESTE ', font='Arial 12 bold', fg='#FF8C00', bg=colors.fundo).place(x=40, y=770)
        Label(self, text='GLOBAL", pode demorar alguns minutos, devido ao processamento.', font='Arial 12 bold', fg='#FF8C00', bg=colors.fundo).place(x=40, y=790)
        Label(self, text='Fique à vontade para utilizar seu computador para fazer outras coisas.', font='Arial 12 bold', fg='#FF8C00', bg=colors.fundo).place(x=40, y=820)

    def generate_custom_test(self):
        """
        Antiga gerar_teste_perso
        """
        # Retrieve user inputs
        base_model = self.ml_lv0_p.get()
        triangulation = self.ml_tr0_p.get()
        meta_model = self.ml_lv1.get()
        indicator = self.ind_meta_perso.get()
        num_tests = int(self.num_teste_mtp.get())
        pre_level_0 = int(self.pre_para_lv0.get())
        pre_level_1 = int(self.pre_para_lv1.get())
        input_window = self.type_input.get()

        # Determine focus based on indicator type
        if indicator == 'Precipitação':
            focus = 1
        elif indicator == 'Temperatura máxima':
            focus = 2
        elif indicator == 'Temperatura mínima':
            focus = 3

        # Perform meta-learning
        meta = MetaLearning()
        meta_ea, meta_er, meta_percent_error, meta_r2, x_meta, y_meta, y_target, \
        base_ea, base_er, base_percent, base_r2, tria_ea, tria_er = \
            meta.customized_meta_learning(focus, base_model, triangulation, meta_model, 0, 0, num_tests, input_window)

        # Create result preview frame
        LabelFrame(self, text='RESULTS PREVIEW:', width=1250, height=950,
                font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=640, y=60)

        # Display error metrics
        errors = [
            ("ABSOLUTE ERROR:", base_ea, tria_ea, meta_ea),
            ("RELATIVE ERROR:", base_er, tria_er, meta_er),
            ("ERROR (%):", base_percent, tria_ea * 100, meta_percent_error),
            ("R2:", base_r2, None, meta_r2)
        ]

        y_positions = [90, 130, 170, 210]
        for idx, (label, val1, val2, val3) in enumerate(errors):
            text = f"{label:<20}  Machine Learning: {round(val1, 4)}"
            if val2 is not None:
                text += f"   ||   Triangulation: {round(val2, 4)}"
            if val3 is not None:
                text += f"   ||   Meta Learning: {round(val3, 4)}"
            Label(self, text=text, font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=660, y=y_positions[idx])

        # Create figure for plotting results
        figure = Figure(figsize=(12.3, 7.5), dpi=100)

        # Absolute Error
        ax1 = figure.add_subplot(2, 2, 1)
        ax1.bar(["ML", "Triang", "Meta"], [base_ea, tria_ea, meta_ea])
        ax1.set_ylabel("Absolute Error")

        # Relative Error
        ax2 = figure.add_subplot(2, 2, 2)
        ax2.bar(["ML", "Triang", "Meta"], [base_er, tria_er, meta_er])
        ax2.set_ylabel("Relative Error")

        # Percentage Error
        ax3 = figure.add_subplot(2, 2, 3)
        ax3.bar(["ML", "Triang", "Meta"], [base_percent, tria_ea * 100, meta_percent_error])
        ax3.set_ylabel("Error (%)")

        # R² Score
        ax4 = figure.add_subplot(2, 2, 4)
        ax4.bar(["ML", "Meta"], [base_r2, meta_r2])
        ax4.set_ylabel("R²")

        # Embed the figure in the Tkinter window
        canvas = FigureCanvasTkAgg(figure, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()
        canvas.get_tk_widget().place(x=650, y=250)

        # Add navigation toolbar
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.place(x=1150, y=10)
        toolbar.update()

    def generate_global_test(self):
        target_variable = self.ind_meta_comb.get()
        num_tests = int(self.num_teste_mtc.get())
        window_type = 'Sim'

        meta_learner = MetaLearning()
        all_models, model_ranking = meta_learner.combine_meta_learning(target_variable, 0, 0, num_tests, window_type)

        LabelFrame(
            self, text='RESULTS:', width=1260, height=950,
            font='Arial 12 bold', fg='white', bg=colors.fundo
        ).place(x=640, y=60)

        Label(
            self, text='Generated Models:', font='Arial 12 bold',
            fg='white', bg=colors.fundo
        ).place(x=660, y=90)

        all_data = []
        for model in all_models:
            row = [
                model[0],  # Model name
                model[1],  # Base learning
                model[2],  # Triangulation
                model[3],  # Meta learning
                model[5],  # Absolute Error
                model[6],  # Relative Error
                model[7],  # Percentage Error
            ]
            all_data.append(row)

        self.all_models_table = Sheet(
            self, data=all_data,
            headers=[
                'Model', 'Base Learning', 'Triangulation',
                'Meta Learning', 'Absolute Error',
                'Relative Error', 'Error (%)'
            ],
            width=890, height=500
        )
        self.all_models_table.enable_bindings()
        self.all_models_table.place(x=660, y=120)

        Label(
            self, text='Model Ranking:', font='Arial 12 bold',
            fg='white', bg=colors.fundo
        ).place(x=1580, y=90)

        ranking_data = []
        x_labels = []
        y_values = []
        for i, model in enumerate(model_ranking):
            model_name = model[0]
            error_value = round(float(model[1].replace(',', '.')), 4)
            ranking_data.append([model_name, error_value])

            if i <= 15:
                x_labels.append(str(model_name))
                y_values.append(error_value)

        self.ranking_table = Sheet(
            self, data=ranking_data,
            headers=['Model', 'Error'],
            width=270, height=500, column_width=115
        )
        self.ranking_table.enable_bindings()
        self.ranking_table.place(x=1580, y=120)

        figure = Figure(figsize=(12, 3.3), dpi=100)
        plot = figure.add_subplot(1, 1, 1)

        plot.bar(x_labels, y_values)
        plot.set_ylabel('Error (%)')
        plot.set_xlabel('Models')
        plot.grid(True)

        canvas = FigureCanvasTkAgg(figure, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()
        canvas.get_tk_widget().place(x=660, y=650)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.place(x=1150, y=10)
        toolbar.update()

     
