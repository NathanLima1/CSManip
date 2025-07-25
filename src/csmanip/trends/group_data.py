import numpy as np
import pandas as pd
import os

def group_data(city_files: list, input_dir: str, output_dir: str):
    """
    Agrupa dados diários em mensais, trimestrais e anuais.

    Args:
        city_files (list): Lista com os nomes dos arquivos de entrada (ex: ['BARBALHA.csv']).
        input_dir (str): O diretório onde os arquivos de entrada estão localizados.
        output_dir (str): O diretório onde os arquivos de saída serão salvos.
    """
    # Garante que o diretório de saída exista
    os.makedirs(output_dir, exist_ok=True)

    for city_filename in city_files:
        # Extrai o nome base do arquivo (ex: "BARBALHA")
        city_name = os.path.splitext(city_filename)[0]
        # Constrói o caminho completo para o arquivo de entrada
        input_path = os.path.join(input_dir, city_filename)

        try:
            df = pd.read_csv(input_path, na_values=-99)
            df.dropna(inplace=True)
            cidade = df.values
        except FileNotFoundError:
            print(f"Erro: Arquivo de entrada não encontrado em '{input_path}'")
            continue # Pula para a próxima cidade se o arquivo não for encontrado

        # O restante da sua lógica para processar os dados permanece o mesmo...
        dadosMensais = []
        Tmax = []
        Tmin = []
        Tmean = []
        Chuva = 0
        cont = 1
        
        for i in range(len(cidade) - 1):
            if cidade[i, 1] == cidade[i + 1, 1]:
                Chuva += float(cidade[i, 3])
                Tmin.append(cidade[i, 5])
                Tmax.append(cidade[i, 4])
                Tmean.append(cidade[i, 6])
                cont += 1
            else:
                if len(Tmax) > 0 and len(Tmin) > 0 and len(Tmean) > 0:
                    aux = [cidade[i, 0], cidade[i, 1], Chuva, 
                           np.nanmax(Tmax), 
                           np.nanmin(Tmin), 
                           np.nanmean(Tmean)]
                    dadosMensais.append(aux)
                Tmax, Tmin, Tmean, Chuva = [], [], [], 0
        
        df_mensal = pd.DataFrame(dadosMensais, columns=["Ano", "Mes", "Chuva", "Tmax", "Tmin", "Tmean"])
        
        # Constrói os caminhos completos para os arquivos de saída
        mensal_output_path = os.path.join(output_dir, f"{city_name}DadosMensais.csv")
        trimestral_output_path = os.path.join(output_dir, f"{city_name}dadosTrimestrais.csv")
        anual_output_path = os.path.join(output_dir, f"{city_name}dadosAnuais.csv")

        # Salva os arquivos de saída
        df_mensal.to_csv(mensal_output_path, index=False)

        # ... (Lógica para dados trimestrais e anuais com caminhos de saída) ...
        dadosTrimestrais = []
        for i in range(len(dadosMensais) - 2):
            if dadosMensais[i][1] in [1, 4, 7, 10]:
                Chuva = sum([row[2] for row in dadosMensais[i:i+3]])
                Tmin = np.nanmin([row[4] for row in dadosMensais[i:i+3]])
                Tmax = np.nanmax([row[3] for row in dadosMensais[i:i+3]])
                Tmean = np.nanmean([row[5] for row in dadosMensais[i:i+3]])
                trimestre = (dadosMensais[i][1] - 1) // 3 + 1
                dadosTrimestrais.append([dadosMensais[i][0], trimestre, Chuva, Tmax, Tmin, Tmean])
        
        df_trimestral = pd.DataFrame(dadosTrimestrais, columns=["Ano", "Trimestre", "Chuva", "Tmax", "Tmin", "Tmean"])
        df_trimestral.to_csv(trimestral_output_path, index=False)
        
        dadosAnuais = []
        Tmax, Tmin, Tmean, Chuva = [], [], [], 0
        
        for i in range(len(dadosMensais) - 1):
            if dadosMensais[i][0] == dadosMensais[i + 1][0]:
                Chuva += dadosMensais[i][2]
                Tmax.append(dadosMensais[i][3])
                Tmin.append(dadosMensais[i][4])
                Tmean.append(dadosMensais[i][5])
            else:
                if Tmax and Tmin and Tmean:
                    aux = [dadosMensais[i][0], Chuva, 
                           np.nanmax(Tmax), 
                           np.nanmin(Tmin), 
                           np.nanmean(Tmean)]
                    dadosAnuais.append(aux)
                Tmax, Tmin, Tmean, Chuva = [], [], [], 0
        
        df_anual = pd.DataFrame(dadosAnuais, columns=["Ano", "Chuva", "Tmax", "Tmin", "Tmean"])
        df_anual['Ano'] = df_anual['Ano'].astype(int)
        df_anual.to_csv(anual_output_path, index=False)

        print(f"Arquivos agrupados para '{city_name}' salvos em '{output_dir}'")