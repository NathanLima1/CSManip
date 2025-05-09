from machine_learning.utils import *

def generate_param(self):
    w = Canvas(self, width=615, height=900, background=fundo, border=0)
    w.place(x=10, y=95)
    self.lbf_para_nn = LabelFrame(self, text='Parâmetros', width=600, height=205, font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=100)
    
    self.alpha_gp = StringVar()
    self.alpha_gp.set('0.0000000001')
    Label(self, text='Alpha (float): ', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=120)
    Entry(self, textvariable=self.alpha_gp, font='Arial 12', width=27, justify=CENTER).place(x=50, y=145)
    
    self.n_restarts_op = IntVar()
    self.n_restarts_op.set(0)
    Label(self, text='N_restart_optimizer (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=120)
    Entry(self, textvariable=self.n_restarts_op, font='Arial 12', width=27, justify=CENTER).place(x=340, y=145)

    self.normalize_y_gp = BooleanVar()
    self.normalize_y_gp.set(0)
    Label(self, text='Normalize_y (Bool 1/0):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=180)
    Entry(self, textvariable=self.normalize_y_gp, font='Arial 12', width=27, justify=CENTER).place(x=50, y=205)

    self.copy_X_train = BooleanVar()
    self.copy_X_train.set(0)
    Label(self, text='Copy_X_train (Bool 1/0):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=180)
    Entry(self, textvariable=self.copy_X_train, font='Arial 12', width=27, justify=CENTER).place(x=340, y=205)

    self.rand_state_gp = StringVar()
    self.rand_state_gp.set('None')
    Label(self, text='Random_state ("None" / int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=240)
    Entry(self, textvariable=self.rand_state_gp, font='Arial 12', width=27, justify=CENTER).place(x=50, y=265)
    

    self.lbf_dt_nn = LabelFrame(self, text='Dados', width=600, height=170, font='Arial 12 bold', fg ='white', bg=fundo).place(x=20, y=320)

    self.data_s = StringVar()
    self.data_s.set('Target city')
    lista_dt = ['Target city', 'Neighbor A', 'Neighbor B', 'Neighbor C']
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

    Button(self, text='Preview', font='Arial 11 bold', fg='white', bg=fun_b, width=25, command=self.gerar_preview_svm).place(x=50, y=505)
    self.save_model = IntVar()
    Checkbutton(self, text='Salvar modelo', variable=self.save_model, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=340, y=505)

