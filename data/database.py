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
        conn.commit()
        conn.close()
        return results
    except sqlite3.Error as e:
        print(f"Erro ao executar a consulta: {e}")
        return []

def list_repositories(active_only=False, limit=100, offset=0):
    query = "SELECT * FROM repositories"
    if active_only:
        query += " WHERE status = 'ativado'"
    query += f" LIMIT {limit} OFFSET {offset}"
    return execute_query(query)

def list_all_repositories():
    query = "SELECT * FROM repositories"
    return execute_query(query)

def get_pull_requests():
    return execute_query("SELECT name, url FROM repositories")

def update_repository(repo_id, new_name, new_url):
    query = "UPDATE repositories SET name = ?, url = ? WHERE id = ?"
    params = (new_name, new_url, repo_id)
    execute_query(query, params)

def delete_repository(repo_id):
    query = "DELETE FROM repositories WHERE id = ?"
    params = (repo_id,)
    execute_query(query, params)

def update_repository_status(repo_id, new_status):
    query = "UPDATE repositories SET status = ? WHERE id = ?"
    params = (new_status, repo_id)
    execute_query(query, params)

def insert_repository(name, url, status):
    query = "INSERT INTO repositories (name, url, status) VALUES (?, ?, ?)"
    params = (name, url, status)
    execute_query(query, params)
