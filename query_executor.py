import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from tkinter import filedialog
import webbrowser
import ttkbootstrap as ttk
from PIL import Image, ImageTk
import requests

DATABASE = 'people.db'

def run_query_executor(version):
    def execute_query(query):
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            conn.close()
            return results
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao executar a consulta: {e}")
            return []

    def display_results(results):
        for row in data_tree.get_children():
            data_tree.delete(row)
        for row in results:
            data_tree.insert("", "end", values=row)

    def on_query_select():
        selected_query = query_var.get()
        results = execute_query(queries[selected_query])
        display_results(results)
        global last_query_results
        last_query_results = results

    def on_search_by_id():
        person_id = id_entry.get()
        if person_id:
            query = f"SELECT * FROM people WHERE id = {person_id}"
            results = execute_query(query)
            display_results(results)
            global last_query_results
            last_query_results = results
        else:
            messagebox.showwarning("Aviso", "Por favor, insira um ID válido.")

    def save_to_excel():
        if last_query_results:
            df = pd.DataFrame(last_query_results, columns=["ID", "First Name", "Last Name", "Age", "City"])
            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
            if file_path:
                try:
                    df.to_excel(file_path, index=False, engine='openpyxl')
                    messagebox.showinfo("Sucesso", "Arquivo salvo com sucesso!")
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao salvar o arquivo: {e}\n{str(e)}")
        else:
            messagebox.showwarning("Aviso", "Não há resultados para salvar.")

    def list_repositories():
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM repositories")
            results = cursor.fetchall()
            conn.close()
            display_repository_buttons(results)
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao listar os repositórios: {e}")

    def display_repository_buttons(repositories):
        for widget in repo_frame.winfo_children():
            widget.destroy()
        for repo in repositories:
            repo_button = ttk.Button(repo_frame, text=repo[1], command=lambda url=repo[2]: open_repository(url), bootstyle="info-outline")
            repo_button.pack(pady=5)

    def open_repository(url):
        webbrowser.open(url)

    def get_pull_requests(repo_name, repo_url):
        api_url = repo_url.replace("https://github.com/", "https://api.github.com/repos/") + "/pulls"
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            return len(response.json())
        except requests.RequestException as e:
            messagebox.showerror("Erro", f"Erro ao buscar pull requests: {e}")
            return 0

    def list_pull_requests():
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute("SELECT name, url FROM repositories")
            results = cursor.fetchall()
            conn.close()
            display_pull_requests(results)
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao listar os repositórios: {e}")

    def display_pull_requests(repositories):
        for widget in pr_frame.winfo_children():
            widget.destroy()
        for repo in repositories:
            pr_count = get_pull_requests(repo[0], repo[1])
            pr_label = ttk.Label(pr_frame, text=f"{repo[0]}: {pr_count} pull requests abertos", bootstyle="info")
            pr_label.pack(pady=5)

    def load_icon(path, size):
        image = Image.open(path)
        image = image.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(image)

    root = ttk.Window(themename="darkly")
    root.title(f"SQLite Query Executor - Versão {version}")
    root.geometry("800x600")

    notebook = ttk.Notebook(root, bootstyle="primary")
    notebook.pack(expand=1, fill='both')

    queries = {
        "Listar todas as pessoas": "SELECT * FROM people WHERE age > 30",
        "Listar pessoas de São Paulo": "SELECT * FROM people WHERE city = 'São Paulo'",
        "Listar pessoas com A": "SELECT * FROM people WHERE last_name LIKE 'A%'"
    }

    # Aba Dados
    data_frame = ttk.Frame(notebook)
    notebook.add(data_frame, text="Dados")

    query_var = tk.StringVar()
    query_label = ttk.Label(data_frame, text="Selecione uma consulta:", bootstyle="info")
    query_label.pack(pady=10)

    query_combobox = ttk.Combobox(data_frame, textvariable=query_var, bootstyle="success")
    query_combobox['values'] = list(queries.keys())
    query_combobox.pack(pady=5)

    # Carregar imagens de ícones e redimensionar
    execute_icon = load_icon("icons/play.png", (20, 20))
    execute_button = ttk.Button(data_frame, text=" Executar", command=on_query_select, image=execute_icon, compound=tk.LEFT, bootstyle="warning-outline")
    execute_button.pack(pady=10)

    search_frame = ttk.Frame(data_frame)
    search_frame.pack(pady=10)

    id_label = ttk.Label(search_frame, text="Buscar por ID:", bootstyle="info")
    id_label.pack(side=tk.LEFT, padx=5)

    id_entry = ttk.Entry(search_frame, bootstyle="success")
    id_entry.pack(side=tk.LEFT, padx=5)

    search_icon = load_icon("icons/search.png", (20, 20))
    search_button = ttk.Button(search_frame, text=" Buscar", command=on_search_by_id, image=search_icon, compound=tk.LEFT, bootstyle="warning-outline")
    search_button.pack(side=tk.LEFT, padx=5)

    save_icon = load_icon("icons/cloud-download.png", (20, 20))
    save_button = ttk.Button(data_frame, text=" Salvar em Excel", command=save_to_excel, image=save_icon, compound=tk.LEFT, bootstyle="warning-outline")
    save_button.pack(pady=10)

    data_tree_frame = ttk.Frame(data_frame)
    data_tree_frame.pack(pady=10)

    data_tree_scroll = ttk.Scrollbar(data_tree_frame)
    data_tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    data_tree = ttk.Treeview(data_tree_frame, columns=("ID", "First Name", "Last Name", "Age", "City"), show="headings",
                             yscrollcommand=data_tree_scroll.set, bootstyle="info")
    data_tree.pack()

    data_tree_scroll.config(command=data_tree.yview)

    data_tree.heading("ID", text="ID")
    data_tree.heading("First Name", text="First Name")
    data_tree.heading("Last Name", text="Last Name")
    data_tree.heading("Age", text="Age")
    data_tree.heading("City", text="City")

    # Aba Repositórios
    repo_frame = ttk.Frame(notebook)
    notebook.add(repo_frame, text="Repositórios")

    list_repositories()

    # Aba Pull Requests
    pr_frame = ttk.Frame(notebook)
    notebook.add(pr_frame, text="Pull Requests")

    list_pull_requests()

    global last_query_results
    last_query_results = []

    root.mainloop()

run_query_executor("v2.0.5")
