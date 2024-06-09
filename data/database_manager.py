import sqlite3

class DatabaseManager:
    def __init__(self, database):
        self.database = database
        self.connection = None

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.database)
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=None):
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
                print(f"Erro ao executar a consulta: {e}")
        return results

    def list_repositories(self):
        query = "SELECT * FROM repositories"
        return self.execute_query(query)

    def get_pull_requests(self):
        query = "SELECT * FROM pull_requests"
        return self.execute_query(query)
