"""Module for the machine learning interface using Tkinter.

This module creates a window with options for selecting different 
Machine Learning algorithms and integrates functionalities such as
parameter selection, data preview, and result visualization.
"""

from data_processing.data_processing import DataProcessing
from tkinter import Toplevel
from machine_learning.view import View
from machine_learning.utils import *

class MachineLearning(Toplevel):
    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)
        self.title('Aprendizado de máquina')
        self.geometry('800x800')
        self.configure(background=fundo)

        label = Label(self, text='APRENDIZADO DE MÁQUINA', font='Arial 14 bold', fg='white', bg=fundo)
        label.place(x=200, y=20)

        self.ml_selected = StringVar()
        self.ml_selected.set('Decision Trees')
        lista_ml = ['Decision Trees', 'Neural network', 'Nearest Neighbors', 'Support Vector', 'Gaussian Process']
        combo = ttk.Combobox(self, values=lista_ml, textvariable=self.ml_selected, width=28, font='Arial 12',
                              justify=CENTER, state='readonly')
        combo.place(x=20, y=60)
        Button(self, text='Escolher Machine Learning', font='Arial 11 bold',
                fg='white', bg=fun_ap, width=30, command=self.gera_param).place(x=340, y=59)

    def int_float(self, value):
        """
        Try to return a int value, if it can't, returns a float value
        """
        try:
            return int(value)
        except:
            return float(value)

    def valid_maxf(self, value):
        """
        Returnes the correct type of a received value
        """
        if value.isdigit() == True:
            value = int(value)
        elif value.isalnum() == True and value.isdigit() == False:
            value = str(value)
        elif value.isalnum() == False and value.isdigit() == False and value.isalpha() == False:
            value = float(value)

        return value

    def save_parameter(self):
        v = View
        return v.save_parameter()

    def data_preview(self, score, mean_abs_error, mean_rel_error, max_abs_error, exact_max,
                     pred_max, min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis):
        v = View()
        v.data_preview(self, score, mean_abs_error, mean_rel_error, max_abs_error, exact_max,
                       pred_max, min_abs_error, exact_min, pred_min, y_exact, y_pred, x_axis)

    def get_end(self, city):
        treatment = DataProcessing()
        return treatment.get_file_path(city)

    def generate_preview_dt(self):
        v = View()
        v.generate_preview_dt(self)

    def generate_preview_nn(self):
        v = View()
        v.generate_preview_nn(self)

    def generate_preview_svm(self):
        v = View()
        v.generate_preview_svm(self)

    def generate_preview_kn(self):
        v = View()
        v.generate_preview_kn(self)
