import pandas as pd
import numpy as np
import statsmodels.api as sm

def mann_kendall_test(data):
    n = len(data)
    s = 0
    for i in range(n - 1):
        for j in range(i + 1, n):
            s += np.sign(data[j] - data[i])

    unique_values = np.unique(data)
    if len(unique_values) == 1:
        return {"trend": "no trend", "p-value": 1.0, "Tau": 0}

    variance = (n * (n - 1) * (2 * n + 5)) / 18
    z = s / np.sqrt(variance) if variance > 0 else 0

    # Determinar tendência com base no valor de S
    trend = "increasing" if s > 0 else "decreasing" if s < 0 else "no trend"

    # Usando normalização para aproximar o p-valor
    p_value = 2 * (1 - sm.stats.norm.cdf(abs(z)))

    tau = s / (n * (n - 1) / 2)
    
    return {"trend": trend, "p-value": p_value, "Tau": tau}

def analyze_trend(csv_file, column_name):
    data_base = pd.read_csv(csv_file)
    
    if column_name not in data_base.columns:
        raise ValueError(f"Coluna '{column_name}' não encontrada no CSV.")
    
    # Pegar a série temporal
    data_series = data_base[column_name].dropna().to_numpy()

    # Teste de Mann-Kendall
    mk_result = mann_kendall_test(data_series)

    # Inclinação de Sen 
    n = len(data_series)
    slopes = [(data_series[j] - data_series[i]) / (j - i) for i in range(n - 1) for j in range(i + 1, n)]
    sens_slope = np.median(slopes)

    return {
        "mann_kendall": mk_result,
        "sens_slope": sens_slope
    }

if __name__ == "__main__":
    csv_file = "dados/BeloHorizonte_TNN.csv"
    trends = analyze_trend(csv_file, "V2")
    