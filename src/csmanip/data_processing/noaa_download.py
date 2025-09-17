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

def find_stations(lat, lon, limit, required_types, radius):
    extent = f"{lat-radius},{lon-radius},{lat+radius},{lon+radius}"

    params = {
        "datasetid": "GHCND",
        "extent": extent,
        "limit": limit,
        "datatypeid": required_types,
        "sortfield": "maxdate",
        "sortorder": "desc"
    }

    try:
        response = requests.get(f"{BASE_URL}stations", headers=headers, params=params)
        response.raise_for_status()

        stations = response.json().get('results', [])

        if not stations:
            print("Nenhuma estação encontrada na área especificada.")
            return None
        
        #stations.sort(key=lambda x: x['maxdate'], reverse=True)
        
        print(f"Encontradas {len(stations)} estações. A mais recente reportou dados em: {stations[0]['maxdate']}")
        return stations
    
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar estações: {e}")
        return None
    
def get_available_datatypes(station_id, start_date, end_date):
    """
    Identifica os tipos de dados presentes naquela estação
    """
    params = {
        "datasetid": "GHCND",
        "stationid": station_id,
        "startdate": start_date,
        "enddate": end_date,
        "limit": 200
    }

    try:
        response = requests.get(f"{BASE_URL}datatypes", headers=headers, params=params)
        response.raise_for_status()

        data_types = response.json().get('results', [])

        if not data_types:
            print(f"Nenhum tipo de dado encontrado para a estação {station_id} no período especificado.")
            return None
        
        return data_types
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar os tipos de dados: {e}")
        return None
    

def check_station_data_types(station_id, required_types, start_date, end_date):
    """
    Verifica se uma estação possui um conjunto específico de tipos de dados
    e imprime um status detalhado para cada um.
    """
    status_check = {key: False for key in required_types}

    available_types = get_available_datatypes(station_id, start_date, end_date)
    
    if available_types:
        available_ids = {dtype['id'] for dtype in available_types}
        for data_type in status_check:
            if data_type in available_ids:
                status_check[data_type] = True

    print("--- Status de disponibilidade dos dados:")
    for data_type, is_available in status_check.items():
        if is_available:
            print(f"    - {data_type}: ✔️ Disponível")
        else:
            print(f"    - {data_type}: ❌ Indisponível")

    return all(status_check.values())        
    
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

def download_noaa_data(city, start_date, end_date, radius=0.5):
    """
    Função principal que cuida de encontrar a estação baseando se na cidade,
    checa os tipos de dados disponíveis naquela estação e baixa
    """
    required_types = ["TMIN", "TMAX", "PRCP"]
    lat, lon = get_city_coords(city)
    print(lat, lon)
    if lat is None or lon is None:
        print("Não foi possível encontrar coordenadas para {city}. Verifique a escrita e formato, ela deve estar nesse formato 'New York, US'.")
    
    print(f"Buscando estações perto de {city} (Lat: {lat}, Lon: {lon}) que tenham TMIN, TMAX e PRCP...")

    stations = find_stations(lat, lon, 10, required_types, radius)
    if not stations:
        print("Não foi possível encontrar uma estação adequada, tente aumentar o raio de busca e verificar o período das datas.")
    found_station = False

    for station in stations:
        dtypes = check_station_data_types(station['id'], required_types, start_date, end_date)
        if dtypes:
            found_station = True
            station_info = {
                'nome': station['name'],
                'id': station['id'],
                'latitude': station.get('latitude', lat),
                'longitude': station.get('longitude', lon),
                'elevation':station.get('elevation', 'N/A'),
                'data_inicial': start_date,
                'data_final': end_date
            }
            station_id = station['id']
            data = get_dly_climate_data_for_station(station_id, start_date, end_date, verbose=True)

            if data:
                temp_name = city.split(",")[0].replace(" ", "")
                file_name = f"{temp_name}.csv"
                print("Nome do arquivo:", file_name)
                salvar_dados_climaticos_csv(data, file_name, station_info)
                break
            else:
                print("Erro ao baixar os dados da estação:", station_id)

    if not found_station:
        print("Não foi possível encontrar uma estação com todos os dados necessários")
