import cdsapi
import pandas as pd 
from geopy.geocoders import Nominatim
import zipfile
import glob
import xarray as xr
import os
import matplotlib.pyplot as plt

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

def unzip_and_merge_all_nc(zip_folder, output_file, extract_folder):
    """
    Extrai todos os arquivos .zip de uma pasta, mescla os arquivos .nc 
    contidos neles e salva o resultado em um único arquivo .nc
    """
    os.makedirs(extract_folder, exist_ok=True)
    zip_files = glob.glob(os.path.join(zip_folder, '*.zip'))

    if not zip_files:
        print(f"Nenhum arquivo .zip encontrado na pasta '{zip_folder}'.")
        return
    
    for zip_file in zip_files:
        try:
            with zipfile.ZipFile(zipfile, 'r') as zip_ref:
                zip_ref.extractall(extract_folder)
            print(f"Arquivo '{os.path.basename(zip_file)}' extraído com sucesso.")
        except zipfile.BadZipFile:
            print(f"Aviso: O arquivo '{os.path.basename(zipfile)}' não é um arquivo zip válido.")

        nc_files = glob.glob(os.path.join(extract_folder, '*.nc'))

        if not nc_files:
            print(f"Nenhum arquivo .nc encontrado na pasta de extração '{extract_folder}'.")
            os.rmdir(extract_folder)
            return
        
        print(f"\nEncontrados {len(nc_files)} arquivos .nc para unificar.")

        try:
            merged_ds = xr.open_mfdataset(nc_files, combine='by_coords')
            print("\n--- Estrutura do Arquivo Unificado ---")
            print(merged_ds)

            # 6. Salva o dataset unificado em um novo arquivo NetCDF.
            merged_ds.to_netcdf(output_file)
            print(f"\nDados unificados salvos com sucesso em '{output_file}'.")

        except Exception as e:
            print(f"\nOcorreu um erro ao unificar os arquivos .nc: {e}")

        finally:
            print("\nIniciando limmpeza dos arquivos temporários...")
            if 'merged_ds' in locals():
                merged_ds.close()

            for f in nc_files:
                try:
                    os.remove(f)
                except OSError as e:
                    print(f"Erro ao remover o arquivo {f}: {e}")

            try:
                os.rmdir(extract_folder)
                print("Limpeza concluída.")
            except OSError as e:
                print(f"A pasta de extração '{extract_folder}' não está vazia ou não pôde ser removida: {e}")
                
def add_min_max_temp_nc(nc_file):
    try:
        ds = xr.open_dataset(nc_file)
        print("--- 1. Estrutura do Dataset Original ---")
        print(ds)
    except FileNotFoundError:
        print("Erro: Arquivo 'dados_unificados.nc' não encontrado.")
        print("Por favor, execute o script de download e unificação primeiro.")
        exit()

    daily_max_temp = ds['t2m'].resample(valid_time='1D').max()
    daily_min_temp = ds['t2m'].resample(valid_time='1D').min()
    daily_mean_temp = ds['t2m'].resample(valid_time='1D').mean()

    ds['tmax'] = daily_max_temp
    ds['tmin'] = daily_min_temp
    ds['tmean'] = daily_mean_temp

    ds_final = ds.drop_vars('t2m')

    temp_vars = ['tmax', 'tmin', 'tmean']

    for var in temp_vars:
        ds_final[var] = ds_final[var] - 273.15
        ds_final[var].attrs['units'] = 'C'
    print("\n--- Estrutura do Dataset Final (Após Adicionar e Remover Variáveis) ---")
    print(ds_final)
    ds_final.to_netcdf("dados_finais.nc")


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

def format_csv(input_file, output_file, station_name):
    try:
        df_input = pd.read_csv(input_file)
    except FileNotFoundError:
        print("Erro arquivo não encontrado", input_file)

    try:
        df_input['valid_time'] = pd.to_datetime(df_input['valid_time'])

        df_input['date'] = df_input['valid_time'].dt.date

        df_input['tmax'] = df_input['tmax'].fillna(method='ffill').fillna(method='bfill')
        df_input['tmin'] = df_input['tmin'].fillna(method='ffill').fillna(method='bfill')

        daily_data = df_input.groupby('date').agg({
            'tp': 'max',
            'tmax': 'max',
            'tmin': 'min'
        }).reset_index()

        daily_data.rename(columns={
            'date': 'Data Medicao',
            'tp': 'PRECIPITACAO TOTAL, DIARIO(mm)',
            'tmax': 'TEMPERATURA MAXIMA, DIARIA(°C)',
            'tmin': 'TEMPERATURA MINIMA, DIARIA(°C)'
        }, inplace=True)
    
    except KeyError as e:
        print(f"ERRO: Uma coluna esperada não foi encontrada: {e}")
        print("Por favor, verifique se os nomes das colunas no seu arquivo csv correspondem ao formato adequados.")
        exit()

    lat = df_input['latitude'].iloc[0]
    lon = df_input['longitude'].iloc[0]

    # Monta o texto do cabeçalho
    header_text = f"""Nome: {station_name}
    Codigo Estacao: N/A
    Latitude: {lat}
    Longitude: {lon}
    Altitude: N/A
    Situacao: N/A
    Data Inicial: {daily_data['Data Medicao'].min()}
    Data Final: {daily_data['Data Medicao'].max()}
    Periodicidade da Medicao: Diaria

    """

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(header_text)
        column_header = ";".join(daily_data.columns) + ";\n"
        f.write(column_header)

        for index, row in daily_data.iterrows():
            date_str = row['Data Medicao'].strftime('%Y-%m-%d')
            # Converte o ponto decimal para vírgula
            precip_str = f"{row['PRECIPITACAO TOTAL, DIARIO(mm)']:.5f}".replace('.', ',')
            tmax_str = f"{row['TEMPERATURA MAXIMA, DIARIA(°C)']:.4f}".replace('.', ',')
            tmin_str = f"{row['TEMPERATURA MINIMA, DIARIA(°C)']:.4f}".replace('.', ',')
            
            line = f"{date_str};{precip_str};{tmax_str};{tmin_str};\n"
            f.write(line)

def convert_nc_to_csv(nc_file, final_csv, station_name):
    try:
        ds = xr.open_dataset(nc_file)
        df = ds.to_dataframe()
        df = df.reset_index()
        df.to_csv('temp.csv', index=False)

        format_csv('temp.csv', final_csv, station_name)
        print("Conversão concluída com sucesso!")
        print(f"Salvo como {final_csv}")

    except FileNotFoundError:
        print("Erro arquivo não encontrado. Certifique-se que o nome está correto.")
    except Exception as e:
        print(f"Ocorreu um erro durante a conversão: {e}")

if __name__ == '__main__':
    # --- AQUI VOCÊ MUDA A CIDADE ---
    cidade_desejada = "Amsterdam, Netherlands"
    download_era5_data(
        city_name=cidade_desejada,
        start_date='2024-05-01', 
        end_date='2024-06-01', # O código atual está simplificado para um dia
        output_file=f'dados_{cidade_desejada.split(",")[0].replace(" ", "_")}.zip',
        output_folder='NewYork'
    )
    zip_path = "NewYork/data_2024_05.zip"
    unzip_and_merge_nc(zip_path, 'dados_unificados.nc', 'saida')
    add_min_max_temp_nc("dados_unificados.nc")
    convert_nc_to_csv("dados_finais.nc", "Amsterdam.csv", "Amsterdam")