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
trends.process_csv(cidades, input_dir, output_dir)
dados_das_estacoes = trends.read_files_climdex(output_dir, cidades)

df_barbalha = dados_das_estacoes["Barbalha.csv"]
indices_calculados = trends.calculate_indices(df_barbalha, ("1991-01-01", "2020-12-31"))

output_dir_indices = 'indices_climaticos'
#trends.write_indices(indices_calculados, "BarbalhaIndex", output_dir)

pdf_output_path = f"{output_dir_indices}/graficos_indices_barbalha.pdf"

trends.plot_and_save_indices(indices_calculados, "Barbalha", output_dir)


print(f"Gráficos de extremos salvos em: {pdf_output_path}")

resultado_tendencia = trends.analyze_trend(
    csv_file='src/csmanip/processed_data/BarbalhadadosAnuais.csv',
    column_name='Tmean'
)

print(resultado_tendencia)