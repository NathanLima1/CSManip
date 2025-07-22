import pandas as pd
import xarray as xr
import xclim
from pathlib import Path
import os
# Importações necessárias para a plotagem
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

class Climdex:
    def __init__(self):
        self.read_columns = ["year", "month", "day", "pr", "tmax", "tmin"]
        self.write_columns = ["year", "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec", "annual"]
        
        self.indices_base = [
            "TXx", "TX10p", "TX90p", "TNn", "TN10p", "TN90p",
            "PRCPTOT", "R95p", "RX1DAY", "RX5DAY", "CDD", "CWD"
        ]
        
        # MELHORIA 1: Mapa de unidades para plotagem dinâmica
        self.units_map = {
            "TXx": "°C", "TX10p": "dias", "TX90p": "dias",
            "TNn": "°C", "TN10p": "dias", "TN90p": "dias",
            "PRCPTOT": "mm", "R95p": "mm", "RX1DAY": "mm", "RX5DAY": "mm",
            "CDD": "dias", "CWD": "dias"
        }

    # ... (os métodos read_files e calculate_indices permanecem os mesmos da versão anterior) ...
    def read_files_climdex(self, processed_dir: str, station_names: list) -> dict:
        """Lê uma lista de arquivos CSV e retorna um dicionário de DataFrames."""
        dataframes = {}
        for name in station_names:
            # 1. Constrói o caminho do arquivo de forma flexível
            file_path = os.path.join(processed_dir, f"{name}.csv")
            
            if not os.path.exists(file_path):
                print(f"AVISO: Arquivo não encontrado em '{file_path}'. Pulando estação '{name}'.")
                continue

            df = pd.read_csv(file_path)

            if 'prec' in df.columns:
                df.rename(columns={'prec': 'pr'}, inplace=True)
            
            df['time'] = pd.to_datetime(df[['year', 'month', 'day']])
            
            if 'Unnamed: 0' in df.columns:
                df = df.drop(columns=['Unnamed: 0'])

            dataframes[name] = df
            
        return dataframes

    def calculate_indices(self, df: pd.DataFrame, base_period: tuple = ("1991-01-01", "2020-12-31")) -> xr.Dataset:
        """Calcula os índices climáticos usando xclim de forma dinâmica."""
        ds = df.to_xarray()
        ds['tmax'].attrs['units'] = 'degC'
        ds['tmin'].attrs['units'] = 'degC'
        ds['pr'].attrs['units'] = 'mm/day'
        tmax_climatology = ds.tmax.sel(time=slice(base_period[0], base_period[1]))
        tmin_climatology = ds.tmin.sel(time=slice(base_period[0], base_period[1]))
        pr_climatology = ds.pr.sel(time=slice(base_period[0], base_period[1]))
        indices_to_calc = {}
        indicator_map = {
            "TXx": (xclim.atmos.tx_max, ds.tmax, {}), "TX10p": (xclim.atmos.tx10p, ds.tmax, {'per': tmax_climatology}),
            "TX90p": (xclim.atmos.tx90p, ds.tmax, {'per': tmax_climatology}), "TNn": (xclim.atmos.tn_min, ds.tmin, {}),
            "TN10p": (xclim.atmos.tn10p, ds.tmin, {'per': tmin_climatology}), "TN90p": (xclim.atmos.tn90p, ds.tmin, {'per': tmin_climatology}),
            "PRCPTOT": (xclim.atmos.prcptot, ds.pr, {}), "R95p": (xclim.atmos.r95p, ds.pr, {'per': pr_climatology}),
            "RX1DAY": (xclim.atmos.rx1day, ds.pr, {}), "RX5DAY": (xclim.atmos.rx5day, ds.pr, {}),
            "CDD": (xclim.atmos.consecutive_dry_days, ds.pr, {}), "CWD": (xclim.atmos.consecutive_wet_days, ds.pr, {}),
        }
        for index_name in self.indices_base:
            if index_name in indicator_map:
                func, data_var, kwargs = indicator_map[index_name]
                indices_to_calc[index_name] = func(data_var, freq='MS', **kwargs)
                indices_to_calc[f"{index_name}_annual"] = func(data_var, freq='YS', **kwargs)
        return xr.Dataset(indices_to_calc).compute()

    def write_indices(self, indices_ds: xr.Dataset, name: str, output_dir: str = "indices_xclim"):
        """Salva cada índice em um arquivo CSV separado."""
        # Este método permanece como antes
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        for index_name in self.indices_base:
            monthly_da = indices_ds[index_name]
            annual_da = indices_ds[f"{index_name}_annual"]
            df_monthly = monthly_da.to_dataframe()
            df_wide = df_monthly.pivot_table(values=index_name, index=df_monthly.index.year, columns=df_monthly.index.month).rename_axis('year', axis='index').rename_axis(None, axis='columns')
            month_names = [pd.to_datetime(f"2024-{i}-01").strftime('%b').lower() for i in range(1, 13)]
            df_wide.columns = month_names
            df_annual = annual_da.to_dataframe().rename(columns={f"{index_name}_annual": "annual"})
            df_annual.index = df_annual.index.year
            final_df = df_wide.join(df_annual['annual']).reset_index().reindex(columns=self.write_columns)
            final_csv_path = output_path / f"{name}_{index_name}.csv"
            final_df.round(2).to_csv(final_csv_path, index=False, sep=",")
            print(f"Índice salvo em: {final_csv_path}")


    # NOVO MÉTODO DE PLOTAGEM INTEGRADO
    def plot_and_save_indices(self, indices_ds: xr.Dataset, name: str, output_dir: str = "graficos_indices"):
        """
        Gera gráficos para cada índice e os salva em arquivos PDF separados.
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Itera sobre cada índice base para criar um PDF para cada um
        for index_name in self.indices_base:
            print(f"Gerando gráfico para o índice: {index_name}")
            
            # Prepara os dados no formato longo, ideal para plotagem
            monthly_da = indices_ds[index_name]
            df_long = monthly_da.to_dataframe(name=index_name).reset_index()
            df_long['year'] = df_long['time'].dt.year
            df_long['month'] = df_long['time'].dt.month

            pdf_path = output_path / f"{name}_decadal_{index_name}.pdf"

            with PdfPages(pdf_path) as pdf:
                start_year = df_long["year"].min()
                end_year = df_long["year"].max()
                
                # Gera lista de décadas para criar os subplots
                decades = list(range(start_year, end_year + 1, 10))
                if not decades: continue

                plt.figure(figsize=(12, len(decades) * 2.5))

                for i, start_decade in enumerate(decades):
                    end_decade = start_decade + 9
                    # Filtra os dados para a década atual
                    subset = df_long[(df_long["year"] >= start_decade) & (df_long["year"] <= end_decade)]

                    if subset.empty:
                        continue

                    ax = plt.subplot(len(decades), 1, i + 1)
                    
                    # Cria um eixo x contínuo (ex: 2001.0 para Jan, 2001.5 para Jun)
                    x_axis = subset["year"] + (subset["month"] - 1) / 12
                    ax.plot(x_axis, subset[index_name], color="blue", linewidth=0.8, marker='o', markersize=2, linestyle='-')

                    # MELHORIA 2: Título e eixos dinâmicos
                    unit = self.units_map.get(index_name, "") # Pega a unidade do mapa
                    ax.set_title(f"Estação: {name}, Década: {start_decade}-{min(end_decade, end_year)}, Índice: {index_name}", fontsize=10)
                    ax.set_ylabel(f"Valor ({unit})")
                    
                    # MELHORIA 3: Limites e Ticks dos eixos dinâmicos
                    ax.set_xlim(start_decade, min(end_decade, end_year) + 1)
                    ax.set_xticks(range(start_decade, min(end_decade, end_year) + 2, 1))
                    # Deixa o matplotlib definir os ticks do eixo y automaticamente
                    
                    ax.grid(True, linestyle='--', alpha=0.6)

                plt.tight_layout()
                pdf.savefig()
                plt.close()
            
            print(f"Gráfico salvo em: {pdf_path}")
