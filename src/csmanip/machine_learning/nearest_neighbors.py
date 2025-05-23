from machine_learning.utils import *
from machine_learning.gui_helpers import NNeighParameterFrame

def generate_param(self):
    Canvas(self, width=615, height=900, background=fundo, border=0).place(x=10, y=95)
    self.param = NNeighParameterFrame(self, fundo)

    create_training_widgets(self, 340)
    
    Button(self, text='Preview', font='Arial 11 bold', fg='white', bg=fun_b, width=25, command=self.gerar_preview_Kn).place(x=50, y=505)
    self.save_model = IntVar()
    Checkbutton(self, text='Salvar modelo', variable=self.save_model, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=340, y=505) 
