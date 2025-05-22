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

    create_training_widgets(self, 340)
    
    Button(self, text='Preview', font='Arial 11 bold', fg='white', bg=fun_b, width=25, command=self.gerar_preview_svm).place(x=50, y=505)
    self.save_model = IntVar()
    Checkbutton(self, text='Salvar modelo', variable=self.save_model, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=340, y=505)

