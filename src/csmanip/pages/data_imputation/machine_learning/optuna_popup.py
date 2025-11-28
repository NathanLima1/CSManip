import tkinter as tk
from tkinter import ttk, messagebox as msg
import threading

class OptunaPopup(tk.Toplevel):
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

        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        i18n_num_trials = controller.i18n.get('num_trials_optuna')
        num_trials = tk.Label(tree_frame, "Teste")
        