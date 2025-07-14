from .utils import *
from .gui_helpers import BaggingTParameterFrame

def generate_param(self):
    Canvas(self, width=615, height=900, background=fundo, border=0).place(x=10, y=95)
    self.param_frame = BaggingTParameterFrame(self, fundo, fun_alt)
    create_training_widgets(self)
    Button(self, text='Preview', font='Arial 11 bold', fg='white', bg=fun_b, width=25, command=self.generate_preview_bt).place(x=50, y=685)
    self.save_model = IntVar()
    Checkbutton(self, text='Save model', variable=self.save_model, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=340, y=685)