import requests
import zipfile
import io

REPO_URL = "https://api.github.com/repos/NakaoMD/sqlite-query-executor/releases/latest"
CURRENT_VERSION = "1.0.0"  # Versão atual do aplicativo
LATEST_VERSION = CURRENT_VERSION  # Variável global para armazenar a versão mais recente


def get_latest_release():
    response = requests.get(REPO_URL)
    response.raise_for_status()
    latest_release = response.json()
    global LATEST_VERSION
    LATEST_VERSION = latest_release["tag_name"]
    return latest_release["tag_name"], latest_release["zipball_url"]


def check_for_updates():
    latest_version, download_url = get_latest_release()

    if latest_version != CURRENT_VERSION:
        print(f"Nova versão disponível: {latest_version}. Atualizando...")
        update_app(download_url)
        return True
    else:
        return False


def update_app(download_url):
    # Baixar o arquivo zip da nova versão
    response = requests.get(download_url)
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        z.extractall()

    # Atualizar a versão atual
    global CURRENT_VERSION
    CURRENT_VERSION = LATEST_VERSION
