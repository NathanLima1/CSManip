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

def get_city_coords(city_name):
    geolocator = Nominatim(user_agent="my-cds-app")
    try:
        location = geolocator.geocode(city_name)
        
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except Exception as e:
        print(f"Erro ao buscar as coordenadas: {e}")
        return None, None
    
def get_city_elevation(latitude, longitude):
    url = f"https://api.open-elevation.com/api/v1/lookup?locations={latitude},{longitude}"
    response = requests.get(url)
    data = response.json()

    if data and data['results']:
        elevation = data['results'][0]['elevation']
        return elevation
    else:
        return "Elevation data not found."

def download_era5_data(city_name: str, start_date: str, end_date: str, output_file: str, output_folder: str):
    """
    Baixa dados de temperatura do ERA5-Land para um intervalo de datas específico.

    Args:
        city_name (str): Nome da cidade escolhida para baixar os dados
        start_date (str): Data de início no formato 'YYYY-MM-DD'.
        end_date (str): Data de fim no formato 'YYYY-MM-DD'.
        output_file (str): Nome do arquivo NetCDF de saída.
    """
    
    lat, lon = get_city_coords(city_name)
    if lat is None:
        print("Download cancelado. Houve um erro ao tentar encontrar a cidade.")
        return
    
    os.makedirs(output_folder, exist_ok=True)
    
    print(f"Iniciando download para {city_name} (Lat: {lat:.2f}, Lon: {lon:.2f}) para o período de {start_date} a {end_date}...")

    c = cdsapi.Client()

    dates = pd.date_range(start=start_date, end=end_date, freq='D')

    for (year, month), days_in_month in dates.to_series().groupby([dates.year, dates.month]):

        day_list = [d.strftime('%d') for d in days_in_month]

        output_file = os.path.join(output_folder, f'data_{year}_{month:02d}.zip')

        print(f"Baixando dados para {year}-{month:02d}...")
        c.retrieve(
            'reanalysis-era5-single-levels',
            {
                'product_type': 'reanalysis',
                'format': 'netcdf',
                'variable': [
                    '2m_temperature',       # Temperatura horária para calcular min/max
                    'total_precipitation',  # Precipitação horária
                ],
                'year': str(year),
                'month': f'{month:02d}',
                'day': day_list,
                'time': [ # Precisamos de todas as horas para calcular max/min do dia
                    '00:00', '01:00', '02:00', '03:00', '04:00', '05:00',
                    '06:00', '07:00', '08:00', '09:00', '10:00', '11:00',
                    '12:00', '13:00', '14:00', '15:00', '16:00', '17:00',
                    '18:00', '19:00', '20:00', '21:00', '22:00', '23:00',
                ],
                'area': [ # Define o ponto de grade mais próximo da cidade
                    lat, lon, lat, lon,
                ],
            },
            output_file)
    
    print(f"Download concluído! Dados salvos em '{output_file}'.")

def unzip_and_merge_nc(zip_file, output_file, extract_folder):
    os.makedirs(extract_folder, exist_ok=True)

    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_folder)
    print(f"Arquivos extraídos para a pasta '{extract_folder}'.")

    nc_files = glob.glob(os.path.join(extract_folder, '*.nc'))
    print(f"Arquivos encontrados: {nc_files}")

    merged_ds = xr.open_mfdataset(nc_files)
    print("\n--- Estrutura do Arquivo Unificado ---")
    print(merged_ds)

    merged_ds.to_netcdf(output_file)
    print(f"\n Dados unificados salvos em '{output_file}'.")

    for f in nc_files:
        os.remove(f)
    os.rmdir(extract_folder)

def unzip_and_merge_all_nc(zip_folder, output_file, extract_folder):
    """
    Extrai todos os arquivos .zip de uma pasta, mescla os arquivos .nc
    contidos neles e salva o resultado em um único arquivo .nc.
    Esta versão lida com arquivos .nc de mesmo nome em zips diferentes.
    """
    os.makedirs(extract_folder, exist_ok=True)
    zip_files = glob.glob(os.path.join(zip_folder, '*.zip'))

    if not zip_files:
        print(f"Nenhum arquivo .zip encontrado na pasta '{zip_folder}'.")
        return

    # Lista para guardar os datasets de cada mês
    datasets_to_merge = []
    
    print(f"Encontrados {len(zip_files)} arquivos .zip para processar.")

    try:
        # Loop principal: processa um zip de cada vez
        for zip_file in sorted(zip_files): # Usar sorted() garante a ordem cronológica
            print(f"Processando: {os.path.basename(zip_file)}")
            
            try:
                with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                    zip_ref.extractall(extract_folder)
            except zipfile.BadZipFile:
                print(f"Aviso: O arquivo '{os.path.basename(zip_file)}' não é um arquivo zip válido. Pulando.")
                continue

            # Encontra os arquivos .nc recém-extraídos
            nc_files_in_zip = glob.glob(os.path.join(extract_folder, '*.nc'))

            if nc_files_in_zip:
                # Carrega os dados do mês atual e adiciona à lista
                ds_month = xr.open_mfdataset(nc_files_in_zip, combine='by_coords')
                ds_month = ds_month.drop_vars(['number', 'expver'], errors='ignore')
                datasets_to_merge.append(ds_month)

                # --- Limpeza Imediata ---
                # Remove os arquivos .nc para não serem sobrescritos na próxima iteração
                for f in nc_files_in_zip:
                    os.remove(f)
        
        # Se a lista não estiver vazia, concatena tudo
        if datasets_to_merge:
            print("\nUnificando os dados de todos os meses...")
            # Concatena os datasets ao longo da dimensão de tempo
            merged_ds = xr.concat(datasets_to_merge, dim='valid_time')
            
            print("\n--- Estrutura do Arquivo Unificado Final ---")
            print(merged_ds)

            # Salva o resultado final
            merged_ds.to_netcdf(output_file)
            print(f"\nDados unificados salvos com sucesso em '{output_file}'.")
            
            # Fecha o dataset
            merged_ds.close()
        else:
            print("Nenhum dado foi encontrado para unificar.")

    except Exception as e:
        print(f"\nOcorreu um erro ao unificar os arquivos .nc: {e}")

    finally:
        print("\nIniciando limpeza final...")
        # Garante que os datasets na lista sejam fechados
        for ds in datasets_to_merge:
            ds.close()
            
        # Tenta remover a pasta de extração, que agora deve estar vazia
        try:
            if not os.listdir(extract_folder): # Verifica se está vazia
                 os.rmdir(extract_folder)
                 print("Pasta de extração temporária removida.")
        except OSError as e:
            print(f"A pasta de extração '{extract_folder}' não pôde ser removida: {e}")


def see_nc_file(nc_file):
    ds = xr.open_dataset(nc_file, engine='netcdf4')

    print("--- Estrutura do Arquivo NetCDF ---")
    print(ds)

    tmax = ds['tmax']
    print("\n--- Detalhes da Variável 'tmax' ---")
    print(tmax)

    tmin = ds['tmin']
    print("\n--- Detalhes da Variável 'tmin' ---")
    print(tmin)

    temp_celsius = tmax - 273.15

    plt.figure(figsize=(12, 6))

    temp_celsius.squeeze().plot()

    plt.ylabel("Temperatura (°C)")
    plt.xlabel("Horário")
    plt.title(f"Variação da Temperatura em New York ({ds['valid_time'].dt.date.values[0]})")
    plt.grid(True, linestyle='--', alpha=0.6)

    plt.show()


def process_netcdf_to_daily_csv(nc_file, final_csv, station_name):
    """
    Abre um arquivo NetCDF com dados horários, calcula os agregados diários
    e salva diretamente em um CSV formatado.
    """
    try:
        # Abre o dataset unificado com dados horários
        ds = xr.open_dataset(nc_file)

        # 1. Calcula os agregados diários usando resample
        daily_tmax = ds['t2m'].resample(valid_time='1D').max() - 273.15
        daily_tmin = ds['t2m'].resample(valid_time='1D').min() - 273.15
        daily_precip = ds['tp'].resample(valid_time='1D').sum() * 1000

        # 2. !! CORREÇÃO AQUI !!
        # Seleciona os dados no único ponto de lat/lon para tornar o array 1-dimensional
        daily_tmax_1d = daily_tmax.isel(latitude=0, longitude=0)
        daily_tmin_1d = daily_tmin.isel(latitude=0, longitude=0)
        daily_precip_1d = daily_precip.isel(latitude=0, longitude=0)

        # 3. Cria um DataFrame do pandas com os dados agora 1-dimensionais
        df_daily = pd.DataFrame({
            'Data Medicao': daily_tmax_1d.valid_time.values,
            'PRECIPITACAO TOTAL, DIARIO(mm)': daily_precip_1d.values,
            'TEMPERATURA MAXIMA, DIARIA(°C)': daily_tmax_1d.values,
            'TEMPERATURA MINIMA, DIARIA(°C)': daily_tmin_1d.values,
            'latitude': ds['latitude'].values[0],
            'longitude': ds['longitude'].values[0]
        })

        # 4. Chama a formatação e escrita do arquivo CSV
        format_daily_csv(df_daily, final_csv, station_name)
        print("Conversão concluída com sucesso!")
        print(f"Salvo como {final_csv}")

    except FileNotFoundError:
        print(f"Erro: Arquivo '{nc_file}' não encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro durante a conversão: {e}")

def format_daily_csv(daily_data, output_file, station_name):
    """
    Formata e escreve o DataFrame com dados já diários para um arquivo CSV.
    """
    lat = daily_data['latitude'].iloc[0]
    lon = daily_data['longitude'].iloc[0]
    elevation = get_city_elevation(lat, lon)

    # Monta o texto do cabeçalho
    header_text = textwrap.dedent(f"""\
    Nome: {station_name}
    Codigo Estacao: N/A
    Latitude: {lat}
    Longitude: {lon}
    Altitude: {elevation}
    Situacao: N/A
    Data Inicial: {daily_data['Data Medicao'].min().strftime('%Y-%m-%d')}
    Data Final: {daily_data['Data Medicao'].max().strftime('%Y-%m-%d')}
    Periodicidade da Medicao: Diaria

    """)

    # Remove colunas de lat/lon antes de salvar
    daily_data_to_save = daily_data.drop(columns=['latitude', 'longitude'])

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(header_text)
        # Define as colunas na ordem desejada
        ordered_columns = ['Data Medicao', 'PRECIPITACAO TOTAL, DIARIO(mm)', 'TEMPERATURA MAXIMA, DIARIA(°C)', 'TEMPERATURA MINIMA, DIARIA(°C)']
        column_header = ";".join(ordered_columns) + ";\n"
        f.write(column_header)

        for index, row in daily_data_to_save.iterrows():
            date_str = pd.to_datetime(row['Data Medicao']).strftime('%Y-%m-%d')
            # Converte o ponto decimal para vírgula
            precip_str = f"{row['PRECIPITACAO TOTAL, DIARIO(mm)']:.5f}".replace('.', ',')
            tmax_str = f"{row['TEMPERATURA MAXIMA, DIARIA(°C)']:.4f}".replace('.', ',')
            tmin_str = f"{row['TEMPERATURA MINIMA, DIARIA(°C)']:.4f}".replace('.', ',')
            
            line = f"{date_str};{precip_str};{tmax_str};{tmin_str};\n"
            f.write(line)

def download_and_process_era_data(city, start_date, end_date):
    city_folder_name = f"data_{city.split(',')[0].replace(' ', '_')}"

    print("="*30)
    print(f"Iniciando processo para a cidade: {city}")
    print("="*30)
    
    download_era5_data(
        city_name=city,
        start_date=start_date, 
        end_date=end_date,
        output_file=f'dados_{city_folder_name}.zip',
        output_folder=city_folder_name
    )

    unzip_and_merge_all_nc(city_folder_name, 'dados_unificados.nc', 'saida')
    
    # Chamada para a nova função única que processa e cria o CSV
    process_netcdf_to_daily_csv("dados_unificados.nc", f"{city}.csv", f"{city}")

    print(f"\n--- Limpando arquivos temporários para {city} ---")
    try:
        shutil.rmtree(city_folder_name)
        os.remove('dados_unificados.nc')
        print("Limpeza concluída com sucesso!")
    except OSError as e:
        print(f"Erro durante a limpeza: {e}")
    print("\n")
