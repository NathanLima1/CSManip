import tkinter as tk
from tkinter import ttk
from tkinter import Canvas, LabelFrame, Label, Entry, StringVar, BooleanVar, IntVar, Scale, Button, Checkbutton, HORIZONTAL, CENTER

fundo = '#4F4F4F' #? Cor de fundo da tela
fun_b = '#3CB371' #? Cor de fundo dos botoes
fun_ap = '#9C444C'
fun_alt = '#C99418'
fun_meta_le = '#191970'

def create_training_widgets(self, y_base=520):
    self.data_s = StringVar()
    self.data_s.set('Target city')
    lista_dt = ['Target city', 'Neighbor A', 'Neighbor B', 'Neighbor C']
    Label(self, text="Dados para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=y_base)
    ttk.Combobox(self, values=lista_dt, textvariable=self.data_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=y_base + 25)

    self.ind_s = StringVar()
    self.ind_s.set('Temperatura máxima')
    lista_ind = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
    Label(self, text='Indicador:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=y_base)
    ttk.Combobox(self, values=lista_ind, textvariable=self.ind_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=y_base + 25)

    self.por_trei = IntVar()
    self.por_trei.set(70)
    Label(self, text="Porção para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=y_base + 60)
    Scale(self, variable=self.por_trei, orient=HORIZONTAL, length=240).place(x=50, y=y_base + 85)

    self.num_teste = IntVar()
    self.num_teste.set(5)

    Label(self, text="Número de testes (int):", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=y_base + 60)
    self.ent_num_teste = Entry(self, textvariable=self.num_teste, width=27, font='Arial 12', justify=CENTER).place(x=340, y=y_base + 85)