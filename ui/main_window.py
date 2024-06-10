import tkinter as tk
from tkinter import ttk
import os
from data.database import list_repositories, get_pull_requests
from ui.repo_window import display_category_buttons
from ui.pull_requests_window import display_category_buttons_pull_requests
from ui.data_window import create_data_tab


class MainWindow(tk.Tk):
    def __init__(self, version):
        super().__init__()
        self.title(f"Motor Executor - Versão {version}")
        self.geometry("800x600")
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=1, fill='both')

        self.create_data_tab()
        self.create_repositories_tab()
        self.create_pull_requests_tab()

        self.create_status_bar()
        self.create_logoff_button()

    def create_data_tab(self):
        self.data_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.data_frame, text="Dados")
        create_data_tab(self.data_frame)

    def create_repositories_tab(self):
        self.repo_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.repo_frame, text="Repositórios")
        categorized_repos = self.categorize_repositories(list_repositories(active_only=True))
        display_category_buttons(self.repo_frame, categorized_repos, self)

    def create_pull_requests_tab(self):
        self.pr_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.pr_frame, text="Pull Requests")
        categorized_repos = self.categorize_repositories(list_repositories(active_only=True))
        display_category_buttons_pull_requests(self.pr_frame, categorized_repos, self)

    def create_status_bar(self):
        user = os.getlogin()
        status_bar = ttk.Label(self, text=f"User: {user}", anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_logoff_button(self):
        button_frame = ttk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        logoff_button = ttk.Button(button_frame, text="Logoff", command=self.logoff)
        logoff_button.pack(side=tk.RIGHT, padx=10)

    def logoff(self):
        self.destroy()
        create_login_window("2.0.5")

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


def create_main_window(version):
    main_window = MainWindow(version)
    main_window.mainloop()


def create_login_window(version):
    from ui.login_window import LoginWindow
    login_window = LoginWindow(version)
    login_window.mainloop()
