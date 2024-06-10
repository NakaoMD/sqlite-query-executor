import sqlite3
from faker import Faker

DATABASE = 'people.db'
faker = Faker()


def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            age INTEGER NOT NULL,
            city TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def populate_table(num_records):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    for _ in range(num_records):
        first_name = faker.first_name()
        last_name = faker.last_name()
        age = faker.random_int(min=18, max=80)
        city = faker.city()
        cursor.execute('''
            INSERT INTO people (first_name, last_name, age, city)
            VALUES (?, ?, ?, ?)
        ''', (first_name, last_name, age, city))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_table()
    populate_table(10000)
    print("Banco de dados populado com sucesso!")
