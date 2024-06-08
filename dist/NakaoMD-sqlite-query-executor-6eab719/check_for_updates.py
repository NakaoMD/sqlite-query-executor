import requests
import os
import zipfile
import sys
import logging

# Configurar logging
logging.basicConfig(filename='app_debug.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

# URL para a API de Releases do GitHub
repo = "NakaoMD/sqlite-query-executor"
releases_url = f"https://api.github.com/repos/{repo}/releases/latest"

# Caminho para o arquivo local de versão
local_version_file = "version.txt"

def get_latest_release_info():
    logging.debug("Verificando informações do último release...")
    response = requests.get(releases_url)
    response.raise_for_status()
    release_info = response.json()
    return release_info

def download_and_extract_zip(url, extract_to='.'):
    logging.debug(f"Baixando atualização de {url}...")
    response = requests.get(url, stream=True)
    zip_path = os.path.join(extract_to, "update.zip")
    with open(zip_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=128):
            f.write(chunk)
    logging.debug("Extraindo atualização...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    os.remove(zip_path)
    logging.debug("Atualização concluída.")

def check_for_updates():
    release_info = get_latest_release_info()
    remote_version = release_info['tag_name']
    logging.debug(f"Versão remota: {remote_version}")

    if os.path.exists(local_version_file):
        with open(local_version_file, 'r') as f:
            local_version = f.read().strip()
    else:
        local_version = "0.0.0"

    logging.debug(f"Versão local: {local_version}")

    if remote_version != local_version:
        logging.debug("Nova versão disponível!")
        asset = next(item for item in release_info['assets'] if item['name'] == 'query_executor.zip')
        download_and_extract_zip(asset['browser_download_url'])
        with open(local_version_file, 'w') as f:
            f.write(remote_version)
        logging.debug("Atualização concluída. Reinicie o aplicativo.")
    else:
        logging.debug("Você já está usando a versão mais recente.")

if __name__ == "__main__":
    try:
        check_for_updates()
    except Exception as e:
        logging.error(f"Erro ao verificar atualizações: {e}")
