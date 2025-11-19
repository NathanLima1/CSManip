import tkinter as tk
from tkinter import ttk, messagebox as msg
import threading

class OptunaStartPopup(tk.Toplevel):
    """
    Janela popup para o usuário poder escolher o número de tentativas que
    o optuna realizará.
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.title(controller.i18n.get('number_trials_title'))
        self.geometry("600x400")

        self.grab_set()
        self.transient(parent)

        i18n = self.controller.i18n