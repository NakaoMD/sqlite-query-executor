
import sqlite3

DATABASE = 'people.db'

def insert_predefined_repositories():
    repos = [
        ("sqlite-query-executor", "https://github.com/NakaoMD/sqlite-query-executor")
    ]

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO repositories (name, url) VALUES (?, ?)", repos)
    conn.commit()
    conn.close()

insert_predefined_repositories()




if __name__ == "__main__":
    insert_predefined_repositories()
