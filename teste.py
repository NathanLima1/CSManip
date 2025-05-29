import csmanip
from tkinter import StringVar

clim = csmanip.Headless()
files = ["src/csmanip/data/BeloHorizonte.csv", "src/csmanip/data/Ibirite.csv", "src/csmanip/data/Florestal.csv", "src/csmanip/data/SeteLagoas.csv"]

#clim.set_cities(files)
#clim.process_selection()
#clim.common_graphs("Target city", "Precipitation", 1962, 2010)
#clim.boxplot("Target city", "Precipitation")
#clim.histograma("Target city", "Precipitation")

clim.triangulation("Arithmetic Average", "Maximum Temperature")
