"""
Arquivo responsável por cuidar da parte principal do framework e gerenciar as telas
"""

from tkinter import Frame
import tkinter as tk
from tkinter import ttk
from tkinter import Canvas, Label, StringVar, Button, CENTER, DISABLED
import tkinter.filedialog as dlg
import tkinter.messagebox as msg
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.dates as mdates
import datetime as dt
import os
import numpy as np
import threading
from .styles import colors
from .data_processing.data_processing import DataProcessing
from .triangulation.triangulation import Triangulation
from .meta_learning.meta_learning import MetaLearning
from .meta_learning.tests_generator import TestsGenerator
from .data_processing.era5_download import download_and_process_era_data
from .data_processing.noaa_download import download_noaa_data
from .language.language_manager import LanguageManager

from .pages.data_imputation.data_imputation_page import DataImputationPage
from .pages.data_imputation.imputation_techniques_page import ImputationTechniquesPage
from .pages.data_imputation.triangulation_page import TriangulationPage
from .pages.data_imputation.machine_learning.machine_learning_page import MachineLearningPage
from .pages.data_imputation.meta_learning.meta_learning_page import MetaLearningPage
from .pages.data_imputation.view_data_page import ViewDataPage
from .pages.trends.trends_page import ClimateTrendsPage
from .pages.tutorial.tutorial_page import TutorialPage
from .pages.download.download_page import DownloadDataPage
from .pages.start_page import StartPage


class Framework(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Gerenciador de idiomas
        self.i18n = LanguageManager()
        self.i18n.set_language("pt_br")

        self.title(self.i18n.get('app_main_title'))
        self.geometry("1000x700")

        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        # loop dos frames (telas) existentes
        for F in (StartPage, TutorialPage, DownloadDataPage, DataImputationPage, ClimateTrendsPage, ViewDataPage, ImputationTechniquesPage,
                  TriangulationPage, MachineLearningPage, MetaLearningPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        
    def update_all_frames_text(self):
        for frame in self.frames.values():
            frame.update_texts()

    def show_translated_message(self, msg_type, title_key, message_key, **kwargs):
        title = self.i18n.get(title_key)
        message_template = self.i18n.get(message_key)

        try:
            message = message_template.format(**kwargs) if kwargs else message_template
        except KeyError as e:
            print(f"Erro de formatação na mensagem '{message_key}': Placeholder {e} faltando nos kwargs.")
            message = message_template

        if msg_type == 'error':
            msg.showerror(title=title, message=message)
        elif msg_type == 'info':
            msg.showinfo(title=title, message=message)
        elif msg_type == 'warning':
            msg.showwarning(title=title, message=message)
        else:
            print(f"Tipo de mensagem desconhecido: {msg_type}")

    