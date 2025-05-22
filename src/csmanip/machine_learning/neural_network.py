from machine_learning.utils import *

def generate_param(self):
    w = Canvas(self, width=615, height=900, background=fundo, border=0)
    w.place(x=10, y=95)
    self.lbf_para_nn = LabelFrame(self, text='Parâmetros', width=600, height=625, font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=100)

    self.activation_v = StringVar()
    lista_act = ['identity', 'logistic', 'tanh', 'relu']
    self.activation_v.set('relu')
    Label(self, text='Activation:', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=120)
    ttk.Combobox(self, values=lista_act, textvariable=self.activation_v, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=145)
    
    self.solver_v = StringVar()
    lista_sol = ['lbfgs', 'sgd', 'adam']
    self.solver_v.set('adam')
    Label(self, text='Solver:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=120)
    ttk.Combobox(self, values=lista_sol, textvariable=self.solver_v, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=145)

    self.alpha_v = StringVar()
    self.alpha_v.set('0.0001')
    Label(self, text='Alpha:', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=180)
    Entry(self, textvariable=self.alpha_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=205)

    self.batch_size_v = StringVar()
    self.batch_size_v.set('auto')
    Label(self, text='Batch_size (int / "auto"):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=180)
    Entry(self, textvariable=self.batch_size_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=205)

    self.learning_rate_v = StringVar()
    lista_learn = ['constant', 'invscaling', 'adaptive']
    self.learning_rate_v.set('constant')
    Label(self, text="Learning_rate:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=240)
    ttk.Combobox(self, values=lista_learn, textvariable=self.learning_rate_v, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=265)

    self.learning_rate_init_v = StringVar()
    self.learning_rate_init_v.set('0.001')
    Label(self, text='Learning_rate_init (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=240)
    Entry(self, textvariable=self.learning_rate_init_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=265)

    self.power_t_v = StringVar()
    self.power_t_v.set('0.5')
    Label(self, text='Power_t (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=300)
    Entry(self, textvariable=self.power_t_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=325)

    self.max_iter_v = StringVar()
    self.max_iter_v.set('200')
    Label(self, text='Max_iter (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=300)
    Entry(self, textvariable=self.max_iter_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=325)


    self.shuffle_v = BooleanVar()
    self.shuffle_v.set(True)
    Label(self, text='Shuffle (bool 1/0):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=360)
    Entry(self, textvariable=self.shuffle_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=385)

    self.tol_v = StringVar()
    self.tol_v.set('0.0001')
    Label(self, text='Tol (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=360)
    Entry(self, textvariable=self.tol_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=385)

    self.verbose_v = BooleanVar()
    self.verbose_v.set(False)
    Label(self, text='Verbose (bool 1/0):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=420)
    Entry(self, textvariable=self.verbose_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=445)

    self.warm_start_v = BooleanVar()
    self.warm_start_v.set(False)
    Label(self, text='Warm_start (bool 1/0):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=420)
    Entry(self, textvariable=self.warm_start_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=445)

    self.momentum_v = StringVar()
    self.momentum_v.set('0.9')
    Label(self, text='Momentum (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=480)
    Entry(self, textvariable=self.momentum_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=505)

    self.nesterovs_momentum_v = BooleanVar()
    self.nesterovs_momentum_v.set(True)
    Label(self, text='Nesterovs_momentum:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=480)
    Entry(self, textvariable=self.nesterovs_momentum_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=505)

    self.early_stopping_v = BooleanVar()
    self.early_stopping_v.set(False)
    Label(self, text='Early_stopping:', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=540)
    Entry(self, textvariable=self.early_stopping_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=565)

    self.validation_fraction_v = StringVar()
    self.validation_fraction_v.set('0.1')
    Label(self, text='Validation_fraction (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=540)
    Entry(self, textvariable=self.validation_fraction_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=565)

    self.beta_1_v = StringVar()
    self.beta_1_v.set('0.9')
    Label(self, text='Beta_1 (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=600)
    Entry(self, textvariable=self.beta_1_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=625)

    self.beta_2_v = StringVar()
    self.beta_2_v.set('0.999')
    Label(self, text='Beta_2 (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=600)
    Entry(self, textvariable=self.beta_2_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=625)

    self.n_iter_no_change_v = StringVar()
    self.n_iter_no_change_v.set('10')
    Label(self, text='N_iter_no_change (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=660)
    Entry(self, textvariable=self.n_iter_no_change_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=685)

    self.max_fun_v = StringVar()
    self.max_fun_v.set('15000')
    Label(self, text='max_fun (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=660)
    Entry(self, textvariable=self.max_fun_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=685)

    '''   data   '''
    self.lbf_dt_nn = LabelFrame(self, text='Dados', width=600, height=170, font='Arial 12 bold', fg ='white', bg=fundo).place(x=20, y=730)

    self.data_s = StringVar()
    self.data_s.set('Target city')
    lista_dt = ['Target city', 'Neighbor A', 'Neighbor B', 'Neighbor C']
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

    Button(self, text='Preview', font='Arial 11 bold', fg='white', bg=fun_b, width=25, command=self.gerar_preview_nn).place(x=50, y=915)
    self.save_model = IntVar()
    Checkbutton(self, text='Salvar modelo', variable=self.save_model, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=340, y=915)


    