from machine_learning.utils import *

def generate_param(self):
    w = Canvas(self, width=615, height=900, background=fundo, border=0)
    w.place(x=10, y=95)
    self.lbf_p = LabelFrame(self, text='Parâmetros', width=600, height=395, font='Arial 12 bold', fg ='white', bg=fundo).place(x=20, y=100)

    self.criterion_v = StringVar()
    lista_cri = ["squared_error", "friedman_mse", "absolute_error", "poisson"]
    self.criterion_v.set("squared_error")
    Label(self, text='Criterion:', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=120)
    ttk.Combobox(self, values=lista_cri, textvariable=self.criterion_v, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=145)

    self.splitter_v = StringVar()
    lista_spl = ["best", "random"]
    self.splitter_v.set("best")
    Label(self, text='Splitter:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=120)
    ttk.Combobox(self, values=lista_spl, textvariable=self.splitter_v, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=145)
    

    self.maxd_v = StringVar()
    self.maxd_v.set("10")
    Label(self, text="Max_deph (int):", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=180)
    self.ent_maxd = Entry(self, textvariable=self.maxd_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=205)

    self.minsam_s_v = IntVar()
    self.minsam_s_v.set(2)
    Label(self, text="Min_samples_split (int/float (.)):", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=180)
    self.minsam_s = Entry(self, textvariable=self.minsam_s_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=205)
    
    self.minsam_l_v = IntVar()
    self.minsam_l_v.set(50)
    Label(self, text="Min_samples_leaf (int/float (.)):", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=240)
    self.ent_minsam_l = Entry(self, textvariable=self.minsam_l_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=265)

    self.minweifra_l_v = StringVar()
    self.minweifra_l_v.set("0.0")
    Label(self, text="Min_weight_fraction_leaf (float (.)):", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=240)
    self.ent_minweifra_l = Entry(self, textvariable=self.minweifra_l_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=265)
    
    self.maxfeat_v = StringVar()
    self.maxfeat_v.set("auto")
    Label(self, text="Max_features :", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=300)
    Label(self, text="Valores para Max_features:", font='Arial 12 bold', fg=fun_alt, bg=fundo).place(x=340, y=300)
    Label(self, text="int / float / 'auto' / 'sqrt' / 'log2'", font='Arial 12 bold', fg=fun_alt, bg=fundo).place(x=340, y=325)
    self.ent_maxfeat_v = Entry(self, textvariable=self.maxfeat_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=325)

    self.maxleaf_n = StringVar()
    self.maxleaf_n.set("10")
    Label(self, text="Max_leaf_nodes (int)", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=360)
    self.ent_maxleaf_n = Entry(self, textvariable=self.maxleaf_n, width=27, font='Arial 12', justify=CENTER).place(x=50, y=385)

    self.minimp_dec = StringVar()
    self.minimp_dec.set("0.0")
    Label(self, text="Min_impurity_decrease (float (.))", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=360)
    self.ent_minimp_dec = Entry(self, textvariable=self.minimp_dec, width=27, font='Arial 12', justify=CENTER).place(x=340, y=385)

    self.ccp_alp_v = StringVar()
    self.ccp_alp_v.set("0.0")
    Label(self, text="Ccp_alpha (value>0.0 float):", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=420)
    self.ent_ccp_alp = Entry(self, textvariable=self.ccp_alp_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=445)

    self.lbf_d = LabelFrame(self, text='Dados', width=600, height=170, font='Arial 12 bold', fg ='white', bg=fundo).place(x=20, y=500)

    create_training_widgets(self)
    
    Button(self, text='Preview', font='Arial 11 bold', fg='white', bg=fun_b, width=25, command=self.gerar_preview_dt).place(x=50, y=685)
    #Button(self, text='Salvar Paramt.', font='Arial 11 bold', fg='white', bg=fun_b, width=25, command=self.salvar_paramt).place(x=340, y=685)
    self.save_model = IntVar()
    Checkbutton(self, text='Salvar modelo', variable=self.save_model, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=340, y=685)