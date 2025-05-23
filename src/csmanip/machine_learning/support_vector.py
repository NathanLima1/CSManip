from machine_learning.utils import *

def generate_param(self):
    w = Canvas(self, width=615, height=900, background=fundo, border=0)
    w.place(x=10, y=95)
    self.lbf_para_nn = LabelFrame(self, text='Parâmetros', width=600, height=385,
                                   font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=100)

    self.kernel_v = StringVar()
    lista_ker = ['linear', 'poly', 'rbf', 'sigmoid']
    self.kernel_v.set('rbf')
    Label(self, text='Kernel:', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=120)
    ttk.Combobox(self, values=lista_ker, textvariable=self.kernel_v, width=25,
                  font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=145)

    self.degree_v = IntVar()
    self.degree_v.set(3)
    Label(self, text='Degree (int):', font='Arial 12 bold',
           fg='white', bg=fundo).place(x=340, y=120)
    Entry(self, textvariable=self.degree_v, font='Arial 12',
           width=27, justify=CENTER).place(x=340, y=145)

    self.gamma_v = StringVar()
    self.gamma_v.set('scale')
    Label(self, text='Gamma ("scale", "auto", float):',
           font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=180)
    Entry(self, textvariable=self.gamma_v, font='Arial 12', width=27,
           justify=CENTER).place(x=50, y=205)

    self.coef0_v = StringVar()
    self.coef0_v.set('0.0')
    Label(self, text='Coef0 (float):', font='Arial 12 bold',
           fg='white', bg=fundo).place(x=340, y=180)
    Entry(self, textvariable=self.coef0_v, font='Arial 12',
           width=27, justify=CENTER).place(x=340, y=205)

    self.tol_v = StringVar()
    self.tol_v.set('0.001')
    Label(self, text='Tol (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=240)
    Entry(self, textvariable=self.tol_v, font='Arial 12',
           width=27, justify=CENTER).place(x=50, y=265)

    self.c_v = StringVar()
    self.c_v.set('1.0')
    Label(self, text='C (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=240)
    Entry(self, textvariable=self.c_v, font='Arial 12',
           width=27, justify=CENTER).place(x=340, y=265)

    self.epsilon_v = StringVar()
    self.epsilon_v.set('0.1')
    Label(self, text='Epsilon (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=300)
    Entry(self, textvariable=self.epsilon_v, font='Arial 12',
           width=27, justify=CENTER).place(x=50, y=325)

    self.shrinking_v = BooleanVar()
    self.shrinking_v.set(True)
    Label(self, text='Shrinking (Bool):', font='Arial 12 bold',
           fg='white', bg=fundo).place(x=340, y=300)
    Entry(self, textvariable=self.shrinking_v, font='Arial 12',
           width=27, justify=CENTER).place(x=340, y=325)

    self.cache_size_v = StringVar()
    self.cache_size_v.set('200')
    Label(self, text='Cache_size (float):', font='Arial 12 bold',
           fg='white', bg=fundo).place(x=50, y=360)
    Entry(self, textvariable=self.cache_size_v, font='Arial 12',
           width=27, justify=CENTER).place(x=50, y=385)   

    self.verbose_v = BooleanVar()
    self.verbose_v.set(False)
    Label(self, text='Verbose (Bool):', font='Arial 12 bold',
           fg='white', bg=fundo).place(x=340, y=360)
    Entry(self, textvariable=self.verbose_v, font='Arial 12',
           width=27, justify=CENTER).place(x=340, y=385)

    self.maxiter_v = IntVar()
    self.maxiter_v.set(-1)
    Label(self, text='Max_iter (int):', font='Arial 12 bold',
           fg='white', bg=fundo).place(x=50, y=420)
    Entry(self, textvariable=self.maxiter_v, font='Arial 12',
           width=27, justify=CENTER).place(x=50, y=445)

    self.lbf_dt_nn = LabelFrame(self, text='Dados', width=600, height=170,
                                 font='Arial 12 bold', fg ='white', bg=fundo).place(x=20, y=500)

    create_training_widgets(self)

    Button(self, text='Preview', font='Arial 11 bold', fg='white', bg=fun_b,
            width=25, command=self.gerar_preview_svm).place(x=50, y=680)
    self.save_model = IntVar()
    Checkbutton(self, text='Salvar modelo', variable=self.save_model, bg=fundo,
                 font='Arial 12 bold', activebackground=fundo).place(x=340, y=680)