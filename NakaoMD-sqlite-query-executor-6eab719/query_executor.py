import sqlite3
import tkinter as tk
from tkinter import ttk
import os
import sys
import logging

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Função para executar a consulta SQLite e obter colunas
def execute_query(query):
    db_path = resource_path('example.db')
    logging.debug(f"Usando banco de dados em: {db_path}")
    if not os.path.exists(db_path):
        logging.debug("Banco de dados não encontrado.")
        return [], ['Erro: Banco de dados não encontrado']

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    col_names = [description[0] for description in cursor.description]
    conn.close()
    return result, col_names

def run_query():
    logging.debug("Executando consulta...")
    selected_query = query_listbox.get(tk.ACTIVE)
    query = predefined_queries[selected_query]
    result, col_names = execute_query(query)
    logging.debug(f"Resultados: {result}")

    # Limpar a tabela antes de inserir novos dados
    for row in tree.get_children():
        tree.delete(row)

    # Atualizar as colunas dinamicamente
    tree["columns"] = col_names
    tree["show"] = "headings"
    for col in col_names:
        tree.heading(col, text=col)
        tree.column(col, minwidth=0, width=100)

    # Inserir novos dados
    for row in result:
        tree.insert("", "end", values=row)

def main():
    # Criação da interface gráfica
    logging.debug("Iniciando a interface gráfica...")
    global query_listbox, tree
    root = tk.Tk()
    root.title("SQLite Query Executor")

    predefined_queries = {
        "Listar todas as pessoas": "SELECT * FROM cadastro_pessoas;",
        "Listar pessoas acima de 25 anos": "SELECT * FROM cadastro_pessoas WHERE idade > 25;",
        "Listar total de pessoas": "SELECT COUNT(*) FROM cadastro_pessoas;"
    }

    # Configuração da grade para tornar o layout responsivo
    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    root.rowconfigure(3, weight=1)

    ttk.Label(root, text="Escolha uma consulta:").grid(column=0, row=0, padx=10, pady=10, sticky=tk.W)

    query_listbox = tk.Listbox(root)
    query_listbox.grid(column=0, row=1, padx=10, pady=10, sticky=tk.NSEW)
    for query_name in predefined_queries.keys():
        query_listbox.insert(tk.END, query_name)

    run_button = ttk.Button(root, text="Executar Consulta", command=run_query)
    run_button.grid(column=0, row=2, padx=10, pady=10, sticky=tk.W)

    # Criação da tabela (Treeview) e adicionando um scrollbar
    tree_frame = ttk.Frame(root)
    tree_frame.grid(column=0, row=3, padx=10, pady=10, sticky=tk.NSEW)

    tree_scroll = ttk.Scrollbar(tree_frame)
    tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
    tree.pack(expand=True, fill=tk.BOTH)
    tree_scroll.config(command=tree.yview)

    # Configuração da grade dentro do frame da tabela para torná-la responsiva
    tree_frame.columnconfigure(0, weight=1)
    tree_frame.rowconfigure(0, weight=1)

    logging.debug("Interface gráfica iniciada.")
    root.mainloop()

if __name__ == "__main__":
    logging.basicConfig(filename='query_debug.log', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')
    main()
