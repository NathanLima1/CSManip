import requests
from geopy.geocoders import Nominatim
import csv
import io
from datetime import datetime
import folium
import webbrowser
from folium.map import Popup
import os


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

def create_station_map_and_get_choice(stations):
    """
    Cria um mapa Folium com as estações, exibe no console uma lista numerada
    e pede ao usuário para escolher uma.

    :param stations: Lista de dicionários das estações válidas.
    :return: O dicionário da estação escolhida pelo usuário, ou None se a escolha for inválida.
    """
    if not stations:
        return None

    # Define o local inicial do mapa como a localização da primeira estação
    map_center = [stations[0]['latitude'], stations[0]['longitude']]
    m = folium.Map(location=map_center, zoom_start=10)

    print("\n--- Estações encontradas com todos os dados necessários ---")
    
    for i, station in enumerate(stations):
        station_id_display = i + 1
        popup_html = (f"<b>ID de Escolha: {station_id_display}</b><br>"
                      f"Nome: {station['name']}<br>"
                      f"ID Oficial: {station['id']}<br>"
                      f"Lat: {station['latitude']}, Lon: {station['longitude']}")
        
        folium.Marker(
            location=[station['latitude'], station['longitude']],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"Escolha #{station_id_display}"
        ).add_to(m)
        
        # Imprime a opção no console
        print(f"  [{station_id_display}] {station['name']} (ID: {station['id']})")

    map_file = 'stations_map.html'
    m.save(map_file)
    print(f"\nMapa com as estações foi salvo como '{map_file}' e será aberto no seu navegador.")
    webbrowser.open('file://' + os.path.realpath(map_file))

    while True:
        try:
            choice = int(input("Digite o número da estação que deseja baixar (ex: 1): "))
            if 1 <= choice <= len(stations):
                return stations[choice - 1]
            else:
                print("Opção inválida. Por favor, escolha um número da lista.")
        except ValueError:
            print("Entrada inválida. Por favor, digite apenas o número.")

def download_noaa_data(city, start_date, end_date, radius=0.5):
    """
    Função principal modificada para encontrar todas as estações válidas,
    mostrar um mapa e permitir que o usuário escolha qual baixar.
    """
    required_types = ["TMIN", "TMAX", "PRCP"]
    lat, lon = get_city_coords(city)
    
    if lat is None or lon is None:
        print(f"Não foi possível encontrar coordenadas para '{city}'. Verifique a escrita (formato 'Cidade, País' ou 'Cidade, Estado').")
        return
    
    print(f"Buscando estações perto de {city} (Lat: {lat:.4f}, Lon: {lon:.4f})...")

    candidate_stations = find_stations(lat, lon, 50, required_types, radius)
    if not candidate_stations:
        print("Não foi possível encontrar estações candidatas. Tente aumentar o raio de busca ou verificar o período das datas.")
        return

    # Filtra apenas as estações que têm os dados para o período exato
    valid_stations = []
    for station in candidate_stations:
        if check_station_data_types(station['id'], required_types, start_date, end_date):
            valid_stations.append(station)
            print(f"  ✔️ Estação '{station['name']}' ({station['id']}) possui os dados necessários.")
        else:
            print(f"  ❌ Estação '{station['name']}' ({station['id']}) não possui todos os dados para o período completo.")


    if not valid_stations:
        print("\nNenhuma estação na área continha todos os tipos de dados (TMIN, TMAX, PRCP) para o período solicitado.")
        print("Tente um período de datas diferente ou aumente o raio de busca.")
        return

    # Mostra o mapa e a lista para o usuário escolher
    chosen_station = create_station_map_and_get_choice(valid_stations)

    if chosen_station:
        print(f"\nEstação escolhida: '{chosen_station['name']}' ({chosen_station['id']})")
        
        station_info = {
            'nome': chosen_station['name'],
            'id': chosen_station['id'],
            'latitude': chosen_station.get('latitude', lat),
            'longitude': chosen_station.get('longitude', lon),
            'elevation': chosen_station.get('elevation', 'N/A'),
            'data_inicial': start_date,
            'data_final': end_date
        }
        
        data = get_dly_climate_data_for_station(chosen_station['id'], start_date, end_date, verbose=True)

        if data:
            temp_name = city.split(",")[0].replace(" ", "")
            file_name = f"{temp_name}_{chosen_station['id'].replace(':', '_')}.csv"
            salvar_dados_climaticos_csv(data, file_name, station_info)
        else:
            print(f"Erro ao baixar os dados da estação escolhida: {chosen_station['id']}")


