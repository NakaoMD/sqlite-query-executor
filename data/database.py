import sqlite3

DATABASE = 'people.db'

def connect():
    return sqlite3.connect(DATABASE)

def execute_query(query, params=()):
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return results
    except sqlite3.Error as e:
        print(f"Erro ao executar a consulta: {e}")
        return []

def list_repositories():
    return execute_query("SELECT * FROM repositories")

def get_pull_requests():
    return execute_query("SELECT name, url FROM repositories")
