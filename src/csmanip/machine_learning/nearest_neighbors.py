from machine_learning.utils import *

def generate_param(self):
    w = Canvas(self, width=615, height=900, background=fundo, border=0)
    w.place(x=10, y=95)


    self.lbf_para_nn = LabelFrame(self, text='Parâmetros', width=600, height=205, font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=100) 

    self.n_neighbors_v = IntVar()
    self.n_neighbors_v.set(5)
    Label(self, text='N_neighbors (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=120)
    Entry(self, textvariable=self.n_neighbors_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=145)

    self.algorithm_v = StringVar()
    lista_alg = ['auto', 'ball_tree', 'kd_tree', 'brute']
    self.algorithm_v.set('auto')
    Label(self, text='Algorithm:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=120)
    ttk.Combobox(self, values=lista_alg, textvariable=self.algorithm_v, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=145)

    self.leaf_size_v = IntVar()
    self.leaf_size_v.set(30)
    Label(self, text='Leaf_size (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=180)
    Entry(self, textvariable=self.leaf_size_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=205)

    self.p_v = IntVar()
    self.p_v.set(2)
    Label(self, text='P (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=180)
    Entry(self, textvariable=self.p_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=205)

    self.n_jobs_v = StringVar()
    self.n_jobs_v.set('5')
    Label(self, text='N_jobs (int / "None"):', font='Aria 12 bold', fg='white', bg=fundo).place(x=50, y=240)
    Entry(self, textvariable=self.n_jobs_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=265)

    self.lbf_d = LabelFrame(self, text='Dados', width=600, height=170, font='Arial 12 bold', fg ='white', bg=fundo).place(x=20, y=320)

    create_training_widgets(self, 340)
    
    Button(self, text='Preview', font='Arial 11 bold', fg='white', bg=fun_b, width=25, command=self.gerar_preview_Kn).place(x=50, y=505)
    self.save_model = IntVar()
    Checkbutton(self, text='Salvar modelo', variable=self.save_model, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=340, y=505) 
