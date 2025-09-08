import requests
from geopy.geocoders import Nominatim
import csv
import io
from datetime import datetime

BASE_URL = "https://www.ncdc.noaa.gov/cdo-web/api/v2/"

headers = {
    "token": "XUygEwyqWKimCiNWLQfhKwIHIrrXKVNp"
}

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

def find_stations(lat, lon):
    radius = 0.5
    extent = f"{lat-radius},{lon-radius},{lat+radius},{lon+radius}"

    params = {
        "datasetid": "GHCND",
        "extent": extent,
        "limit": 10
    }

    try:
        response = requests.get(f"{BASE_URL}stations", headers=headers, params=params)
        response.raise_for_status()

        stations = response.json().get('results', [])

        if not stations:
            print("Nenhuma estação encontrada na área especificada.")
            return None
        
        stations.sort(key=lambda x: x['maxdate'], reverse=True)
        
        print(f"Encontradas {len(stations)} estações. A mais recente reportou dados em: {stations[0]['maxdate']}")
        return stations
    
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar estações: {e}")
        return None
    
def get_dly_climate_data_for_station(stationid, startdate, enddate, verbose):
    """
    Obtém os dados climáticos diários (TMIN, TMAX, PRCP) para uma estação
    específica dentro de um intervalo de datas, no formato CSV.
    """

    # Limpa o ID da estação se ele tiver um prefixo como 'GHCND:'
    if str(stationid).count(':') == 1: 
        stationid = str(stationid).partition(":")[2]

    # Converte as strings de data para objetos datetime, removendo a parte do tempo se houver
    if isinstance(startdate, str):
        if 'T' in startdate: 
            startdate = startdate.partition("T")[0]
        start = datetime.strptime(startdate, "%Y-%m-%d")
    else:
        start = startdate

    if isinstance(enddate, str):
        if 'T' in enddate: 
            enddate = enddate.partition("T")[0]
        end = datetime.strptime(enddate, "%Y-%m-%d")
    else:
        end = enddate

    if start > end: 
        raise Exception(f"ERRO: A data de início {start} é posterior à data de fim {end}")

    # Formata as datas para a URL da API
    startdate_str = start.strftime("%Y-%m-%d")
    enddate_str = end.strftime("%Y-%m-%d")

    url = (f"https://www.ncei.noaa.gov/access/services/data/v1?dataset=daily-summaries"
           f"&dataTypes=TMIN,TMAX,PRCP&stations={stationid}&startDate={startdate_str}"
           f"&endDate={enddate_str}&format=csv&units=standard&includeAttributes=false")
    
    if verbose: 
        print("URL:", url)
    
    headers = {'token': "XUygEwyqWKimCiNWLQfhKwIHIrrXKVNp"}
    
    try:
        req = requests.get(url, headers=headers)
    except Exception as e:
        print(f"ERRO de conexão: {repr(e)} na URL: {url}")
        return None
    
    if req.status_code != 200:
        print(f"\tERRO: Código de status {req.status_code} - {req.text}")
        return None

    # Ler resposta CSV
    csv_data = []
    reader = csv.DictReader(io.StringIO(req.text))
    for row in reader:
        csv_data.append({
            "DATE": row.get("DATE", "N/A"),
            "TMIN": row.get("TMIN", None),
            "TMAX": row.get("TMAX", None),
            "PRCP": row.get("PRCP", None)
        })

    return csv_data

def salvar_dados_climaticos_csv(dados, nome_arquivo, info_estacao):
    """
    Salva os dados climáticos em um arquivo CSV no formato do 'BeloHorizonte.csv'.

    :param dados: Lista de dicionários com os dados climáticos.
    :param nome_arquivo: Nome do arquivo CSV a ser criado (ex: 'clima_cidade.csv').
    :param info_estacao: Dicionário com as informações da estação.
    """
    with open(nome_arquivo, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')

        # Escreve o cabeçalho com as informações da estação
        writer.writerow([f"Nome: {info_estacao.get('nome', '')}"])
        writer.writerow([f"Codigo Estacao: {info_estacao.get('id', '')}"])
        writer.writerow([f"Latitude: {info_estacao.get('latitude', '')}"])
        writer.writerow([f"Longitude: {info_estacao.get('longitude', '')}"])
        writer.writerow([f"Altitude: {info_estacao.get('elevation', '')}"])
        writer.writerow(["Situacao: Operante"]) # Assumindo como operante
        writer.writerow([f"Data Inicial: {info_estacao.get('data_inicial', '')}"])
        writer.writerow([f"Data Final: {info_estacao.get('data_final', '')}"])
        writer.writerow(["Periodicidade da Medicao: Diaria"])
        writer.writerow([]) # Linha em branco

        # Escreve o cabeçalho das colunas de dados
        writer.writerow([
            "Data Medicao",
            "PRECIPITACAO TOTAL, DIARIO(mm)",
            "TEMPERATURA MAXIMA, DIARIA(°C)",
            "TEMPERATURA MINIMA, DIARIA(°C)",
            "" # Adiciona uma coluna extra para o ; no final
        ])

        # Escreve os dados, fazendo a conversão de unidades
        for linha in dados:
            try:
                # Converte Precipitação de polegadas para milímetros
                prcp_mm = float(linha['PRCP']) * 25.4 if linha['PRCP'] else ''
                # Converte Temperatura de Fahrenheit para Celsius
                tmax_c = (float(linha['TMAX']) - 32) * 5/9 if linha['TMAX'] else ''
                tmin_c = (float(linha['TMIN']) - 32) * 5/9 if linha['TMIN'] else ''

                # Formata a data para o padrão do arquivo
                data_medicao = datetime.strptime(linha['DATE'], '%Y-%m-%d').strftime('%Y-%m-%d')
                
                # Formata os números com vírgula como separador decimal
                prcp_str = f"{prcp_mm:.1f}".replace('.', ',') if prcp_mm != '' else ''
                tmax_str = f"{tmax_c:.1f}".replace('.', ',') if tmax_c != '' else ''
                tmin_str = f"{tmin_c:.1f}".replace('.', ',') if tmin_c != '' else ''
                
                writer.writerow([data_medicao, prcp_str, tmax_str, tmin_str, ''])

            except (ValueError, TypeError) as e:
                print(f"Aviso: Não foi possível processar a linha: {linha}. Erro: {e}")

if __name__ == "__main__":
    city = "New York, US"
    
    start_date = "2023-01-01"
    end_date = "2023-12-31"
    dados_climaticos = get_dly_climate_data_for_station("GHCND:USC00477132", start_date, end_date, verbose=True)

    if dados_climaticos:
        # 3. Preparar informações da estação e salvar no CSV
        info_estacao = {
            'nome': 'Lock and Dam N.4, US',
            'id': "GHCND:USC00470124",
            'latitude': "38",
            'longitude': "84",
            'elevation': "143",
            'data_inicial': start_date,
            'data_final': end_date
        }
        
        nome_do_arquivo_csv = "LockDam.csv"
        salvar_dados_climaticos_csv(dados_climaticos, nome_do_arquivo_csv, info_estacao)
        
        print(f"\nDados salvos com sucesso no arquivo '{nome_do_arquivo_csv}'")
    

    