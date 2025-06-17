import csmanip
from tkinter import StringVar

clim = csmanip.Headless()
files = ["src/csmanip/data/BeloHorizonte.csv", "src/csmanip/data/Ibirite.csv", "src/csmanip/data/Florestal.csv", "src/csmanip/data/SeteLagoas.csv"]


#clim.generate_global_test()
loop = csmanip.Framework()
loop.mainloop()