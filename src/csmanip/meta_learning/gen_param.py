from tkinter import Canvas, Label, LabelFrame, StringVar, IntVar, BooleanVar, Entry, Scale, Checkbutton, Button, HORIZONTAL, CENTER
import tkinter as ttk
from ..styles import colors

def generate_param(self):
    opcao = self.ml_selected.get()
    if opcao == 'Decision Trees':
        w = Canvas(self, width=615, height=900, background=colors.fundo, border=0)
        w.place(x=10, y=95)
        self.lbf_p = LabelFrame(self, text='Parâmetros', width=600, height=395, font='Arial 12 bold', fg ='white', bg=colors.fundo).place(x=20, y=100)

        self.criterion_v = StringVar()
        lista_cri = ["squared_error", "friedman_mse", "absolute_error", "poisson"]
        self.criterion_v.set("squared_error")
        Label(self, text='Criterion:', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=50, y=120)
        ttk.Combobox(self, values=lista_cri, textvariable=self.criterion_v, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=145)

        self.splitter_v = StringVar()
        lista_spl = ["best", "random"]
        self.splitter_v.set("best")
        Label(self, text='Splitter:', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=340, y=120)
        ttk.Combobox(self, values=lista_spl, textvariable=self.splitter_v, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=145)
        

        self.maxd_v = StringVar()
        self.maxd_v.set("10")
        Label(self, text="Max_deph (int):", font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=50, y=180)
        self.ent_maxd = Entry(self, textvariable=self.maxd_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=205)

        self.minsam_s_v = IntVar()
        self.minsam_s_v.set(2)
        Label(self, text="Min_samples_split (int/float (.)):", font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=340, y=180)
        self.minsam_s = Entry(self, textvariable=self.minsam_s_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=205)
        
        self.minsam_l_v = IntVar()
        self.minsam_l_v.set(50)
        Label(self, text="Min_samples_leaf (int/float (.)):", font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=50, y=240)
        self.ent_minsam_l = Entry(self, textvariable=self.minsam_l_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=265)

        self.minweifra_l_v = StringVar()
        self.minweifra_l_v.set("0.0")
        Label(self, text="Min_weight_fraction_leaf (float (.)):", font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=340, y=240)
        self.ent_minweifra_l = Entry(self, textvariable=self.minweifra_l_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=265)
        
        self.maxfeat_v = StringVar()
        self.maxfeat_v.set("auto")
        Label(self, text="Max_features :", font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=50, y=300)
        Label(self, text="Valores para Max_features:", font='Arial 12 bold', fg=colors.fun_alt, bg=colors.fundo).place(x=340, y=300)
        Label(self, text="int / float / 'auto' / 'sqrt' / 'log2'", font='Arial 12 bold', fg=colors.fun_alt, bg=colors.fundo).place(x=340, y=325)
        self.ent_maxfeat_v = Entry(self, textvariable=self.maxfeat_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=325)

        self.maxleaf_n = StringVar()
        self.maxleaf_n.set("10")
        Label(self, text="Max_leaf_nodes (int)", font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=50, y=360)
        self.ent_maxleaf_n = Entry(self, textvariable=self.maxleaf_n, width=27, font='Arial 12', justify=CENTER).place(x=50, y=385)

        self.minimp_dec = StringVar()
        self.minimp_dec.set("0.0")
        Label(self, text="Min_impurity_decrease (float (.))", font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=340, y=360)
        self.ent_minimp_dec = Entry(self, textvariable=self.minimp_dec, width=27, font='Arial 12', justify=CENTER).place(x=340, y=385)

        self.ccp_alp_v = StringVar()
        self.ccp_alp_v.set("0.0")
        Label(self, text="Ccp_alpha (value>0.0 float):", font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=50, y=420)
        self.ent_ccp_alp = Entry(self, textvariable=self.ccp_alp_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=445)

        self.lbf_d = LabelFrame(self, text='Dados', width=600, height=170, font='Arial 12 bold', fg ='white', bg=colors.fundo).place(x=20, y=500)

        self.data_s = StringVar()
        self.data_s.set('Target city')
        lista_dt = ['Target city', 'Neighbor A', 'Neighbor B', 'Neighbor C']
        Label(self, text="Dados para treinamento:", font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=50, y=520)
        self.combo_c = ttk.Combobox(self, values=lista_dt, textvariable=self.data_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=545)

        self.ind_s = StringVar()
        self.ind_s.set('Temperatura máxima')
        lista_ind = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
        Label(self, text='Indicador:', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=340, y=520)
        ttk.Combobox(self, values=lista_ind, textvariable=self.ind_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=545)

        self.por_trei = IntVar()
        self.por_trei.set(70)
        Label(self, text="Porção para treinamento:", font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=50, y=580)
        Scale(self, variable=self.por_trei, orient=HORIZONTAL, length=240).place(x=50, y=605)
    
        self.num_teste = IntVar()
        self.num_teste.set(5)
        Label(self, text="Número de testes (int):", font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=340, y=580)
        self.ent_num_teste = Entry(self, textvariable=self.num_teste, width=27, font='Arial 12', justify=CENTER).place(x=340, y=605)

        
        Button(self, text='Preview', font='Arial 11 bold', fg='white', bg=colors.fun_b, width=25, command=self.gerar_preview_dt).place(x=50, y=685)
        #Button(self, text='Salvar Paramt.', font='Arial 11 bold', fg='white', bg=colors.fun_b, width=25, command=self.salvar_paramt).place(x=340, y=685)
        self.save_model = IntVar()
        Checkbutton(self, text='Salvar modelo', variable=self.save_model, bg=colors.fundo, font='Arial 12 bold', activebackground=colors.fundo).place(x=340, y=685)
    elif opcao == 'Neural network':
        w = Canvas(self, width=615, height=900, background=colors.fundo, border=0)
        w.place(x=10, y=95)
        self.lbf_para_nn = LabelFrame(self, text='Parâmetros', width=600, height=625, font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=20, y=100)

        self.activation_v = StringVar()
        lista_act = ['identity', 'logistic', 'tanh', 'relu']
        self.activation_v.set('relu')
        Label(self, text='Activation:', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=50, y=120)
        ttk.Combobox(self, values=lista_act, textvariable=self.activation_v, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=145)
        
        self.solver_v = StringVar()
        lista_sol = ['lbfgs', 'sgd', 'adam']
        self.solver_v.set('adam')
        Label(self, text='Solver:', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=340, y=120)
        ttk.Combobox(self, values=lista_sol, textvariable=self.solver_v, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=145)

        self.alpha_v = StringVar()
        self.alpha_v.set('0.0001')
        Label(self, text='Alpha:', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=50, y=180)
        Entry(self, textvariable=self.alpha_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=205)

        self.batch_size_v = StringVar()
        self.batch_size_v.set('auto')
        Label(self, text='Batch_size (int / "auto"):', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=340, y=180)
        Entry(self, textvariable=self.batch_size_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=205)

        self.learning_rate_v = StringVar()
        lista_learn = ['constant', 'invscaling', 'adaptive']
        self.learning_rate_v.set('constant')
        Label(self, text="Learning_rate:", font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=50, y=240)
        ttk.Combobox(self, values=lista_learn, textvariable=self.learning_rate_v, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=265)

        self.learning_rate_init_v = StringVar()
        self.learning_rate_init_v.set('0.001')
        Label(self, text='Learning_rate_init (float):', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=340, y=240)
        Entry(self, textvariable=self.learning_rate_init_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=265)

        self.power_t_v = StringVar()
        self.power_t_v.set('0.5')
        Label(self, text='Power_t (float):', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=50, y=300)
        Entry(self, textvariable=self.power_t_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=325)

        self.max_iter_v = StringVar()
        self.max_iter_v.set('200')
        Label(self, text='Max_iter (int):', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=340, y=300)
        Entry(self, textvariable=self.max_iter_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=325)


        self.shuffle_v = BooleanVar()
        self.shuffle_v.set(True)
        Label(self, text='Shuffle (bool 1/0):', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=50, y=360)
        Entry(self, textvariable=self.shuffle_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=385)

        self.tol_v = StringVar()
        self.tol_v.set('0.0001')
        Label(self, text='Tol (float):', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=340, y=360)
        Entry(self, textvariable=self.tol_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=385)

        self.verbose_v = BooleanVar()
        self.verbose_v.set(False)
        Label(self, text='Verbose (bool 1/0):', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=50, y=420)
        Entry(self, textvariable=self.verbose_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=445)

        self.warm_start_v = BooleanVar()
        self.warm_start_v.set(False)
        Label(self, text='Warm_start (bool 1/0):', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=340, y=420)
        Entry(self, textvariable=self.warm_start_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=445)

        self.momentum_v = StringVar()
        self.momentum_v.set('0.9')
        Label(self, text='Momentum (float):', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=50, y=480)
        Entry(self, textvariable=self.momentum_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=505)

        self.nesterovs_momentum_v = BooleanVar()
        self.nesterovs_momentum_v.set(True)
        Label(self, text='Nesterovs_momentum:', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=340, y=480)
        Entry(self, textvariable=self.nesterovs_momentum_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=505)

        self.early_stopping_v = BooleanVar()
        self.early_stopping_v.set(False)
        Label(self, text='Early_stopping:', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=50, y=540)
        Entry(self, textvariable=self.early_stopping_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=565)

        self.validation_fraction_v = StringVar()
        self.validation_fraction_v.set('0.1')
        Label(self, text='Validation_fraction (float):', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=340, y=540)
        Entry(self, textvariable=self.validation_fraction_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=565)

        self.beta_1_v = StringVar()
        self.beta_1_v.set('0.9')
        Label(self, text='Beta_1 (float):', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=50, y=600)
        Entry(self, textvariable=self.beta_1_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=625)

        self.beta_2_v = StringVar()
        self.beta_2_v.set('0.999')
        Label(self, text='Beta_2 (float):', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=340, y=600)
        Entry(self, textvariable=self.beta_2_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=625)

        self.n_iter_no_change_v = StringVar()
        self.n_iter_no_change_v.set('10')
        Label(self, text='N_iter_no_change (int):', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=50, y=660)
        Entry(self, textvariable=self.n_iter_no_change_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=685)

        self.max_fun_v = StringVar()
        self.max_fun_v.set('15000')
        Label(self, text='max_fun (int):', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=340, y=660)
        Entry(self, textvariable=self.max_fun_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=685)

        '''   data   '''
        self.lbf_dt_nn = LabelFrame(self, text='Dados', width=600, height=170, font='Arial 12 bold', fg ='white', bg=colors.fundo).place(x=20, y=730)

        self.data_s = StringVar()
        self.data_s.set('Target city')
        lista_dt = ['Target city', 'Neighbor A', 'Neighbor B', 'Neighbor C']
        Label(self, text="Dados para treinamento:", font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=50, y=750)
        self.combo_c = ttk.Combobox(self, values=lista_dt, textvariable=self.data_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=775)

        self.ind_s = StringVar()
        self.ind_s.set('Temperatura máxima')
        lista_ind = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
        Label(self, text='Indicador:', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=340, y=750)
        ttk.Combobox(self, values=lista_ind, textvariable=self.ind_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=775)

        self.por_trei = IntVar()
        self.por_trei.set(70)
        Label(self, text="Porção para treinamento:", font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=50, y=810)
        Scale(self, variable=self.por_trei, orient=HORIZONTAL, length=240).place(x=50, y=835)
    
        self.num_teste = IntVar()
        self.num_teste.set(5)
        Label(self, text="Número de testes (int):", font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=340, y=810)
        self.ent_num_teste = Entry(self, textvariable=self.num_teste, width=27, font='Arial 12', justify=CENTER).place(x=340, y=835)

        Button(self, text='Preview', font='Arial 11 bold', fg='white', bg=colors.fun_b, width=25, command=self.gerar_preview_nn).place(x=50, y=915)
        self.save_model = IntVar()
        Checkbutton(self, text='Salvar modelo', variable=self.save_model, bg=colors.fundo, font='Arial 12 bold', activebackground=colors.fundo).place(x=340, y=915)
    elif opcao == 'Nearest Neighbors':

        w = Canvas(self, width=615, height=900, background=colors.fundo, border=0)
        w.place(x=10, y=95)
        

        self.lbf_para_nn = LabelFrame(self, text='Parâmetros', width=600, height=205, font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=20, y=100) 

        self.n_neighbors_v = IntVar()
        self.n_neighbors_v.set(5)
        Label(self, text='N_neighbors (int):', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=50, y=120)
        Entry(self, textvariable=self.n_neighbors_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=145)

        self.algorithm_v = StringVar()
        lista_alg = ['auto', 'ball_tree', 'kd_tree', 'brute']
        self.algorithm_v.set('auto')
        Label(self, text='Algorithm:', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=340, y=120)
        ttk.Combobox(self, values=lista_alg, textvariable=self.algorithm_v, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=145)

        self.leaf_size_v = IntVar()
        self.leaf_size_v.set(30)
        Label(self, text='Leaf_size (int):', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=50, y=180)
        Entry(self, textvariable=self.leaf_size_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=205)

        self.p_v = IntVar()
        self.p_v.set(2)
        Label(self, text='P (int):', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=340, y=180)
        Entry(self, textvariable=self.p_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=205)

        self.n_jobs_v = StringVar()
        self.n_jobs_v.set('5')
        Label(self, text='N_jobs (int / "None"):', font='Aria 12 bold', fg='white', bg=colors.fundo).place(x=50, y=240)
        Entry(self, textvariable=self.n_jobs_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=265)

        self.lbf_d = LabelFrame(self, text='Dados', width=600, height=170, font='Arial 12 bold', fg ='white', bg=colors.fundo).place(x=20, y=320)

        self.data_s = StringVar()
        self.data_s.set('Target city')
        lista_dt = ['Target city', 'Neighbor A', 'Neighbor B', 'Neighbor C']
        Label(self, text="Dados para treinamento:", font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=50, y=340)
        self.combo_c = ttk.Combobox(self, values=lista_dt, textvariable=self.data_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=365)

        self.ind_s = StringVar()
        self.ind_s.set('Temperatura máxima')
        lista_ind = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
        Label(self, text='Indicador:', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=340, y=340)
        ttk.Combobox(self, values=lista_ind, textvariable=self.ind_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=365)

        self.por_trei = IntVar()
        self.por_trei.set(70)
        Label(self, text="Porção para treinamento:", font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=50, y=400)
        Scale(self, variable=self.por_trei, orient=HORIZONTAL, length=240).place(x=50, y=425)

        self.num_teste = IntVar()
        self.num_teste.set(5)
        Label(self, text="Número de testes (int):", font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=340, y=400)
        self.ent_num_teste = Entry(self, textvariable=self.num_teste, width=27, font='Arial 12', justify=CENTER).place(x=340, y=425)

        Button(self, text='Preview', font='Arial 11 bold', fg='white', bg=colors.fun_b, width=25, command=self.gerar_preview_Kn).place(x=50, y=505)
        self.save_model = IntVar()
        Checkbutton(self, text='Salvar modelo', variable=self.save_model, bg=colors.fundo, font='Arial 12 bold', activebackground=colors.fundo).place(x=340, y=505) 
    elif opcao == 'Support Vector':
        w = Canvas(self, width=615, height=900, background=colors.fundo, border=0)
        w.place(x=10, y=95)
        self.lbf_para_nn = LabelFrame(self, text='Parâmetros', width=600, height=385, font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=20, y=100)
        
        self.kernel_v = StringVar()
        lista_ker = ['linear', 'poly', 'rbf', 'sigmoid']
        self.kernel_v.set('rbf')
        Label(self, text='Kernel:', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=50, y=120)
        ttk.Combobox(self, values=lista_ker, textvariable=self.kernel_v, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=145)

        self.degree_v = IntVar()
        self.degree_v.set(3)
        Label(self, text='Degree (int):', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=340, y=120)
        Entry(self, textvariable=self.degree_v, font='Arial 12', width=27, justify=CENTER).place(x=340, y=145) 

        self.gamma_v = StringVar()
        self.gamma_v.set('scale')
        Label(self, text='Gamma ("scale", "auto", float):', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=50, y=180)
        Entry(self, textvariable=self.gamma_v, font='Arial 12', width=27, justify=CENTER).place(x=50, y=205)

        self.coef0_v = StringVar()
        self.coef0_v.set('0.0')
        Label(self, text='Coef0 (float):', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=340, y=180)
        Entry(self, textvariable=self.coef0_v, font='Arial 12', width=27, justify=CENTER).place(x=340, y=205)

        self.tol_v = StringVar()
        self.tol_v.set('0.001')
        Label(self, text='Tol (float):', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=50, y=240)
        Entry(self, textvariable=self.tol_v, font='Arial 12', width=27, justify=CENTER).place(x=50, y=265)

        self.c_v = StringVar()
        self.c_v.set('1.0')
        Label(self, text='C (float):', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=340, y=240)
        Entry(self, textvariable=self.c_v, font='Arial 12', width=27, justify=CENTER).place(x=340, y=265)

        self.epsilon_v = StringVar()
        self.epsilon_v.set('0.1')
        Label(self, text='Epsilon (float):', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=50, y=300)
        Entry(self, textvariable=self.epsilon_v, font='Arial 12', width=27, justify=CENTER).place(x=50, y=325)   

        self.shrinking_v = BooleanVar()
        self.shrinking_v.set(True)
        Label(self, text='Shrinking (Bool):', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=340, y=300)
        Entry(self, textvariable=self.shrinking_v, font='Arial 12', width=27, justify=CENTER).place(x=340, y=325)

        self.cache_size_v = StringVar()
        self.cache_size_v.set('200')
        Label(self, text='Cache_size (float):', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=50, y=360)
        Entry(self, textvariable=self.cache_size_v, font='Arial 12', width=27, justify=CENTER).place(x=50, y=385)   

        self.verbose_v = BooleanVar()
        self.verbose_v.set(False)
        Label(self, text='Verbose (Bool):', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=340, y=360)
        Entry(self, textvariable=self.verbose_v, font='Arial 12', width=27, justify=CENTER).place(x=340, y=385)

        self.maxiter_v = IntVar()
        self.maxiter_v.set(-1)
        Label(self, text='Max_iter (int):', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=50, y=420)
        Entry(self, textvariable=self.maxiter_v, font='Arial 12', width=27, justify=CENTER).place(x=50, y=445)

        self.lbf_dt_nn = LabelFrame(self, text='Dados', width=600, height=170, font='Arial 12 bold', fg ='white', bg=colors.fundo).place(x=20, y=500)

        self.data_s = StringVar()
        self.data_s.set('Target city')
        lista_dt = ['Target city', 'Neighbor A', 'Neighbor B', 'Neighbor C']
        Label(self, text="Dados para treinamento:", font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=50, y=520)
        self.combo_c = ttk.Combobox(self, values=lista_dt, textvariable=self.data_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=545)

        self.ind_s = StringVar()
        self.ind_s.set('Temperatura máxima')
        lista_ind = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
        Label(self, text='Indicador:', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=340, y=520)
        ttk.Combobox(self, values=lista_ind, textvariable=self.ind_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=545)

        self.por_trei = IntVar()
        self.por_trei.set(70)
        Label(self, text="Porção para treinamento:", font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=50, y=580)
        Scale(self, variable=self.por_trei, orient=HORIZONTAL, length=240).place(x=50, y=605)
    
        self.num_teste = IntVar()
        self.num_teste.set(5)
        Label(self, text="Número de testes (int):", font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=340, y=580)
        self.ent_num_teste = Entry(self, textvariable=self.num_teste, width=27, font='Arial 12', justify=CENTER).place(x=340, y=605)

        Button(self, text='Preview', font='Arial 11 bold', fg='white', bg=colors.fun_b, width=25, command=self.gerar_preview_svm).place(x=50, y=680)
        self.save_model = IntVar()
        Checkbutton(self, text='Salvar modelo', variable=self.save_model, bg=colors.fundo, font='Arial 12 bold', activebackground=colors.fundo).place(x=340, y=680)
    elif opcao == 'Gaussian Process':
        w = Canvas(self, width=615, height=900, background=colors.fundo, border=0)
        w.place(x=10, y=95)
        self.lbf_para_nn = LabelFrame(self, text='Parâmetros', width=600, height=205, font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=20, y=100)
        
        self.alpha_gp = StringVar()
        self.alpha_gp.set('0.0000000001')
        Label(self, text='Alpha (float): ', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=50, y=120)
        Entry(self, textvariable=self.alpha_gp, font='Arial 12', width=27, justify=CENTER).place(x=50, y=145)
        
        self.n_restarts_op = IntVar()
        self.n_restarts_op.set(0)
        Label(self, text='N_restart_optimizer (int):', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=340, y=120)
        Entry(self, textvariable=self.n_restarts_op, font='Arial 12', width=27, justify=CENTER).place(x=340, y=145)

        self.normalize_y_gp = BooleanVar()
        self.normalize_y_gp.set(0)
        Label(self, text='Normalize_y (Bool 1/0):', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=50, y=180)
        Entry(self, textvariable=self.normalize_y_gp, font='Arial 12', width=27, justify=CENTER).place(x=50, y=205)

        self.copy_X_train = BooleanVar()
        self.copy_X_train.set(0)
        Label(self, text='Copy_X_train (Bool 1/0):', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=340, y=180)
        Entry(self, textvariable=self.copy_X_train, font='Arial 12', width=27, justify=CENTER).place(x=340, y=205)

        self.rand_state_gp = StringVar()
        self.rand_state_gp.set('None')
        Label(self, text='Random_state ("None" / int):', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=50, y=240)
        Entry(self, textvariable=self.rand_state_gp, font='Arial 12', width=27, justify=CENTER).place(x=50, y=265)
        

        self.lbf_dt_nn = LabelFrame(self, text='Dados', width=600, height=170, font='Arial 12 bold', fg ='white', bg=colors.fundo).place(x=20, y=320)

        self.data_s = StringVar()
        self.data_s.set('Target city')
        lista_dt = ['Target city', 'Neighbor A', 'Neighbor B', 'Neighbor C']
        Label(self, text="Dados para treinamento:", font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=50, y=340)
        self.combo_c = ttk.Combobox(self, values=lista_dt, textvariable=self.data_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=365)

        self.ind_s = StringVar()
        self.ind_s.set('Temperatura máxima')
        lista_ind = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
        Label(self, text='Indicador:', font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=340, y=340)
        ttk.Combobox(self, values=lista_ind, textvariable=self.ind_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=365)

        self.por_trei = IntVar()
        self.por_trei.set(70)
        Label(self, text="Porção para treinamento:", font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=50, y=400)
        Scale(self, variable=self.por_trei, orient=HORIZONTAL, length=240).place(x=50, y=425)
    
        self.num_teste = IntVar()
        self.num_teste.set(5)
        Label(self, text="Número de testes (int):", font='Arial 12 bold', fg='white', bg=colors.fundo).place(x=340, y=400)
        self.ent_num_teste = Entry(self, textvariable=self.num_teste, width=27, font='Arial 12', justify=CENTER).place(x=340, y=425)

        Button(self, text='Preview', font='Arial 11 bold', fg='white', bg=colors.fun_b, width=25, command=self.gerar_preview_svm).place(x=50, y=505)
        self.save_model = IntVar()
        Checkbutton(self, text='Salvar modelo', variable=self.save_model, bg=colors.fundo, font='Arial 12 bold', activebackground=colors.fundo).place(x=340, y=505)
