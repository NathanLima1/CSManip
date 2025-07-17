import pandas as pd
import xarray as xr
import xclim

df = pd.read_csv("dados.csv")
df['data'] = pd.to_datetime(df['data'])
df = df.set_index('data')

ds = df.to_xarray()

ds['tmax'].attrs['units'] = 'degC'
ds['tmin'].attrs['units'] = 'degC'
ds['pr'].attrs['units'] = 'mm/day'

# Para os índices baseados em percentis, precisamos de um período de referência.
# Vamos usar todo o período de dados para criar os "climatology" objects.
# Isso é feito uma vez e reutilizado.
pr_climatology = xclim.core.calendar.climatology(ds.pr, 'dayofyear', '1991-01-01', '2020-12-31')
tmax_climatology = xclim.core.calendar.climatology(ds.tmax, 'dayofyear', '1991-01-01', '2020-12-31')
tmin_climatology = xclim.core.calendar.climatology(ds.tmin, 'dayofyear', '1991-01-01', '2020-12-31')

# Dia mais quente
txx = xclim.atmos.tx_max(ds.tmax, freq='YS')
print("TXx", txx)

# Noite mais fria
tnn = xclim.atmos.tn_min(ds.tmin, freq='YS')

# Calcula os percentis uma única vez para o período de referência
p10_tmax = tmax_climatology.quantile(0.1, 'dayofyear')
p90_tmax = tmax_climatology.quantile(0.9, 'dayofyear')
p10_tmin = tmin_climatology.quantile(0.1, 'dayofyear')
p90_tmin = tmin_climatology.quantile(0.9, 'dayofyear')

# Agora, calcula os índices para cada ano
tx10p = xclim.atmos.tx10p(ds.tmax, p10_tmax, freq='YS')
tx90p = xclim.atmos.tx90p(ds.tmax, p90_tmax, freq='YS')
tn10p = xclim.atmos.tn10p(ds.tmin, p10_tmin, freq='YS')
tn90p = xclim.atmos.tn90p(ds.tmin, p90_tmin, freq='YS')

print(f"\nTX10p (% de dias frios):\n{tx10p}")
print(f"\nTX90p (% de dias quentes):\n{tx90p}")
print(f"\nTN10p (% de noites frias):\n{tn10p}")
print(f"\nTN90p (% de noites quentes):\n{tn90p}")

# precipitação total
prcptot = xclim.atmos.prcptot(ds.pr, freq='YS')
print(f"\nPRCPTOT (Precipitação total anual):\n{prcptot}")

# Calcula o percentil 95 da precipitação para o período de referência
p95_pr = pr_climatology.quantile(0.95, 'dayofyear')

# Calcula o índice
r95p = xclim.atmos.r95p(ds.pr, p95_pr, freq='YS')
print(f"\nR95p (Precipitação em dias muito chuvosos):\n{r95p}")

rx1day = xclim.atmos.rx1day(ds.pr, freq='YS')
rx5day = xclim.atmos.rx5day(ds.pr, freq='YS')

print(f"\nRX1DAY (Máximo de chuva em 1 dia):\n{rx1day}")
print(f"\nRX5DAY (Máximo de chuva em 5 dias):\n{rx5day}")

cdd = xclim.atmos.consecutive_dry_days(ds.pr, freq='YS')
print(f"\nCDD (Máximo de dias secos consecutivos):\n{cdd}")

cwd = xclim.atmos.consecutive_wet_days(ds.pr, freq='YS')
print(f"\nCWD (Máximo de dias úmidos consecutivos):\n{cwd}")