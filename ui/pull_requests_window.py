import tkinter as tk
from tkinter import ttk
from ui.utils import load_icon
import requests
from data.state_manager import state_manager  # Importar o state_manager

def display_category_buttons_pull_requests(parent_frame, categorized_repos, main_app):
    for widget in parent_frame.winfo_children():
        widget.destroy()

    for category, repos in categorized_repos.items():
        if repos:
            button_text = f"{category.upper()} ({len(repos)})"
            cat_button = ttk.Button(parent_frame, text=button_text, command=lambda r=repos: open_category_window_pull_requests(r, category, main_app))
            cat_button.pack(pady=5)

def open_category_window_pull_requests(repos, category, main_app):
    category_window = tk.Toplevel(main_app)
    category_window.title(f"Pull Requests - {category.upper()}")
    category_window.geometry("600x400")

    pr_icon = load_icon("icons/git.png", (20, 20))

    # Frame principal
    main_frame = ttk.Frame(category_window)
    main_frame.pack(fill=tk.BOTH, expand=1)

    # Canvas para a área rolável
    canvas = tk.Canvas(main_frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    # Barra de rolagem vertical
    scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Frame rolável
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    def display_pull_requests():
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        for repo in repos:
            repo_label = ttk.Label(scrollable_frame, text=f"{repo[0]}: {state_manager.get_pr_count(repo[1])} pull requests abertos", image=pr_icon, compound=tk.LEFT)
            repo_label.image = pr_icon  # Keep a reference to avoid garbage collection
            repo_label.pack(pady=5, anchor='w')

    def update_pull_requests():
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        for repo in repos:
            pr_count = get_pull_requests_count(repo[1])
            pr_label = ttk.Label(scrollable_frame, text=f"{repo[0]}: {pr_count} pull requests abertos", image=pr_icon, compound=tk.LEFT)
            pr_label.image = pr_icon  # Keep a reference to avoid garbage collection
            pr_label.pack(pady=5, anchor='w')

    # Adiciona botões na parte superior da janela
    button_frame = ttk.Frame(scrollable_frame)
    button_frame.pack(fill=tk.X, pady=5)

    update_button = ttk.Button(button_frame, text="Atualizar", command=update_pull_requests)
    update_button.pack(side=tk.LEFT, padx=10)

    close_button = ttk.Button(button_frame, text="Fechar", command=category_window.destroy)
    close_button.pack(side=tk.RIGHT, padx=10)

    display_pull_requests()

def get_pull_requests_count(repo_url):
    if repo_url in state_manager.pull_request_cache:
        return state_manager.pull_request_cache[repo_url]

    api_url = repo_url.replace("https://github.com/", "https://api.github.com/repos/") + "/pulls"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        pr_count = len(response.json())

        # Armazena os resultados em cache
        state_manager.set_pr_count(repo_url, pr_count)
        return pr_count
    except requests.RequestException as e:
        print(f"Erro ao buscar pull requests: {e}")
        return 0
