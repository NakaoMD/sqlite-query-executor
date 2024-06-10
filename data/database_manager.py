import sqlite3
import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class DatabaseManager:
    """Classe responsável pela gestão do banco de dados."""

    def __init__(self, database):
        """
        Inicializa a instância do DatabaseManager.

        :param database: O caminho para o arquivo do banco de dados SQLite.
        """
        self.database = database
        self.connection = None

    def connect(self):
        """Conecta ao banco de dados SQLite."""
        try:
            self.connection = sqlite3.connect(self.database)
            logging.info("Conectado ao banco de dados com sucesso.")
        except sqlite3.Error as e:
            logging.error(f"Erro ao conectar ao banco de dados: {e}")

    def disconnect(self):
        """Desconecta do banco de dados SQLite."""
        if self.connection:
            self.connection.close()
            logging.info("Desconectado do banco de dados.")

    def execute_query(self, query, params=None):
        """
        Executa uma consulta SQL e retorna os resultados.

        :param query: A consulta SQL a ser executada.
        :param params: Parâmetros para a consulta SQL.
        :return: Resultados da consulta SQL.
        """
        results = []
        if self.connection:
            try:
                cursor = self.connection.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                results = cursor.fetchall()
            except sqlite3.Error as e:
                logging.error(f"Erro ao executar a consulta: {e}")
        return results

    def get_all_optin_data(self):
        """
        Retorna todos os dados da tabela optin_data.

        :return: Lista de registros da tabela optin_data.
        """
        query = "SELECT * FROM optin_data"
        return self.execute_query(query)

    def get_optin_data_by_id(self, cod_idef_pess):
        """
        Retorna os dados da tabela optin_data para um ID específico.

        :param cod_idef_pess: O ID da pessoa.
        :return: Registro correspondente na tabela optin_data.
        """
        query = "SELECT * FROM optin_data WHERE cod_idef_pess = ?"
        return self.execute_query(query, (cod_idef_pess,))

    def get_all_repositories(self):
        """
        Retorna todos os repositórios da tabela repositories.

        :return: Lista de repositórios.
        """
        query = "SELECT * FROM repositories"
        return self.execute_query(query)

    def get_pull_requests_count(self, repo_url):
        """
        Retorna a contagem de pull requests abertos para um repositório específico.

        :param repo_url: A URL do repositório no GitHub.
        :return: Contagem de pull requests abertos.
        """
        if not repo_url.startswith("https://"):
            repo_url = "https://github.com/" + repo_url

        api_url = repo_url.replace("https://github.com/", "https://api.github.com/repos/") + "/pulls"
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            pr_count = len(response.json())
            return pr_count
        except requests.RequestException as e:
            logging.error(f"Erro ao buscar pull requests para {repo_url}: {e}")
            return 0

    def repair_database(self):
        """Repara o banco de dados caso ele esteja corrompido ou ausente."""
        try:
            self.connect()
            # Verifique a integridade do banco de dados
            result = self.execute_query("PRAGMA integrity_check")
            if result[0][0] == 'ok':
                logging.info("Banco de dados íntegro.")
            else:
                logging.warning("Banco de dados corrompido. Tentando reparar...")
                # Implementar lógica de reparo, como recriar tabelas ou restaurar de um backup
                self.execute_query("REINDEX")
                logging.info("Banco de dados reparado com sucesso.")
        except sqlite3.Error as e:
            logging.error(f"Erro ao reparar o banco de dados: {e}")
        finally:
            self.disconnect()

    def main(self):
        """Método principal para executar operações de exemplo no banco de dados."""
        self.repair_database()  # Verifica e repara o banco de dados ao iniciar

        self.connect()

        logging.info("Consultando todos os dados da tabela 'optin_data':")
        all_optin_data = self.get_all_optin_data()
        for record in all_optin_data:
            logging.info(record)

        logging.info("\nConsultando optin_data pelo ID:")
        cod_idef_pess = all_optin_data[0][0]  # Pega o primeiro ID para consulta
        optin_data = self.get_optin_data_by_id(cod_idef_pess)
        if optin_data:
            logging.info(f"Registro com ID {cod_idef_pess}: {optin_data}")
        else:
            logging.warning(f"Nenhum registro encontrado com ID {cod_idef_pess}")

        logging.info("\nConsultando todos os repositórios:")
        all_repositories = self.get_all_repositories()
        for repo in all_repositories:
            logging.info(repo)

        logging.info("\nConsultando pull requests para cada repositório:")
        for repo in all_repositories:
            repo_name = repo[0]
            repo_url = repo[1]
            pr_count = self.get_pull_requests_count(repo_url)
            logging.info(f"Repositório {repo_name}: {pr_count} pull requests abertos")

        self.disconnect()


if __name__ == "__main__":
    database_manager = DatabaseManager("people.db")
    database_manager.main()
