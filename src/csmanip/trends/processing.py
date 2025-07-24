import pandas as pd
import os
import numpy as np

          
def process_csv(cities: list, input_dir:str, output_dir:str):
    os.makedirs(output_dir, exist_ok=True)
    columns = ["data", "prec", "tmax", "tmean", "tmin"]

    for city in cities:
        input_file = os.path.join(input_dir, city)
        output_file = os.path.join(output_dir, city)
        try:
            df = pd.read_csv(input_file, skiprows=11, header=None, names=columns, sep=";", decimal=",", index_col=False)
            
            # Substituir valores ausentes nas colunas climáticas por -99
            df[["prec", "tmax", "tmin", "tmean"]] = df[["prec", "tmax", "tmin", "tmean"]].fillna(-99)
            # Remover linhas com qualquer -99
            #df = df[(df["prec"] != -99) & (df["tmax"] != -99) & (df["tmin"] != -99 & (df["tmean"] != -99))]

            df["data"] = pd.to_datetime(df["data"], format="%Y-%m-%d", errors="coerce")

            df["year"] = df["data"].dt.year
            df["month"] = df["data"].dt.month
            df["day"] = df["data"].dt.day

            df.drop(columns=["data"], inplace=True)

            sorted_columns = ["year", "month", "day", "prec", "tmax", "tmin", "tmean"]
            df = df[sorted_columns]
            
            df.to_csv(output_file, index=False, sep=",", header=False)
            

        except FileNotFoundError:
            print(f"Erro: Arquivo {input_file} não encontrado.")
        except Exception as e:
            print(f"Erro ao ler {input_file}: {e}")

