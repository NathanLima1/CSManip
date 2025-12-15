import pandas as pd
import numpy as np
from scipy import stats

def mann_kendall_test(data):
    n = len(data)
    s = 0
    for i in range(n - 1):
        for j in range(i + 1, n):
            s += np.sign(data[j] - data[i])

    unique, counts = np.unique(data, return_counts=True)
    
    if len(unique) == n:
        tie_correction = 0
    else:
        tie_correction = np.sum(counts[counts > 1] * (counts[counts > 1] - 1) * (2 * counts[counts > 1] + 5))

    variance = (n * (n - 1) * (2 * n + 5) - tie_correction) / 18
    
    if variance > 0:
        if s > 0:
            z = (s - 1) / np.sqrt(variance)
        elif s < 0:
            z = (s + 1) / np.sqrt(variance)
        else: # s == 0
            z = 0
    else:
        return {"trend": "no trend", "p-value": 1.0, "Tau": 0, "Z-score": 0}

    trend = "increasing" if s > 0 else "decreasing" if s < 0 else "no trend"

    p_value = 2 * (1 - stats.norm.cdf(abs(z)))

    tau = s / (n * (n - 1) / 2)
    
    return {"trend": trend, "p-value": p_value, "Tau": tau, "Z-score": z}

def analyze_trend(csv_file, column_name):
    data_base = pd.read_csv(csv_file)
    
    if column_name not in data_base.columns:
        raise ValueError(f"Coluna '{column_name}' não encontrada no CSV.")
    
    data_series = data_base[column_name].dropna().to_numpy()

    mk_result = mann_kendall_test(data_series)

    n = len(data_series)
    slopes = [(data_series[j] - data_series[i]) / (j - i) for i in range(n - 1) for j in range(i + 1, n)]
    sens_slope = np.median(slopes)

    return {
        "mann_kendall": mk_result,
        "sens_slope": sens_slope
    }

def analyze_indicator_trend(file_path):
    column_name = 'annual'
    try:
        data_base = pd.read_csv(
            file_path,
            header=0,
            sep=','
        )
    except Exception as e:
        print(f"ERRO ao ler {file_path}. Ignorando. Erro: {e}")
        return None
    
    if data_base.columns[0] != 'year' and not data_base.columns[0].startswith('Unnamed'):
         data_base.rename(columns={data_base.columns[0]: 'year'}, inplace=True)
    
    if column_name not in data_base.columns:
        print(f"AVISO: Coluna '{column_name}' não encontrada em {file_path}. Colunas disponíveis: {data_base.columns.tolist()}")
        return None
    
    data_series = data_base[column_name].replace('', np.nan).dropna().astype(float).to_numpy()

    if len(data_series) < 3:
        print(f"AVISO: {file_path} tem menos de 3 pontos de dados na coluna '{column_name}' e foi ignorado.")
        return None
    
    mk_result = mann_kendall_test(data_series)

    n = len(data_series)

    slopes = [(data_series[j] - data_series[i]) / (j - i) 
              for i in range(n - 1) 
              for j in range(i + 1, n)]
              
    sens_slope = np.median(slopes)

    return {
        "mann_kendall": mk_result,
        "sens_slope": sens_slope
    }