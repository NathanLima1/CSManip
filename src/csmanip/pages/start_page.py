from .utils import *
from .tooltip import CreateToolTip

if typing.TYPE_CHECKING:
    from .data_imputation.data_imputation_page import DataImputationPage
    from .download.download_page import DownloadDataPage
    from .tutorial.tutorial_page import TutorialPage
    from .trends.trends_page import ClimateTrendsPage

class StartPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        # --- Widgets ---
        self.welcome_label = ttk.Label(self, text="", font=("Verdana", 20, "bold"))
        self.welcome_label.pack(pady=40, padx=10)

        button_frame = ttk.Frame(self)
        button_frame.pack()

        i18n = self.controller.i18n

        self.tutorial_btn = ttk.Button(button_frame, text="", command=self.go_to_tutorial)
        self.tutorial_btn.pack(pady=10, fill=tk.X)
        self.tutorial_tooltip = CreateToolTip(self.tutorial_btn, text=i18n.get('tutorial_home_hint'))

        self.download_btn = ttk.Button(button_frame, text="", command=self.go_to_download)
        self.download_btn.pack(pady=10, fill=tk.X)
        self.download_tooltip = CreateToolTip(self.download_btn, text=i18n.get('download_home_hint'))

        self.imputation_btn = ttk.Button(button_frame, text="", command=self.go_to_data_imputation)
        self.imputation_btn.pack(pady=10, fill=tk.X)
        self.imputation_tooltip = CreateToolTip(self.imputation_btn, text=i18n.get('imputation_home_hint'))

        self.trends_btn = ttk.Button(button_frame, text="", command=self.go_to_trends)
        self.trends_btn.pack(pady=10, fill=tk.X)
        self.trends_tooltip = CreateToolTip(self.trends_btn, text=i18n.get('trends_home_hint'))

        # --- Seletor de Idioma ---
        lang_frame = ttk.Frame(self)
        lang_frame.pack(pady=50)
        self.lang_label = ttk.Label(lang_frame, text="")
        self.lang_label.pack(side=tk.LEFT, padx=5)

        self.lang_combobox = ttk.Combobox(lang_frame, values=list(controller.i18n.available_languages.keys()), state="readonly")
        self.lang_combobox.pack(side=tk.LEFT)
        self.lang_combobox.set("Português (BR)")
        self.lang_combobox.bind("<<ComboboxSelected>>", self.change_language)
        
        # Inicializa os textos
        self.update_texts()

    def go_to_data_imputation(self):
        """Importa e navega para a página de imputação de dados."""
        from .data_imputation.data_imputation_page import DataImputationPage
        self.controller.show_frame(DataImputationPage)

    def go_to_tutorial(self):
        """Importa e navega para a página de tutorial."""
        from .tutorial.tutorial_page import TutorialPage
        self.controller.show_frame(TutorialPage)

    def go_to_download(self):
        """Importa e navega para a página de download de dados."""
        from .download.download_page import DownloadDataPage
        self.controller.show_frame(DownloadDataPage)

    def go_to_trends(self):
        """Importa e navega para a página de tendencias climaticas."""
        from .trends.trends_page import ClimateTrendsPage
        self.controller.show_frame(ClimateTrendsPage)

    def update_texts(self):
        """Atualiza os textos APENAS para esta tela."""
        i18n = self.controller.i18n
        self.welcome_label.config(text=i18n.get('welcome_text'))
        self.tutorial_btn.config(text=i18n.get('tutorial_btn'))
        self.download_btn.config(text=i18n.get('download_data_btn'))
        self.imputation_btn.config(text=i18n.get('data_imputation_btn'))
        self.trends_btn.config(text=i18n.get('climatic_trends_btn'))
        self.lang_label.config(text=i18n.get('language_label'))
        self.tutorial_tooltip.text = i18n.get('tutorial_home_hint')
        self.download_tooltip.text = i18n.get('download_home_hint')
        self.imputation_tooltip.text = i18n.get('imputation_home_hint')
        self.trends_tooltip.text = i18n.get('trends_home_hint')

    def change_language(self, event=None):
        selected_display_name = self.lang_combobox.get()
        lang_code = self.controller.i18n.available_languages[selected_display_name]
        
        self.controller.i18n.set_language(lang_code)
        self.controller.update_all_frames_text()

