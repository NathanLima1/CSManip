import csmanip
from tkinter import StringVar

clim = csmanip.Headless()
files = ["src/csmanip/data/Nova_Xavantina.csv", "src/csmanip/data/Goiania.csv", "src/csmanip/data/Canarana.csv", "src/csmanip/data/Poxoreu.csv"]
#clim.set_cities(files)
#clim.process_selection()
#clim.grid_search_dt()

#clim.common_graphs("Common data", "Maximum temperature", 1961, 2012)
#clim.generate_custom_test()
#clim.generate_global_test()
#loop = csmanip.Framework()
#loop.mainloop()
#clim.triangulation("Optimized Normal Ratio", "Maximum Temperature")
#clim.triangulation("Optimized Inverse Distance Weighted", "Maximum temperature")

trends = csmanip.Trends()

input_dir = "src/csmanip/data"
output_dir = "src/csmanip/processed_data"

cidades = ["Barbalha.csv"]

trends.group_data(cidades, output_dir, output_dir)
trends.plot_annual_data(
    csv_path='src/csmanip/processed_data/BarbalhadadosAnuais.csv',
    index='tmean',  # Coluna a ser plotada ('tmax', 'tmin', 'tmean', 'prec')
    file_name='tendencia_anual_tmedia_barbalha.png',
    title_img='Tendência da Temperatura Média Anual em Barbalha',
    caption_img='Fonte: INMET'
)