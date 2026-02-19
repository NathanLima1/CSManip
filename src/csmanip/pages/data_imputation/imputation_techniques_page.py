from ..utils import *
if typing.TYPE_CHECKING:
    from .data_imputation_page import DataImputationPage
from .triangulation_page import TriangulationPage
from .machine_learning.machine_learning_page import MachineLearningPage
from .meta_learning.meta_learning_page import MetaLearningPage
from ..tooltip import CreateToolTip

class ImputationTechniquesPage(ttk.Frame):
    """Tela para escolher a técnica de imputação."""
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        i18n = controller.i18n

        # --- Frame Superior ---
        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        self.back_button = ttk.Button(top_frame, text="", command=self.go_to_data_imputation)
        self.back_button.pack(side=tk.LEFT)

        self.page_title = ttk.Label(top_frame, text="", font=("Verdana", 16, "bold"))
        self.page_title.pack(side=tk.LEFT, expand=True)

        main_container = ttk.Frame(self)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        main_container.grid_columnconfigure(0, weight=1, minsize=250)
        main_container.grid_columnconfigure(1, weight=3)
        main_container.grid_rowconfigure(0, weight=1)
        
        # --- PAINEL DA ESQUERDA ---
        left_panel = ttk.Frame(main_container)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        self.choose_technique_label = ttk.Label(left_panel, text="", font=("Verdana", 12))
        self.choose_technique_label.pack(anchor="w", pady=(0, 10), padx=5)

        self.triangulation_btn = ttk.Button(left_panel, text="", command=lambda: controller.show_frame(TriangulationPage))
        self.triangulation_btn.pack(fill=tk.X, pady=5)
        self.triangulation_hint = CreateToolTip(self.triangulation_btn, text=i18n.get('triangulation_input_hint'))

        self.machine_learning_btn = ttk.Button(left_panel, text="", command=lambda: controller.show_frame(MachineLearningPage))
        self.machine_learning_btn.pack(fill=tk.X, pady=5)
        self.machine_learning_hint = CreateToolTip(self.machine_learning_btn, text=i18n.get('machine_learning_input_hint'))
        
        self.meta_learning_btn = ttk.Button(left_panel, text="", command=lambda: controller.show_frame(MetaLearningPage))
        self.meta_learning_btn.pack(fill=tk.X, pady=5)
        self.meta_learning_hint = CreateToolTip(self.meta_learning_btn, text=i18n.get('meta_learning_input_hint'))


        # --- PAINEL DA DIREITA ---
        right_panel = ttk.Frame(main_container, relief="solid", borderwidth=1)
        right_panel.grid(row=0, column=1, sticky="nsew")
        
        self.update_texts()

    def go_to_data_imputation(self):
        """Importa e navega para a página inicial."""
        from .data_imputation_page  import DataImputationPage
        self.controller.show_frame(DataImputationPage)
        
    def update_texts(self):
        """Atualiza os textos APENAS para esta tela."""
        i18n = self.controller.i18n
        
        self.back_button.config(text=i18n.get('back_btn'))
        self.page_title.config(text=i18n.get('imputation_techniques_page_title'))
        self.choose_technique_label.config(text=i18n.get('choose_a_technique_label'))
        self.triangulation_btn.config(text=i18n.get('triangulation_btn'))
        self.machine_learning_btn.config(text=i18n.get('machine_learning_btn'))
        self.meta_learning_btn.config(text=i18n.get('meta_learning_btn'))
        self.triangulation_hint.text = i18n.get('triangulation_input_hint')
        self.machine_learning_hint.text = i18n.get('machine_learning_input_hint')
        self.meta_learning_hint.text = i18n.get('meta_learning_input_hint')
