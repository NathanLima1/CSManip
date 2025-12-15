import pandas as pd
import xarray as xr
import xclim
from xclim.indicators import icclim
from xclim import indices
from pathlib import Path
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np


class Climdex:
    def __init__(self):
        self.read_columns = ["year", "month", "day", "pr", "tmax", "tmin"]
        self.write_columns = ["year", "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec", "annual"]
        
        self.indices_base = [
            "TXx", "TX10p", "TX90p", "TNn", "TN10p", "TN90p",
            "PRCPTOT", "R95p", "RX1DAY", "RX5DAY", "CDD", "CWD"
        ]
        
        self.units_map = {
            "TXx": "°C", "TX10p": "dias", "TX90p": "dias",
            "TNn": "°C", "TN10p": "dias", "TN90p": "dias",
            "PRCPTOT": "mm", "R95p": "mm", "RX1DAY": "mm", "RX5DAY": "mm",
            "CDD": "dias", "CWD": "dias"
        }

    def read_files_climdex(self, processed_dir: str, station_names: list) -> dict:
        dataframes = {}
        col_names = ["year", "month", "day", "prec", "tmax", "tmin", "tmean"]

        for name in station_names:
            file_path = os.path.join(processed_dir, f"{name}")
            
            if not os.path.exists(file_path):
                print(f"AVISO: Arquivo não encontrado em '{file_path}'. Pulando estação '{name}'.")
                continue

            df = pd.read_csv(file_path, header=None, names=col_names)

            rename_dict = {
                'prec': 'pr',
                'tmax': 'tasmax',
                'tmin': 'tasmin'
            }
            df.rename(columns=rename_dict, inplace=True)
            
            df['time'] = pd.to_datetime(df[['year', 'month', 'day']])
            df.set_index('time', inplace=True)
            df.drop(columns=['year', 'month', 'day'], inplace=True)

            if 'Unnamed: 0' in df.columns:
                df.drop(columns=['Unnamed: 0'], inplace=True)

            dataframes[name] = df
            
        return dataframes

    def calculate_indices(self, df: pd.DataFrame, base_period: tuple[str, str]):
        """
        Calcula uma lista de índices climáticos do ETCCDI usando xclim.
        """
        # Converter o DataFrame do pandas para um Dataset do xarray
        if not isinstance(df.index, pd.DatetimeIndex):
            raise ValueError("O DataFrame de entrada deve ter um DatetimeIndex.")
        ds = df.to_xarray()

        ds.tasmax.attrs.update({
            'standard_name': 'air_temperature',
            'cell_methods': 'time: maximum',
            'units': 'degC'
        })
        ds.tasmin.attrs.update({
            'standard_name': 'air_temperature',
            'cell_methods': 'time: minimum',
            'units': 'degC'
        })
        if 'pr' in ds:
            ds.pr.attrs.update({
                'standard_name': 'precipitation_flux',
                'cell_methods': 'time: mean',
                'units': 'mm/day'
            })

        # Preparar o período base para cálculo dos percentis
        ds_base = ds.sel(time=slice(base_period[0], base_period[1]))

        # Pré-calcular todos os percentis necessários
        with xr.set_options(keep_attrs=True):
            tx10_thresh = xclim.core.calendar.percentile_doy(ds_base.tasmax, per=10).sel(percentiles=10).drop_vars('percentiles')
            tx90_thresh = xclim.core.calendar.percentile_doy(ds_base.tasmax, per=90).sel(percentiles=90).drop_vars('percentiles')
            tn10_thresh = xclim.core.calendar.percentile_doy(ds_base.tasmin, per=10).sel(percentiles=10).drop_vars('percentiles')
            tn90_thresh = xclim.core.calendar.percentile_doy(ds_base.tasmin, per=90).sel(percentiles=90).drop_vars('percentiles')
            if 'pr' in ds:
                pr95_thresh = xclim.core.calendar.percentile_doy(ds_base.pr, per=95).sel(percentiles=95).drop_vars('percentiles')

        #  Definir e calcular cada índice com os nomes de função corretos
        indices_results = {}
        freq_m = 'MS'  # Frequência Mensal (Month Start)

        # --- Índices de Temperatura ---
        indices_results['TXx'] = icclim.TXx(tasmax=ds.tasmax, freq=freq_m)
        indices_results['TNn'] = icclim.TNn(tasmin=ds.tasmin, freq=freq_m)
        indices_results['TX10p'] = indices.tx10p(tasmax=ds.tasmax, tasmax_per=tx10_thresh, freq=freq_m)
        indices_results['TX90p'] = indices.tx90p(tasmax=ds.tasmax, tasmax_per=tx90_thresh, freq=freq_m)
        indices_results['TN10p'] = indices.tn10p(tasmin=ds.tasmin, tasmin_per=tn10_thresh, freq=freq_m)
        indices_results['TN90p'] = indices.tn90p(tasmin=ds.tasmin, tasmin_per=tn90_thresh, freq=freq_m)
        indices_results['TR'] = icclim.TR(tasmin=ds.tasmin, freq=freq_m)
        indices_results['FD'] = icclim.FD(tasmin=ds.tasmin, freq=freq_m)


        # --- Índices de Precipitação ---
        if 'pr' in ds:
            indices_results['PRCPTOT'] = icclim.PRCPTOT(pr=ds.pr, freq=freq_m)
            indices_results['R95p'] = icclim.R95p(pr=ds.pr, pr_per=pr95_thresh, freq=freq_m)
            indices_results['RX1DAY'] = icclim.RX1day(pr=ds.pr, freq=freq_m)
            indices_results['RX5DAY'] = icclim.RX5day(pr=ds.pr, freq=freq_m)
            indices_results['CDD'] = icclim.CDD(pr=ds.pr, freq=freq_m)
            indices_results['CWD'] = icclim.CWD(pr=ds.pr, freq=freq_m)
            indices_results['R10mm'] = icclim.R10mm(pr=ds.pr, freq=freq_m)
            indices_results['R20mm'] = icclim.R20mm(pr=ds.pr, freq=freq_m)

        else:
            print("Aviso: Coluna 'pr' de precipitação não encontrada. Índices de precipitação não serão calculados.")

        # Combinar todos os resultados em um único DataFrame
        valid_indices = {k: v for k, v in indices_results.items() if v is not None}
        final_ds = xr.Dataset(valid_indices)
        
        freq_a = 'AS'  # Frequência Anual (Year Start)
        annual_indices = {}

        # Agregação para índices de contagem ou soma (dias, mm)
        sum_indices = ["TX10p", "TX90p", "TN10p", "TN90p", "PRCPTOT", "R95p", "R10mm", "R20mm", "FD", "TR", "CWD", "CDD"]
        for name, da in final_ds.items():
            if name in sum_indices:
                annual_indices[f"{name}_annual"] = da.resample(time=freq_a).sum(skipna=False)

        # Agregação para índices de máximo (°C, mm)
        max_indices = ["TXx", "RX1DAY", "RX5DAY"]
        for name, da in final_ds.items():
            if name in max_indices:
                annual_indices[f"{name}_annual"] = da.resample(time=freq_a).max(skipna=False)

        # Agregação para índices de mínimo (°C)
        min_indices = ["TNn"]
        for name, da in final_ds.items():
            if name in min_indices:
                annual_indices[f"{name}_annual"] = da.resample(time=freq_a).min(skipna=False)
                
        # 7. Combinar os resultados anuais com os mensais
        final_ds = xr.merge([final_ds, xr.Dataset(annual_indices)])

        return final_ds

    def write_indices(self, indices_ds: xr.Dataset, name: str, output_dir: str = "indices_xclim"):
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        temp_indices_to_correct = ["TXx", "TNn"]
        for index_name in self.indices_base:
            monthly_da = indices_ds[index_name]
            annual_da = indices_ds[f"{index_name}_annual"]

            if index_name in temp_indices_to_correct:
                monthly_da = monthly_da - 273.15
                annual_da = annual_da - 273.15
            df_monthly = monthly_da.to_dataframe()
            df_wide = df_monthly.pivot_table(values=index_name, index=df_monthly.index.year, columns=df_monthly.index.month).rename_axis('year', axis='index').rename_axis(None, axis='columns')
            month_names = [pd.to_datetime(f"2024-{i}-01").strftime('%b').lower() for i in range(1, 13)]
            df_wide.columns = month_names
            df_annual = annual_da.to_dataframe().rename(columns={f"{index_name}_annual": "annual"})
            df_annual.index = df_annual.index.year
            final_df = df_wide.join(df_annual['annual']).reset_index().reindex(columns=self.write_columns)
            final_csv_path = output_path / f"{name}_{index_name}"
            final_df.round(2).to_csv(final_csv_path, index=False, sep=",")
            print(f"Índice salvo em: {final_csv_path}")

    def plot_and_save_indices(self, indices_ds: xr.Dataset, name: str, output_dir: str = "graficos_indices"):
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        temp_indices_to_correct = ["TXx", "TNn"]
        
        for index_name in self.indices_base:
            print(f"Gerando gráfico para o índice: {index_name}")
            
            monthly_da = indices_ds[index_name].copy(deep=True)
            if index_name in temp_indices_to_correct:
                monthly_da = monthly_da - 273.15

            df_long = monthly_da.to_dataframe(name=index_name).reset_index()
            df_long['year'] = df_long['time'].dt.year
            df_long['month'] = df_long['time'].dt.month

            pdf_path = output_path / f"{name}_decadal_{index_name}.pdf"

            with PdfPages(pdf_path) as pdf:
                start_year = df_long["year"].min()
                end_year = df_long["year"].max()
                
                decades = list(range(start_year, end_year + 1, 10))
                if not decades: continue

                plt.figure(figsize=(12, len(decades) * 2.5))

                for i, start_decade in enumerate(decades):
                    end_decade = start_decade + 9
                    subset = df_long[(df_long["year"] >= start_decade) & (df_long["year"] <= end_decade)]

                    if subset.empty:
                        continue

                    ax = plt.subplot(len(decades), 1, i + 1)
                    
                    x_axis = subset["year"] + (subset["month"] - 1) / 12
                    ax.plot(x_axis, subset[index_name], color="blue", linewidth=0.8, marker='o', markersize=2, linestyle='-')

                    unit = self.units_map.get(index_name, "")
                    ax.set_title(f"Estação: {name}, Década: {start_decade}-{min(end_decade, end_year)}, Índice: {index_name}", fontsize=10)
                    ax.set_ylabel(f"Valor ({unit})")
                    
                    ax.set_xlim(start_decade, min(end_decade, end_year) + 1)
                    ax.set_xticks(range(start_decade, min(end_decade, end_year) + 2, 1))
                    
                    ax.grid(True, linestyle='--', alpha=0.6)

                plt.tight_layout()
                pdf.savefig()
                plt.close()
            
            print(f"Gráfico salvo em: {pdf_path}")