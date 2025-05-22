import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

file_name = "BH Tmax.png"
title_img = "BH Tmax"
caption_img = "the img caption"

data_base = pd.read_csv("C:\\Users\\limam\\OneDrive\\Documentos\\IC\\study-on-changing-trends-main\\BELOHORIZONTEdadosAnuais.csv")

data_base = data_base.iloc[:, [0, 1]]  # Seleciona as colunas relevantes
data_base.columns = ["year", "temperature"] 

data_base["temperature"] = data_base["temperature"].replace(-99.9, None)  # Trata valores ausentes

data_base["date"] = pd.to_datetime(data_base["year"].astype(str) + "-01-01")  # Converte anos para datas

# Configuração do gráfico
sns.set_style("white")
plt.figure(figsize=(12, 2))

cmap = sns.color_palette("RdBu_r", as_cmap=True)

plt.scatter(data_base["date"], [1] * len(data_base), c=data_base["temperature"], cmap=cmap, marker="s", s=200)
plt.gca().xaxis.set_major_locator(mdates.YearLocator(5))  # Marcações a cada 5 anos
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
plt.yticks([])
plt.title(title_img, fontsize=14, fontweight="bold")
plt.xlabel("")
plt.ylabel("")
plt.grid(False)
plt.figtext(0.9, 0.02, caption_img, fontsize=10, ha="right")

# Salvando a imagem
plt.savefig(file_name, dpi=300, bbox_inches='tight')
plt.show()
