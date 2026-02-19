import cdsapi
import pandas as pd 
from geopy.geocoders import Nominatim
import zipfile
import glob
import xarray as xr
import os
import matplotlib.pyplot as plt
import requests
import textwrap
import shutil
import sys 


def get_city_coords(city_name, logger=print):
    """Obtém coordenadas da cidade."""
    geolocator = Nominatim(user_agent="my-cds-app", timeout=10)
    try:
        location = geolocator.geocode(city_name)
        if location:
            return location.latitude, location.longitude
        else:
            logger(f"Aviso: Não foi possível encontrar coordenadas para {city_name}.")
            return None, None
    except Exception as e:
        logger(f"Erro ao buscar as coordenadas: {e}")
        return None, None
    
def get_city_elevation(latitude, longitude, logger=print):
    """Obtém elevação das coordenadas."""
    url = f"https://api.open-elevation.com/api/v1/lookup?locations={latitude},{longitude}"
    try:
        response = requests.get(url)
        data = response.json()
        if data and data['results']:
            elevation = data['results'][0]['elevation']
            return elevation
        else:
            logger("Dados de elevação não encontrados.")
            return "Elevation data not found."
    except Exception as e:
        logger(f"Erro ao buscar elevação: {e}")
        return "Error fetching elevation"

# --- Funções de Processamento com logger ---

def download_era5_data(city_name: str, start_date: str, end_date: str, output_folder: str, logger=print):
    """Baixa os dados do ERA5-Land para a pasta de saída especificada."""
    
    lat, lon = get_city_coords(city_name, logger)
    if lat is None:
        logger("Download cancelado. Houve um erro ao tentar encontrar a cidade.")
        return False # Indica falha
    
    # Garante que a pasta de saída exista
    os.makedirs(output_folder, exist_ok=True)
    
    logger(f"Iniciando download para {city_name} (Lat: {lat:.2f}, Lon: {lon:.2f}) para o período de {start_date} a {end_date}...")

    c = cdsapi.Client()
    dates = pd.date_range(start=start_date, end=end_date, freq='D')

    for (year, month), days_in_month in dates.to_series().groupby([dates.year, dates.month]):
        day_list = [d.strftime('%d') for d in days_in_month]
        output_file_month = os.path.join(output_folder, f'data_{year}_{month:02d}.zip')

        logger(f"Baixando dados para {year}-{month:02d}...")
        try:
            c.retrieve(
                'reanalysis-era5-single-levels',
                {
                    'product_type': 'reanalysis', 'format': 'netcdf',
                    'variable': ['2m_temperature', 'total_precipitation'],
                    'year': str(year), 'month': f'{month:02d}', 'day': day_list,
                    'time': ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00',
                             '06:00', '07:00', '08:00', '09:00', '10:00', '11:00',
                             '12:00', '13:00', '14:00', '15:00', '16:00', '17:00',
                             '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'],
                    'area': [lat, lon, lat, lon],
                },
                output_file_month
            )
        except Exception as e:
            logger(f"ERRO: Falha ao baixar dados para {year}-{month:02d}. Erro: {e}")
            return False # Indica falha
    
    logger(f"Download concluído! Dados salvos em '{output_folder}'.")
    return True # Indica sucesso

def unzip_and_merge_all_nc(zip_folder, output_nc_file, extract_folder, logger=print):
    """Extrai e mescla todos os .nc de uma pasta de zips."""
    os.makedirs(extract_folder, exist_ok=True)
    zip_files = glob.glob(os.path.join(zip_folder, '*.zip'))

    if not zip_files:
        logger(f"Nenhum arquivo .zip encontrado na pasta '{zip_folder}'.")
        return

    datasets_to_merge = []
    logger(f"Encontrados {len(zip_files)} arquivos .zip para processar.")

    try:
        for zip_file in sorted(zip_files):
            logger(f"Processando: {os.path.basename(zip_file)}")
            try:
                with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                    zip_ref.extractall(extract_folder)
            except zipfile.BadZipFile:
                logger(f"Aviso: O arquivo '{os.path.basename(zip_file)}' não é um zip válido. Pulando.")
                continue

            nc_files_in_zip = glob.glob(os.path.join(extract_folder, '*.nc'))
            if nc_files_in_zip:
                ds_month = xr.open_mfdataset(nc_files_in_zip, combine='by_coords', engine='netcdf4')
                ds_month = ds_month.drop_vars(['number', 'expver'], errors='ignore')
                datasets_to_merge.append(ds_month)
                for f in nc_files_in_zip:
                    os.remove(f)
        
        if datasets_to_merge:
            logger("\nUnificando os dados de todos os meses...")
            merged_ds = xr.concat(datasets_to_merge, dim='valid_time')
            logger("\n--- Estrutura do Arquivo Unificado Final ---")
            logger(str(merged_ds)) # Converte para string para logar
            merged_ds.to_netcdf(output_nc_file)
            logger(f"\nDados unificados salvos com sucesso em '{output_nc_file}'.")
            merged_ds.close()
        else:
            logger("Nenhum dado foi encontrado para unificar.")
    except Exception as e:
        logger(f"\nOcorreu um erro ao unificar os arquivos .nc: {e}")
        raise # Re-levanta o erro para a GUI
    finally:
        logger("\nIniciando limpeza final dos .nc...")
        for ds in datasets_to_merge:
            ds.close()
        try:
            if os.path.exists(extract_folder) and not os.listdir(extract_folder):
                 os.rmdir(extract_folder)
                 logger("Pasta de extração temporária removida.")
        except OSError as e:
            logger(f"A pasta de extração '{extract_folder}' não pôde ser removida: {e}")

def process_netcdf_to_daily_csv(nc_file, final_csv, station_name, logger=print):
    """Converte o arquivo .nc unificado em um CSV formatado."""
    try:
        ds = xr.open_dataset(nc_file)

        daily_tmax = (ds['t2m'].resample(valid_time='1D').max() - 273.15).isel(latitude=0, longitude=0)
        daily_tmin = (ds['t2m'].resample(valid_time='1D').min() - 273.15).isel(latitude=0, longitude=0)
        daily_precip = (ds['tp'].resample(valid_time='1D').sum() * 1000).isel(latitude=0, longitude=0)

        df_daily = pd.DataFrame({
            'Data Medicao': daily_tmax.valid_time.values,
            'PRECIPITACAO TOTAL, DIARIO(mm)': daily_precip.values,
            'TEMPERATURA MAXIMA, DIARIA(°C)': daily_tmax.values,
            'TEMPERATURA MINIMA, DIARIA(°C)': daily_tmin.values,
            'latitude': ds['latitude'].values[0],
            'longitude': ds['longitude'].values[0]
        })

        format_daily_csv(df_daily, final_csv, station_name, logger=logger) # Passa o logger
        logger(f"Conversão para CSV concluída com sucesso! Salvo como {final_csv}")

    except FileNotFoundError:
        logger(f"Erro: Arquivo '{nc_file}' não encontrado.")
        raise
    except Exception as e:
        logger(f"Ocorreu um erro durante a conversão: {e}")
        raise

def format_daily_csv(daily_data, output_file, station_name, logger=print):
    """Formata e escreve o DataFrame diário para o arquivo CSV final."""
    lat = daily_data['latitude'].iloc[0]
    lon = daily_data['longitude'].iloc[0]
    elevation = get_city_elevation(lat, lon, logger=logger) # Passa o logger

    header_text = textwrap.dedent(f"""\
    Nome: {station_name}
    Codigo Estacao: ERA5-Land
    Latitude: {lat}
    Longitude: {lon}
    Altitude: {elevation}
    Situacao: N/A
    Data Inicial: {daily_data['Data Medicao'].min().strftime('%Y-%m-%d')}
    Data Final: {daily_data['Data Medicao'].max().strftime('%Y-%m-%d')}
    Periodicidade da Medicao: Diaria

    """)

    daily_data_to_save = daily_data.drop(columns=['latitude', 'longitude'])

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(header_text)
        ordered_columns = ['Data Medicao', 'PRECIPITACAO TOTAL, DIARIO(mm)', 'TEMPERATURA MAXIMA, DIARIA(°C)', 'TEMPERATURA MINIMA, DIARIA(°C)']
        column_header = ";".join(ordered_columns) + ";\n"
        f.write(column_header)

        for index, row in daily_data_to_save.iterrows():
            date_str = pd.to_datetime(row['Data Medicao']).strftime('%Y-%m-%d')
            precip_str = f"{row['PRECIPITACAO TOTAL, DIARIO(mm)']:.5f}".replace('.', ',')
            tmax_str = f"{row['TEMPERATURA MAXIMA, DIARIA(°C)']:.4f}".replace('.', ',')
            tmin_str = f"{row['TEMPERATURA MINIMA, DIARIA(°C)']:.4f}".replace('.', ',')
            line = f"{date_str};{precip_str};{tmax_str};{tmin_str};\n"
            f.write(line)


def download_and_process_era_data(city, start_date, end_date, output_dir, logger=print):
    """
    Função principal que orquestra todo o processo de download e conversão.
    Todos os arquivos são salvos DENTRO do output_dir.
    """
    
    city_slug = city.split(',')[0].replace(' ', '_').lower()
    temp_download_folder = os.path.join(output_dir, f"temp_zip_{city_slug}")
    temp_extract_folder = os.path.join(output_dir, "temp_extract")
    unified_nc_file = os.path.join(output_dir, f"{city_slug}_unificado.nc")
    final_csv_file = os.path.join(output_dir, f"ECMWF_{city_slug}_{start_date}_to_{end_date}.csv") # Nome de arquivo final claro

    os.makedirs(temp_download_folder, exist_ok=True)
    os.makedirs(temp_extract_folder, exist_ok=True)

    logger("="*30)
    logger(f"Iniciando processo para a cidade: {city}")
    logger("="*30)
    
    success = download_era5_data(
        city_name=city,
        start_date=start_date, 
        end_date=end_date,
        output_folder=temp_download_folder,
        logger=logger
    )
    
    if not success:
        logger("Falha na etapa de download. Abortando.")
        return 

    unzip_and_merge_all_nc(
        temp_download_folder, 
        unified_nc_file, 
        temp_extract_folder, 
        logger=logger
    )
    
    process_netcdf_to_daily_csv(
        unified_nc_file, 
        final_csv_file, 
        city,
        logger=logger
    )

    logger(f"\n--- Limpando arquivos temporários para {city} ---")
    try:
        shutil.rmtree(temp_download_folder)
        shutil.rmtree(temp_extract_folder)
        os.remove(unified_nc_file)
        logger("Limpeza concluída com sucesso!")
    except OSError as e:
        logger(f"Erro durante a limpeza: {e}")
    logger("\nProcesso finalizado.")