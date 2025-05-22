import numpy as np
import pandas as pd

city_files = {
    1: "ARAXA.csv",
    2: "BARBALHA.csv",
    3: "BELOHORIZONTE.csv",
    4: "BELEM.csv",
    5: "CAPARAO.csv",
    6: "CUIABA.csv",
    7: "CURITIBA.csv",
    8: "MANAUS.csv",
    9: "NATAL.csv",
    10: "SAOPAULO.csv",
    11: "SAOSIMAO.csv",
    12: "Cabrobo.csv"
}

for index in range(1, 13):
    city_name = city_files[index].split(".")[0]
    cidade = pd.read_csv(f"address/{city_files[index]}").values
    
    dadosMensais = []
    Tmax = []
    Tmin = []
    Tmean = []
    Chuva = 0
    cont = 1
    
    for i in range(len(cidade) - 1):
        if cidade[i, 1] == cidade[i + 1, 1]:
            Chuva += cidade[i, 3]
            Tmin.append(cidade[i, 5])
            Tmax.append(cidade[i, 4])
            Tmean.append(cidade[i, 6])
            cont += 1
        else:
            if len(Tmax) > 0 and len(Tmin) > 0 and len(Tmean) > 0:
                aux = [cidade[i, 0], cidade[i, 1], Chuva, max(Tmax), min(Tmin), np.mean(Tmean)]
                dadosMensais.append(aux)
            Tmax, Tmin, Tmean, Chuva = [], [], [], 0
    
    df_mensal = pd.DataFrame(dadosMensais, columns=["Ano", "Mes", "Chuva", "Tmax", "Tmin", "Tmean"])
    df_mensal.to_csv(f"{city_name}DadosMensais.csv", index=False)
    
    dadosTrimestrais = []
    for i in range(len(dadosMensais) - 2):
        if dadosMensais[i][1] in [1, 4, 7, 10]:
            Chuva = sum([row[2] for row in dadosMensais[i:i+3]])
            Tmin = min(row[4] for row in dadosMensais[i:i+3])
            Tmax = max(row[3] for row in dadosMensais[i:i+3])
            Tmean = np.mean([row[5] for row in dadosMensais[i:i+3]])
            trimestre = (dadosMensais[i][1] - 1) // 3 + 1
            dadosTrimestrais.append([dadosMensais[i][0], trimestre, Chuva, Tmax, Tmin, Tmean])
    
    df_trimestral = pd.DataFrame(dadosTrimestrais, columns=["Ano", "Trimestre", "Chuva", "Tmax", "Tmin", "Tmean"])
    df_trimestral.to_csv(f"{city_name}dadosTrimestrais.csv", index=False)
    
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
                aux = [dadosMensais[i][0], Chuva, max(Tmax), min(Tmin), np.mean(Tmean)]
                dadosAnuais.append(aux)
            Tmax, Tmin, Tmean, Chuva = [], [], [], 0
    
    df_anual = pd.DataFrame(dadosAnuais, columns=["Ano", "Chuva", "Tmax", "Tmin", "Tmean"])
    df_anual.to_csv(f"{city_name}dadosAnuais.csv", index=False)
