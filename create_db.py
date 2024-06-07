import sqlite3

# Criação do banco de dados e conexão
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# Criação de uma tabela e inserção de dados de exemplo
cursor.execute('''
CREATE TABLE IF NOT EXISTS cadastro_pessoas (
    id INTEGER PRIMARY KEY,
    nome TEXT,
    idade INTEGER,
    email TEXT,
    telefone TEXT
)
''')

# Inserção de dados de exemplo
cursor.execute('INSERT INTO cadastro_pessoas (nome, idade, email, telefone) VALUES ("João", 30, "joao@example.com", "123456789")')
cursor.execute('INSERT INTO cadastro_pessoas (nome, idade, email, telefone) VALUES ("Maria", 25, "maria@example.com", "987654321")')

conn.commit()
conn.close()
