import os
import json
import urllib.request
from pathlib import Path

GITHUB_USER = "NathanLima1"
REPO_NAME = "CSManip"
FOLDER_PATH = "src/csmanip/datasets/data" 
BRANCH = "main"
API_URL = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}/contents/{FOLDER_PATH}?ref={BRANCH}"
RAW_BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/{FOLDER_PATH}"

def download_all_datasets():
    """
    Consulta a API do GitHub para listar arquivos na pasta e baixa todos os CSVs.
    """
    cache_dir = Path.home() / ".csmanip_data"
    cache_dir.mkdir(exist_ok=True)
    
    print(f"Verificando arquivos no GitHub em: {FOLDER_PATH}...")

    try:
        with urllib.request.urlopen(API_URL) as response:
            files_list = json.loads(response.read().decode())
    except Exception as e:
        raise RuntimeError(f"Erro ao listar arquivos do GitHub. Verifique a internet ou o limite da API.\nErro: {e}")

    downloaded_files = []

    for file_info in files_list:
        file_name = file_info['name']
        
        if file_name.endswith('.csv'):
            local_path = cache_dir / file_name
            if local_path.exists():
                downloaded_files.append(str(local_path))
                continue
            
            remote_url = f"{RAW_BASE_URL}/{file_name}"
            print(f"Baixando: {file_name}...")
            
            try:
                urllib.request.urlretrieve(remote_url, local_path)
                downloaded_files.append(str(local_path))
            except Exception as e:
                print(f"Falha ao baixar {file_name}: {e}")
                if local_path.exists():
                    os.remove(local_path)

    print("Todos os datasets estão prontos!")
    return downloaded_files