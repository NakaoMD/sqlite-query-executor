import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from tkinter import filedialog
from data.database import execute_query
from ui.utils import load_icon, ToolTip, add_button_feedback

# Variáveis globais para paginação
current_page = 0
page_size = 10
last_query_results = []

def create_data_tab(data_frame):
    global query_var, queries, data_tree, result_count_label

    query_var = tk.StringVar()
    query_label = ttk.Label(data_frame, text="Selecione uma consulta:")
    query_label.pack(pady=10)

    queries = {
        "Listar todas as pessoas": "SELECT * FROM people WHERE age > 30",
        "Listar pessoas de São Paulo": "SELECT * FROM people WHERE city = 'São Paulo'",
        "Listar pessoas com A": "SELECT * FROM people WHERE last_name LIKE 'A%'"
    }

    query_combobox = ttk.Combobox(data_frame, textvariable=query_var)
    query_combobox['values'] = list(queries.keys())
    query_combobox.pack(pady=5)

    execute_icon = load_icon("icons/play.png", (20, 20))
    execute_button = ttk.Button(data_frame, text=" Executar", command=lambda: on_query_select(query_var.get(), queries, data_tree, 0), image=execute_icon, compound=tk.LEFT)
    execute_button.pack(pady=10)
    add_button_feedback(execute_button)  # Adiciona feedback visual ao botão
    ToolTip(execute_button, text="Clique para executar a consulta selecionada")  # Adiciona tooltip

    search_frame = ttk.Frame(data_frame)
    search_frame.pack(pady=10)

    id_label = ttk.Label(search_frame, text="Buscar por ID:")
    id_label.pack(side=tk.LEFT, padx=5)

    id_entry = ttk.Entry(search_frame)
    id_entry.pack(side=tk.LEFT, padx=5)

    search_icon = load_icon("icons/search.png", (20, 20))
    search_button = ttk.Button(search_frame, text=" Buscar", command=lambda: on_search_by_id(id_entry, data_tree, 0), image=search_icon, compound=tk.LEFT)
    search_button.pack(side=tk.LEFT, padx=5)
    add_button_feedback(search_button)  # Adiciona feedback visual ao botão
    ToolTip(search_button, text="Digite um ID e clique para buscar")  # Adiciona tooltip

    save_icon = load_icon("icons/cloud-download.png", (20, 20))
    save_button = ttk.Button(data_frame, text=" Salvar em Excel", command=lambda: save_to_excel(last_query_results), image=save_icon, compound=tk.LEFT)
    save_button.pack(pady=10)
    add_button_feedback(save_button)  # Adiciona feedback visual ao botão
    ToolTip(save_button, text="Clique para salvar os resultados em um arquivo Excel")  # Adiciona tooltip

    pagination_frame = ttk.Frame(data_frame)
    pagination_frame.pack(pady=10)

    prev_button = ttk.Button(pagination_frame, text="Anterior", command=lambda: change_page(-1))
    prev_button.pack(side=tk.LEFT, padx=5)
    add_button_feedback(prev_button)  # Adiciona feedback visual ao botão
    ToolTip(prev_button, text="Clique para ver a página anterior")  # Adiciona tooltip

    next_button = ttk.Button(pagination_frame, text="Próximo", command=lambda: change_page(1))
    next_button.pack(side=tk.LEFT, padx=5)
    add_button_feedback(next_button)  # Adiciona feedback visual ao botão
    ToolTip(next_button, text="Clique para ver a próxima página")  # Adiciona tooltip

    result_count_label = ttk.Label(data_frame, text="Total de Resultados: 0")
    result_count_label.pack(pady=5)

    data_tree_frame = ttk.Frame(data_frame)
    data_tree_frame.pack(pady=10)

    data_tree_scroll = ttk.Scrollbar(data_tree_frame)
    data_tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    data_tree = ttk.Treeview(data_tree_frame, columns=("ID", "First Name", "Last Name", "Age", "City"), show="headings", yscrollcommand=data_tree_scroll.set)
    data_tree.pack()

    data_tree_scroll.config(command=data_tree.yview)

    data_tree.heading("ID", text="ID")
    data_tree.heading("First Name", text="First Name")
    data_tree.heading("Last Name", text="Last Name")
    data_tree.heading("Age", text="Age")
    data_tree.heading("City", text="City")

def on_query_select(selected_query, queries, data_tree, page):
    global current_page, last_query_results, result_count_label
    query = queries[selected_query] + f" LIMIT {page_size} OFFSET {page * page_size}"
    results = execute_query(query)
    total_query = f"SELECT COUNT(*) FROM ({queries[selected_query]})"
    total_results = execute_query(total_query)[0][0]
    display_results(data_tree, results)
    last_query_results = results
    current_page = page
    result_count_label.config(text=f"Total de Resultados: {total_results}")

def on_search_by_id(id_entry, data_tree, page):
    global current_page, last_query_results, result_count_label
    person_id = id_entry.get()
    if not person_id.isdigit():
        messagebox.showwarning("Aviso", "Por favor, insira um ID válido.")
        id_entry.config(background='red')
        return
    else:
        id_entry.config(background='white')

    query = f"SELECT * FROM people WHERE id = ? LIMIT {page_size} OFFSET {page * page_size}"
    results = execute_query(query, (person_id,))
    total_query = "SELECT COUNT(*) FROM people WHERE id = ?"
    total_results = execute_query(total_query, (person_id,))[0][0]
    display_results(data_tree, results)
    last_query_results = results
    current_page = page
    result_count_label.config(text=f"Total de Resultados: {total_results}")

def change_page(direction):
    global current_page
    current_page += direction
    if current_page < 0:
        current_page = 0
    on_query_select(query_var.get(), queries, data_tree, current_page)

def save_to_excel(results):
    if results:
        df = pd.DataFrame(results, columns=["ID", "First Name", "Last Name", "Age", "City"])
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
        if file_path:
            try:
                df.to_excel(file_path, index=False, engine='openpyxl')
                messagebox.showinfo("Sucesso", "Arquivo salvo com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar o arquivo: {e}\n{str(e)}")
    else:
        messagebox.showwarning("Aviso", "Não há resultados para salvar.")

def display_results(data_tree, results):
    for row in data_tree.get_children():
        data_tree.delete(row)
    for row in results:
        data_tree.insert("", "end", values=row)
