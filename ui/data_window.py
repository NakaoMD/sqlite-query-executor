import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from tkinter import filedialog
from data.database import execute_query
from ui.utils import load_icon

def create_data_tab(notebook):
    data_frame = ttk.Frame(notebook)
    notebook.add(data_frame, text="Dados")

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
    execute_button = ttk.Button(data_frame, text=" Executar", command=lambda: on_query_select(query_var.get(), queries, data_tree), image=execute_icon, compound=tk.LEFT)
    execute_button.pack(pady=10)

    search_frame = ttk.Frame(data_frame)
    search_frame.pack(pady=10)

    id_label = ttk.Label(search_frame, text="Buscar por ID:")
    id_label.pack(side=tk.LEFT, padx=5)

    id_entry = ttk.Entry(search_frame)
    id_entry.pack(side=tk.LEFT, padx=5)

    search_icon = load_icon("icons/search.png", (20, 20))
    search_button = ttk.Button(search_frame, text=" Buscar", command=lambda: on_search_by_id(id_entry, data_tree), image=search_icon, compound=tk.LEFT)
    search_button.pack(side=tk.LEFT, padx=5)

    save_icon = load_icon("icons/cloud-download.png", (20, 20))
    save_button = ttk.Button(data_frame, text=" Salvar em Excel", command=lambda: save_to_excel(last_query_results), image=save_icon, compound=tk.LEFT)
    save_button.pack(pady=10)

    data_tree_frame = ttk.Frame(data_frame)
    data_tree_frame.pack(pady=10)

    data_tree_scroll = ttk.Scrollbar(data_tree_frame)
    data_tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    data_tree = ttk.Treeview(data_tree_frame, columns=("ID", "First Name", "Last Name", "Age", "City"), show="headings",
                             yscrollcommand=data_tree_scroll.set)
    data_tree.pack()

    data_tree_scroll.config(command=data_tree.yview)

    data_tree.heading("ID", text="ID")
    data_tree.heading("First Name", text="First Name")
    data_tree.heading("Last Name", text="Last Name")
    data_tree.heading("Age", text="Age")
    data_tree.heading("City", text="City")

    global last_query_results
    last_query_results = []

def on_query_select(selected_query, queries, data_tree):
    query = queries[selected_query]
    results = execute_query(query)
    display_results(data_tree, results)
    global last_query_results
    last_query_results = results

def on_search_by_id(id_entry, data_tree):
    person_id = id_entry.get()
    if person_id:
        query = f"SELECT * FROM people WHERE id = {person_id}"
        results = execute_query(query)
        display_results(data_tree, results)
        global last_query_results
        last_query_results = results
    else:
        messagebox.showwarning("Aviso", "Por favor, insira um ID válido.")

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
