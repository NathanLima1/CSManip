import tkinter as tk
from tkinter import ttk, messagebox as msg
import tkinter.filedialog as dlg
import typing
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import messagebox as msg
from tkinter import Canvas, Label, StringVar, Button, CENTER, DISABLED
from ..triangulation.triangulation import Triangulation
from ..data_processing.data_processing import DataProcessing