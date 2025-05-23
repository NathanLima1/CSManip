from machine_learning.utils import *
from machine_learning.gui_helpers import DTParameterFrame

def generate_param(self):
    Canvas(self, width=615, height=900, background=fundo, border=0).place(x=10, y=95)
    self.param_frame = DTParameterFrame(self, fundo, fun_alt)
    create_training_widgets(self)
    
    Button(self, text='Preview', font='Arial 11 bold', fg='white', bg=fun_b, width=25, command=self.gerar_preview_dt).place(x=50, y=685)
    #Button(self, text='Salvar Paramt.', font='Arial 11 bold', fg='white', bg=fun_b, width=25, command=self.salvar_paramt).place(x=340, y=685)
    self.save_model = IntVar()
    Checkbutton(self, text='Salvar modelo', variable=self.save_model, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=340, y=685)