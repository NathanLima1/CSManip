import csmanip
from tkinter import StringVar

clim = csmanip.Headless()
files = ["src/csmanip/data/BeloHorizonte.csv", "src/csmanip/data/Ibirite.csv", "src/csmanip/data/Florestal.csv", "src/csmanip/data/SeteLagoas.csv"]
#clim.set_cities(files)
#clim.process_selection()
#clim.grid_search_dt()

#clim.common_graphs("Common data", "Maximum temperature", 1961, 2012)
#clim.generate_custom_test()
#clim.generate_global_test()
#loop = csmanip.Framework()
#loop.mainloop()
#clim.triangulation("Arithmetic Average", "Maximum temperature")
clim.triangulation("Optimized Inverse Distance Weighted", "Maximum temperature")