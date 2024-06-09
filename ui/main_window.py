import tkinter as tk
from tkinter import ttk
from data.database import list_repositories, get_pull_requests
from ui.repo_window import display_category_buttons
from ui.pull_requests_window import display_category_buttons_pull_requests
from ui.data_window import create_data_tab

class MainWindow(tk.Tk):
    def __init__(self, version):
        super().__init__()
        self.title(f"SQLite Query Executor - Versão {version}")
        self.geometry("800x600")
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=1, fill='both')

        self.create_data_tab()
        self.create_repositories_tab()
        self.create_pull_requests_tab()

    def create_data_tab(self):
        create_data_tab(self.notebook)

    def create_repositories_tab(self):
        repo_frame = ttk.Frame(self.notebook)
        self.notebook.add(repo_frame, text="Repositórios")
        categorized_repos = self.categorize_repositories(list_repositories())
        display_category_buttons(repo_frame, categorized_repos, self)

    def create_pull_requests_tab(self):
        pr_frame = ttk.Frame(self.notebook)
        self.notebook.add(pr_frame, text="Pull Requests")
        categorized_repos = self.categorize_repositories(list_repositories())
        display_category_buttons_pull_requests(pr_frame, categorized_repos, self)

    def categorize_repositories(self, repositories):
        categories = {"app": [], "dep": [], "infra": [], "other": []}
        for repo in repositories:
            category = "other"
            if repo[1].startswith("app"):
                category = "app"
            elif repo[1].startswith("dep"):
                category = "dep"
            elif repo[1].startswith("infra"):
                category = "infra"
            categories[category].append(repo)
        return categories

if __name__ == "__main__":
    app = MainWindow("2.0.5")
    app.mainloop()
