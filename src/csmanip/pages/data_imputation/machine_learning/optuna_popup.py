import tkinter as tk
from tkinter import ttk

class OptunaPopup(tk.Toplevel):
    """
    Janela popup para o usuário definir o número de tentativas (trials) do Optuna.
    """
    def __init__(self, parent, controller, callback):
        super().__init__(parent)
        self.controller = controller
        self.callback = callback
        i18n = controller.i18n

        self.title(i18n.get('number_trials_title'))
        self.geometry("350x200")
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()

        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        lbl_msg = ttk.Label(
            main_frame, 
            text=i18n.get('num_trials_optuna_msg'),
            wraplength=300
        )
        lbl_msg.pack(pady=(0, 10))

        self.trials_var = tk.StringVar(value="10")
        entry_frame = ttk.Frame(main_frame)
        entry_frame.pack(pady=10)
        
        ttk.Label(entry_frame, text="Nº Trials:").pack(side=tk.LEFT, padx=5)
        self.trials_entry = ttk.Entry(entry_frame, textvariable=self.trials_var, width=10, justify='center')
        self.trials_entry.pack(side=tk.LEFT, padx=5)

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        self.btn_confirm = ttk.Button(
            btn_frame, 
            text=i18n.get('confirm_btn'), 
            command=self._on_confirm
        )
        self.btn_confirm.pack(side=tk.RIGHT, padx=5)

        self.btn_cancel = ttk.Button(
            btn_frame, 
            text=i18n.get('cancel_btn'), 
            command=self.destroy
        )
        self.btn_cancel.pack(side=tk.RIGHT, padx=5)
        
        self._center_window(parent)

    def _center_window(self, parent):
        self.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_rooty() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

    def _on_confirm(self):
        try:
            val = int(self.trials_var.get())
            if val < 1:
                raise ValueError
            
            self.destroy()
            self.callback(val)
            
        except ValueError:
            tk.messagebox.showerror(
                self.controller.i18n.get('error_title'),
                self.controller.i18n.get('invalid_trials_msg')
            )