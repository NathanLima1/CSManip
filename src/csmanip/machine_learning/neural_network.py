from machine_learning.utils import *
from machine_learning.gui_helpers import NNParameterFrame

def generate_param(self):
    self.param_frame = NNParameterFrame(self, fundo)
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


    