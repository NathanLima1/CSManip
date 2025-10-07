import csmanip

clim = csmanip.Headless()

files = ["src/csmanip/data/BeloHorizonte.csv", "src/csmanip/data/Ibirite.csv", "src/csmanip/data/Florestal.csv", "src/csmanip/data/SeteLagoas.csv"]

CIDADE = "Mineapolis, US"
DATA_INICIO = "2023-01-01"
DATA_FIM = "2023-01-31"

clim.download_noaa_data(CIDADE, DATA_INICIO, DATA_FIM)