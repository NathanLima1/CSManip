from ..utils import *
if typing.TYPE_CHECKING:
    from ..start_page import StartPage

class TutorialPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        # --- Widgets ---
        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        self.back_button = ttk.Button(top_frame, text="", command=self.go_to_start_page)
        self.back_button.pack(side=tk.LEFT)

        self.page_title = ttk.Label(top_frame, text="", font=("Verdana", 16, "bold"))
        self.page_title.pack(side=tk.LEFT, expand=True)

        main_container = ttk.Frame(self)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        #... (código para painel esquerdo e direito)
        
        # Inicializa os textos
        self.update_texts()

    def go_to_start_page(self):
        """Importa e navega para a página inicial."""
        from ..start_page import StartPage
        self.controller.show_frame(StartPage)
        
    def update_texts(self):
        """Atualiza os textos APENAS para esta tela."""
        i18n = self.controller.i18n
        self.controller.title(i18n.get('app_main_title'))
        self.back_button.config(text=i18n.get('back_btn'))
        self.page_title.config(text=i18n.get('tutorial_title'))
        # Adicione .config(text=...) para todos os outros widgets desta tela aqui