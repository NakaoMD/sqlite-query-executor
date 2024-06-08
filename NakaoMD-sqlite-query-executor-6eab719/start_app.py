import subprocess
import sys
import os
import logging
import psutil
import time

# Configurar logging
logging.basicConfig(filename='app_debug.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

# Verificar se o aplicativo já está em execução
def is_already_running():
    try:
        if sys.platform == "win32":
            lock_file = os.path.join(os.environ['TEMP'], 'app.lock')
        else:
            lock_file = '/tmp/app.lock'

        if os.path.exists(lock_file):
            with open(lock_file, 'r') as f:
                pid = int(f.read().strip())
                logging.debug(f"Arquivo de lock encontrado. PID: {pid}")
                # Verificar se o processo ainda está em execução
                try:
                    # Usar psutil para verificar se o processo está em execução
                    if psutil.pid_exists(pid):
                        logging.debug("Aplicativo já está em execução.")
                        return True
                    else:
                        logging.debug("PID não está em execução. Removendo o arquivo de lock.")
                        os.remove(lock_file)
                        logging.debug("Arquivo de lock removido.")
                except Exception as e:
                    logging.error(f"Erro ao verificar o estado do PID: {e}")
                    return True

        with open(lock_file, 'w') as f:
            f.write(str(os.getpid()))
            logging.debug(f"Arquivo de lock criado. PID: {os.getpid()}")

        return False
    except Exception as e:
        logging.error(f"Erro ao verificar se o aplicativo já está em execução: {e}")
        return True

def remove_lock_file():
    try:
        if sys.platform == "win32":
            lock_file = os.path.join(os.environ['TEMP'], 'app.lock')
        else:
            lock_file = '/tmp/app.lock'

        if os.path.exists(lock_file):
            os.remove(lock_file)
            logging.debug("Arquivo de lock removido.")
    except Exception as e:
        logging.error(f"Erro ao remover o arquivo de lock: {e}")

def main():
    try:
        logging.debug("Iniciando verificação de execução.")
        if is_already_running():
            logging.debug("Finalizando devido a execução existente.")
            return

        logging.debug("Verificando atualizações...")

        # Verificar atualizações antes de iniciar o aplicativo
        try:
            logging.debug("Executando check_for_updates.py")
            result = subprocess.run([sys.executable, "check_for_updates.py"], capture_output=True, text=True)
            logging.debug(result.stdout)
            logging.debug(result.stderr)
        except Exception as e:
            logging.error(f"Erro ao verificar atualizações: {e}")

        logging.debug("Iniciando o aplicativo...")

        # Tentar importar e executar o query_executor.py diretamente
        try:
            logging.debug("Importando query_executor")
            import query_executor
            query_executor.main()
        except Exception as e:
            logging.error(f"Erro ao importar ou executar query_executor diretamente: {e}")

        logging.debug("Executando query_executor.py")
        try:
            result = subprocess.run([sys.executable, "query_executor.py"], capture_output=True, text=True)
            logging.debug(result.stdout)
            logging.debug(result.stderr)
        except Exception as e:
            logging.error(f"Erro ao iniciar o aplicativo: {e}")
        finally:
            time.sleep(1)  # Adicionando um atraso para garantir que o aplicativo finalizou corretamente
            remove_lock_file()
            logging.debug("Aplicativo finalizado.")
    except Exception as e:
        logging.error(f"Erro inesperado: {e}")

if __name__ == "__main__":
    main()
