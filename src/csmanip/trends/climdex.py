import pandas as pd
import xarray as xr
import xclim
import numpy as np
import os
# A parte de plotagem foi mantida como estava, você pode ajustá-la depois se necessário.
# from matplotlib.backends.backend_pdf import PdfPages
# import matplotlib.pyplot as plt

class Climdex:
    def __init__(self):
        # A coluna de leitura pode ser simplificada se o seu CSV não tiver cabeçalho
        self.read_columns = ["year", "month", "day", "pr", "tmax", "tmin"]
        self.write_columns = ["year", "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec", "annual"]

    def read_files(self, names:list):
        """
        Lê uma lista de arquivos CSV e retorna um dicionário de DataFrames.
        """
        csv_files = {}
        for name in names:
            csv_file = os.path.join("..", "dados", f"{name}.csv")
            # Adicionado 'parse_dates' para já criar a coluna de data
            df = pd.read_csv(csv_file, names=self.read_columns, header=None)
            df['time'] = pd.to_datetime(df[['year', 'month', 'day']])
            df = df.set_index('time')
            csv_files[name] = df
        return csv_files

    def calculate_indices(self, df: pd.DataFrame, base_period: tuple = ("1991-01-01", "2020-12-31")):
        """
        Calcula os índices climáticos usando xclim.
        Retorna um xarray.Dataset com todos os índices calculados.
        """
        # Converte o DataFrame do pandas para um Dataset do xarray
        ds = df.to_xarray()
        
        # Adicionar metadados de unidades
        ds['tmax'].attrs['units'] = 'degC'
        ds['tmin'].attrs['units'] = 'degC'
        ds['pr'].attrs['units'] = 'mm/day'

        tmax_climatology = ds.tmax.sel(time=slice(base_period[0], base_period[1]))
        tmin_climatology = ds.tmin.sel(time=slice(base_period[0], base_period[1]))
        pr_climatology = ds.pr.sel(time=slice(base_period[0], base_period[1]))

        indices_to_calc = {
            "TXx": xclim.atmos.tx_max(ds.tmax, freq='MS'),
            "TX10p": xclim.atmos.tx10p(ds.tmax, per=tmax_climatology, freq='MS'),
            "TX90p": xclim.atmos.tx90p(ds.tmax, per=tmax_climatology, freq='MS'),
            "TNn": xclim.atmos.tn_min(ds.tmin, freq='MS'),
            "TN10p": xclim.atmos.tn10p(ds.tmin, per=tmin_climatology, freq='MS'),
            "TN90p": xclim.atmos.tn90p(ds.tmin, per=tmin_climatology, freq='MS'),
            "TXx_annual": xclim.atmos.tx_max(ds.tmax, freq='YS'),
            "TX10p_annual": xclim.atmos.tx10p(ds.tmax, per=tmax_climatology, freq='YS'),
            "TX90p_annual": xclim.atmos.tx90p(ds.tmax, per=tmax_climatology, freq='YS'),
            "TNn_annual": xclim.atmos.tn_min(ds.tmin, freq='YS'),
            "TN10p_annual": xclim.atmos.tn10p(ds.tmin, per=tmin_climatology, freq='YS'),
            "TN90p_annual": xclim.atmos.tn90p(ds.tmin, per=tmin_climatology, freq='YS'),
            "PRCPTOT": xclim.atmos.prcptot(ds.pr, freq='MS'),
            "R95p": xclim.atmos.r95p(ds.pr, per=pr_climatology, freq='MS'),
            "RX1DAY": xclim.atmos.rx1day(ds.pr, freq='MS'),
            "RX5DAY": xclim.atmos.rx5day(ds.pr, freq='MS'),
            "CDD": xclim.atmos.consecutive_dry_days(ds.pr, freq='MS'),
            "CWD": xclim.atmos.consecutive_wet_days(ds.pr, freq='MS'),
            "PRCPTOT_annual": xclim.atmos.prcptot(ds.pr, freq='YS'),
            "R95p_annual": xclim.atmos.r95p(ds.pr, per=pr_climatology, freq='YS'),
            "RX1DAY_annual": xclim.atmos.rx1day(ds.pr, freq='YS'),
            "RX5DAY_annual": xclim.atmos.rx5day(ds.pr, freq='YS'),
            "CDD_annual": xclim.atmos.consecutive_dry_days(ds.pr, freq='YS'),
            "CWD_annual": xclim.atmos.consecutive_wet_days(ds.pr, freq='YS'),
        }
        return xclim.core.indicator.build_indicator_module_from_dict({}, indices_to_calc).compute()


    def write_indices(self, indices_ds: xr.Dataset, name: str):
        """
        Recebe um Dataset do xarray (do xclim) e salva cada índice
        em um arquivo CSV separado, no formato mensal + anual.
        """
        output_dir = "indices_xclim"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        index_names = ["TXx", "TX10p", "TX90p", "TNn", "TN10p", "TN90p"]

        for index_name in index_names:
            monthly_da = indices_ds[index_name]
            annual_da = indices_ds[f"{index_name}_annual"]

            # Converte os dados mensais para DataFrame e pivotar para o formato de colunas
            df_monthly = monthly_da.to_dataframe()
            df_wide = df_monthly.pivot_table(
                values=index_name, 
                index=df_monthly.index.year, 
                columns=df_monthly.index.month
            ).rename_axis('year', axis='index').rename_axis(None, axis='columns')

            # Renomeia colunas de número (1-12) para nome do mês ('jan'-'dec')
            df_wide.columns = [m.lower() for m in pd.to_datetime(df_wide.columns, format='%m').month_name().str[:3]]

            # Prepara dados anuais e junta com os mensais
            df_annual = annual_da.to_dataframe()
            df_annual = df_annual.rename(columns={f"{index_name}_annual": "annual"})
            df_annual.index = df_annual.index.year # Alinhar o índice (ano)

            # Junta os dois DataFrames
            final_df = df_wide.join(df_annual['annual'])
            
            # Reordena para o formato final
            final_df = final_df.reset_index()
            final_df = final_df.reindex(columns=self.write_columns)
            
            # Salva no arquivo CSV
            output_path = os.path.join(output_dir, f"{name}_{index_name}.csv")
            final_df.round(2).to_csv(output_path, index=False, sep=",")
            print(f"Índice salvo em: {output_path}")