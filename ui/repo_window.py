import tkinter as tk
from tkinter import ttk
from ui.utils import load_icon
import webbrowser

def display_category_buttons(parent_frame, categorized_repos, main_app):
    for widget in parent_frame.winfo_children():
        widget.destroy()

    for category, repos in categorized_repos.items():
        if repos:
            button_text = f"{category.upper()} ({len(repos)})"
            cat_button = ttk.Button(parent_frame, text=button_text, command=lambda c=category: open_category_window(categorized_repos[c], main_app))
            cat_button.pack(pady=5)

def open_category_window(repos, main_app):
    category_window = tk.Toplevel(main_app)
    category_window.title("Repositórios")
    category_window.geometry("400x400")

    git_icon = load_icon("icons/git.png", (20, 20))

    for repo in repos:
        repo_button = ttk.Button(category_window, text=repo[1], image=git_icon, compound=tk.LEFT, command=lambda url=repo[2]: open_repository(url))
        repo_button.image = git_icon  # Keep a reference to avoid garbage collection
        repo_button.pack(pady=5)

    close_button = ttk.Button(category_window, text="Fechar", command=category_window.destroy)
    close_button.pack(pady=10)

def open_repository(url):
    webbrowser.open(url)
