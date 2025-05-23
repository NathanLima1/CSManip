"""Module for the machine learning interface using Tkinter.

This module creates a window with options for selecting different 
Machine Learning algorithms and integrates functionalities such as
parameter selection, data preview, and result visualization.
"""

from tkinter import Toplevel
from machine_learning.view import View
from machine_learning.utils import *
from machine_learning.gui_helpers import *
from data_processing.data_processing import DataProcessing

class MachineLearning(Toplevel):
    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)
        self.title('Aprendizado de máquina')
        self.geometry('800x800')
        self.configure(background=fundo)

        Label(self, text='APRENDIZADO DE MÁQUINA', font='Arial 14 bold',
               fg='white', bg=fundo).place(x=200, y=20)

        self.ml_selected = StringVar()
        self.ml_selected.set('Decision Trees')
        lista_ml = ['Decision Trees',
                     'Neural network',
                     'Nearest Neighbors',
                     'Support Vector',
                     'Gaussian Process']
        
        combo = ttk.Combobox(self, values=lista_ml, textvariable=self.ml_selected,
                              width=28, font='Arial 12', justify=CENTER, state='readonly')
        combo.place(x=20, y=60)
        Button(self, text='Escolher Machine Learning', font='Arial 11 bold',
                fg='white', bg=fun_ap, width=30, command=self.generate_param).place(x=340, y=59)

    def int_float(self, value):
        """
        Try to return a int value, if it can't, returns a float value
        """
        try:
            return int(value)
        except:
            return float(value)

    def valid_maxf(self, value):
        """
        Returnes the correct type of a received value
        """
        if value.isdigit() == True:
            value = int(value)
        elif value.isalnum() == True and value.isdigit() == False:
            value = str(value)
        elif value.isalnum() == False and value.isdigit() == False and value.isalpha() == False:
            value = float(value)

        return value

    def save_parameter(self):
        v = View
        return v.save_parameter()

    def data_preview(self, score, mean_abs_error, mean_rel_error, max_abs_error, exact_max,
                     pred_max, min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis):
        v = View()
        v.data_preview(self, score, mean_abs_error, mean_rel_error, max_abs_error, exact_max,
                       pred_max, min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis)

    def get_end(self, city):
        treatment = DataProcessing()
        return treatment.get_file_path(city)

    def generate_preview_dt(self):
        v = View()
        v.generate_preview_dt(self)

    def generate_preview_nn(self):
        v = View()
        v.generate_preview_nn(self)

    def generate_preview_svm(self):
        v = View()
        v.generate_preview_svm(self)

    def generate_preview_kn(self):
        v = View()
        v.generate_preview_kn(self)

    def generate_param(self):
        opcao = self.ml_selected.get()
        if opcao == 'Decision Trees':
            Canvas(self, width=615, height=900, background=fundo, border=0).place(x=10, y=95)
            self.param_frame = DTParameterFrame(self, fundo, fun_alt)
            
            self.data_s = StringVar()
            self.data_s.set('Cidade alvo')
            lista_dt = ['Cidade alvo', 'Vizinha A', 'Vizinha B', 'Vizinha C']
            Label(self, text="Dados para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=520)
            self.combo_c = ttk.Combobox(self, values=lista_dt, textvariable=self.data_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=545)

            self.ind_s = StringVar()
            self.ind_s.set('Temperatura máxima')
            lista_ind = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
            Label(self, text='Indicador:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=520)
            ttk.Combobox(self, values=lista_ind, textvariable=self.ind_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=545)

            self.por_trei = IntVar()
            self.por_trei.set(70)
            Label(self, text="Porção para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=580)
            Scale(self, variable=self.por_trei, orient=HORIZONTAL, length=240).place(x=50, y=605)
        
            self.num_teste = IntVar()
            self.num_teste.set(5)
            Label(self, text="Número de testes (int):", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=580)
            self.ent_num_teste = Entry(self, textvariable=self.num_teste, width=27, font='Arial 12', justify=CENTER).place(x=340, y=605)
           
            Button(self, text='Preview', font='Arial 11 bold', fg='white', bg=fun_b, width=25, command=self.generate_preview_dt).place(x=50, y=685)
            #Button(self, text='Salvar Paramt.', font='Arial 11 bold', fg='white', bg=fun_b, width=25, command=self.salvar_paramt).place(x=340, y=685)
            self.save_model = IntVar()
            Checkbutton(self, text='Salvar modelo', variable=self.save_model, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=340, y=685)
        elif opcao == 'Neural network':
            Canvas(self, width=615, height=900, background=fundo, border=0).place(x=10, y=95)
            self.param_frame = NNParameterFrame(self, fundo)
            self.data_s = StringVar()
            self.data_s.set('Cidade alvo')
            lista_dt = ['Cidade alvo', 'Vizinha A', 'Vizinha B', 'Vizinha C']
            Label(self, text="Dados para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=750)
            self.combo_c = ttk.Combobox(self, values=lista_dt, textvariable=self.data_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=775)

            self.ind_s = StringVar()
            self.ind_s.set('Temperatura máxima')
            lista_ind = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
            Label(self, text='Indicador:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=750)
            ttk.Combobox(self, values=lista_ind, textvariable=self.ind_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=775)

            self.por_trei = IntVar()
            self.por_trei.set(70)
            Label(self, text="Porção para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=810)
            Scale(self, variable=self.por_trei, orient=HORIZONTAL, length=240).place(x=50, y=835)
        
            self.num_teste = IntVar()
            self.num_teste.set(5)
            Label(self, text="Número de testes (int):", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=810)
            self.ent_num_teste = Entry(self, textvariable=self.num_teste, width=27, font='Arial 12', justify=CENTER).place(x=340, y=835)

            Button(self, text='Preview', font='Arial 11 bold', fg='white', bg=fun_b, width=25, command=self.generate_preview_nn).place(x=50, y=915)
            self.save_model = IntVar()
            Checkbutton(self, text='Salvar modelo', variable=self.save_model, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=340, y=915)
        elif opcao == 'Nearest Neighbors':
           Canvas(self, width=615, height=900, background=fundo, border=0).place(x=10, y=95)
           self.param_frame = NNeighParameterFrame(self, fundo)

           self.lbf_para_nn = LabelFrame(self, text='Parâmetros', width=600, height=205, font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=100) 

           self.data_s = StringVar()
           self.data_s.set('Cidade alvo')
           lista_dt = ['Cidade alvo', 'Vizinha A', 'Vizinha B', 'Vizinha C']
           Label(self, text="Dados para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=340)
           self.combo_c = ttk.Combobox(self, values=lista_dt, textvariable=self.data_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=365)

           self.ind_s = StringVar()
           self.ind_s.set('Temperatura máxima')
           lista_ind = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
           Label(self, text='Indicador:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=340)
           ttk.Combobox(self, values=lista_ind, textvariable=self.ind_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=365)

           self.por_trei = IntVar()
           self.por_trei.set(70)
           Label(self, text="Porção para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=400)
           Scale(self, variable=self.por_trei, orient=HORIZONTAL, length=240).place(x=50, y=425)

           self.num_teste = IntVar()
           self.num_teste.set(5)
           Label(self, text="Número de testes (int):", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=400)
           self.ent_num_teste = Entry(self, textvariable=self.num_teste, width=27, font='Arial 12', justify=CENTER).place(x=340, y=425)

           Button(self, text='Preview', font='Arial 11 bold', fg='white', bg=fun_b, width=25, command=self.generate_preview_kn).place(x=50, y=505)
           self.save_model = IntVar()
           Checkbutton(self, text='Salvar modelo', variable=self.save_model, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=340, y=505) 
        elif opcao == 'Support Vector':
            w = Canvas(self, width=615, height=900, background=fundo, border=0)
            w.place(x=10, y=95)
            self.lbf_para_nn = LabelFrame(self, text='Parâmetros', width=600, height=385, font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=100)
            
            self.kernel_v = StringVar()
            lista_ker = ['linear', 'poly', 'rbf', 'sigmoid']
            self.kernel_v.set('rbf')
            Label(self, text='Kernel:', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=120)
            ttk.Combobox(self, values=lista_ker, textvariable=self.kernel_v, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=145)

            self.degree_v = IntVar()
            self.degree_v.set(3)
            Label(self, text='Degree (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=120)
            Entry(self, textvariable=self.degree_v, font='Arial 12', width=27, justify=CENTER).place(x=340, y=145) 

            self.gamma_v = StringVar()
            self.gamma_v.set('scale')
            Label(self, text='Gamma ("scale", "auto", float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=180)
            Entry(self, textvariable=self.gamma_v, font='Arial 12', width=27, justify=CENTER).place(x=50, y=205)

            self.coef0_v = StringVar()
            self.coef0_v.set('0.0')
            Label(self, text='Coef0 (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=180)
            Entry(self, textvariable=self.coef0_v, font='Arial 12', width=27, justify=CENTER).place(x=340, y=205)

            self.tol_v = StringVar()
            self.tol_v.set('0.001')
            Label(self, text='Tol (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=240)
            Entry(self, textvariable=self.tol_v, font='Arial 12', width=27, justify=CENTER).place(x=50, y=265)

            self.c_v = StringVar()
            self.c_v.set('1.0')
            Label(self, text='C (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=240)
            Entry(self, textvariable=self.c_v, font='Arial 12', width=27, justify=CENTER).place(x=340, y=265)

            self.epsilon_v = StringVar()
            self.epsilon_v.set('0.1')
            Label(self, text='Epsilon (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=300)
            Entry(self, textvariable=self.epsilon_v, font='Arial 12', width=27, justify=CENTER).place(x=50, y=325)   

            self.shrinking_v = BooleanVar()
            self.shrinking_v.set(True)
            Label(self, text='Shrinking (Bool):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=300)
            Entry(self, textvariable=self.shrinking_v, font='Arial 12', width=27, justify=CENTER).place(x=340, y=325)

            self.cache_size_v = StringVar()
            self.cache_size_v.set('200')
            Label(self, text='Cache_size (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=360)
            Entry(self, textvariable=self.cache_size_v, font='Arial 12', width=27, justify=CENTER).place(x=50, y=385)   

            self.verbose_v = BooleanVar()
            self.verbose_v.set(False)
            Label(self, text='Verbose (Bool):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=360)
            Entry(self, textvariable=self.verbose_v, font='Arial 12', width=27, justify=CENTER).place(x=340, y=385)

            self.maxiter_v = IntVar()
            self.maxiter_v.set(-1)
            Label(self, text='Max_iter (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=420)
            Entry(self, textvariable=self.maxiter_v, font='Arial 12', width=27, justify=CENTER).place(x=50, y=445)

            self.lbf_dt_nn = LabelFrame(self, text='Dados', width=600, height=170, font='Arial 12 bold', fg ='white', bg=fundo).place(x=20, y=500)

            self.data_s = StringVar()
            self.data_s.set('Cidade alvo')
            lista_dt = ['Cidade alvo', 'Vizinha A', 'Vizinha B', 'Vizinha C']
            Label(self, text="Dados para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=520)
            self.combo_c = ttk.Combobox(self, values=lista_dt, textvariable=self.data_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=545)

            self.ind_s = StringVar()
            self.ind_s.set('Temperatura máxima')
            lista_ind = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
            Label(self, text='Indicador:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=520)
            ttk.Combobox(self, values=lista_ind, textvariable=self.ind_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=545)

            self.por_trei = IntVar()
            self.por_trei.set(70)
            Label(self, text="Porção para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=580)
            Scale(self, variable=self.por_trei, orient=HORIZONTAL, length=240).place(x=50, y=605)
        
            self.num_teste = IntVar()
            self.num_teste.set(5)
            Label(self, text="Número de testes (int):", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=580)
            self.ent_num_teste = Entry(self, textvariable=self.num_teste, width=27, font='Arial 12', justify=CENTER).place(x=340, y=605)

            Button(self, text='Preview', font='Arial 11 bold', fg='white', bg=fun_b, width=25, command=self.generate_preview_svm).place(x=50, y=680)
            self.save_model = IntVar()
            Checkbutton(self, text='Salvar modelo', variable=self.save_model, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=340, y=680)
        elif opcao == 'Gaussian Process':
            w = Canvas(self, width=615, height=900, background=fundo, border=0)
            w.place(x=10, y=95)
            self.param_frame = GPParameterFrame(self, fundo)
            
            self.data_s = StringVar()
            self.data_s.set('Cidade alvo')
            lista_dt = ['Cidade alvo', 'Vizinha A', 'Vizinha B', 'Vizinha C']
            Label(self, text="Dados para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=340)
            self.combo_c = ttk.Combobox(self, values=lista_dt, textvariable=self.data_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=365)

            self.ind_s = StringVar()
            self.ind_s.set('Temperatura máxima')
            lista_ind = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
            Label(self, text='Indicador:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=340)
            ttk.Combobox(self, values=lista_ind, textvariable=self.ind_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=365)

            self.por_trei = IntVar()
            self.por_trei.set(70)
            Label(self, text="Porção para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=400)
            Scale(self, variable=self.por_trei, orient=HORIZONTAL, length=240).place(x=50, y=425)
        
            self.num_teste = IntVar()
            self.num_teste.set(5)
            Label(self, text="Número de testes (int):", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=400)
            self.ent_num_teste = Entry(self, textvariable=self.num_teste, width=27, font='Arial 12', justify=CENTER).place(x=340, y=425)

            Button(self, text='Preview', font='Arial 11 bold', fg='white', bg=fun_b, width=25, command=self.generate_preview_svm).place(x=50, y=505)
            self.save_model = IntVar()
            Checkbutton(self, text='Salvar modelo', variable=self.save_model, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=340, y=505)
