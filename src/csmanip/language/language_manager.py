import json
import os

class LanguageManager:
    def __init__(self):
        self.translations = {}
        self.language_folder = os.path.dirname(os.path.abspath(__file__))
        try:
            self.available_languages = self._load_available_languages()
            self.current_language = None
        except FileNotFoundError:
            raise FileNotFoundError(
                f"A pasta de idiomas '{self.language_folder}' não foi encontrada."
            )

    def _load_available_languages(self):
        """Carrega os códigos de idioma disponíveis baseados nos nomes dos arquivos JSON."""
        langs = {}
        for filename in os.listdir(self.language_folder):
            if filename.endswith('.json'):
                lang_code = filename.split('.')[0]
                lang_map = {"pt_br": "Português (BR)", "en_us": "English (US)", "es_es": "Español (ES)"}
                langs[lang_map.get(lang_code, lang_code)] = lang_code
        return langs
    
    def set_language(self, lang_code):
        """Define o idioma atual e carrega suas traduções"""
        file_path = os.path.join(self.language_folder, f"{lang_code}.json")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.translations = json.load(f)
                self.current_language = lang_code
        except FileNotFoundError:
            print(f"Arquivo de idioma '{lang_code}.json' não encontrado.")
            if self.current_language is None:
                self.set_language("pt_br")

    def get(self, key, **kwargs):
        """Retorna o texto traduzido para uma chave específica"""
        text = self.translations.get(key, key)
        if kwargs:
            try:
                return text.format(**kwargs)
            except KeyError:
                return text 
        return text