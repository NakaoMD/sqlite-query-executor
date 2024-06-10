import tkinter as tk
from tkinter import ttk, messagebox
from data.database import list_repositories, list_all_repositories, update_repository, delete_repository, \
    update_repository_status, insert_repository
from ui.utils import load_icon
import os


class AdminWindow(tk.Tk):
    def __init__(self, version):
        super().__init__()
        self.title(f"Admin Panel - Versão {version}")
        self.geometry("800x600")
        self.create_repository_tab()
        self.create_status_bar()
        self.create_logoff_button()

    def create_repository_tab(self):
        self.repo_frame = ttk.Frame(self)
        self.repo_frame.pack(expand=1, fill='both')
        self.display_repositories()

    def display_repositories(self):
        self.repo_frame.pack_forget()
        self.repo_frame = ttk.Frame(self)
        self.repo_frame.pack(expand=1, fill='both')

        self.canvas = tk.Canvas(self.repo_frame)
        self.scrollbar = ttk.Scrollbar(self.repo_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        columns = ("ID", "Name", "URL", "Status")
        self.repo_tree = ttk.Treeview(self.scrollable_frame, columns=columns, show='headings')
        for col in columns:
            self.repo_tree.heading(col, text=col)
        self.repo_tree.pack(expand=1, fill='both', padx=10, pady=10)

        self.repo_tree.bind("<Motion>", self.on_treeview_scroll)

        self.current_page = 0
        self.load_repositories()

        button_frame = ttk.Frame(self.scrollable_frame)
        button_frame.pack(pady=10)

        add_button = ttk.Button(button_frame, text="Adicionar", command=self.add_repository)
        add_button.pack(side=tk.LEFT, padx=5)

        edit_button = ttk.Button(button_frame, text="Editar", command=self.edit_repository)
        edit_button.pack(side=tk.LEFT, padx=5)

        delete_button = ttk.Button(button_frame, text="Excluir", command=self.delete_repository)
        delete_button.pack(side=tk.LEFT, padx=5)

    def load_repositories(self):
        repositories = list_all_repositories()
        for repo in repositories:
            self.repo_tree.insert("", "end", values=repo)

    def on_treeview_scroll(self, event):
        if self.repo_tree.yview()[1] >= 0.95:  # Carregar mais dados quando o scroll está próximo do fim
            self.current_page += 1
            self.load_repositories()

    def add_repository(self):
        add_window = tk.Toplevel(self)
        add_window.title("Adicionar Repositório")
        add_window.geometry("400x250")

        add_frame = ttk.Frame(add_window)
        add_frame.pack(expand=1, fill='both', padx=10, pady=10)

        add_frame.columnconfigure(1, weight=1)

        name_label = ttk.Label(add_frame, text="Nome:")
        name_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        name_entry = ttk.Entry(add_frame)
        name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

        url_label = ttk.Label(add_frame, text="URL:")
        url_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        url_entry = ttk.Entry(add_frame)
        url_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)

        status_label = ttk.Label(add_frame, text="Status:")
        status_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        status_var = tk.StringVar(value="ativado")
        status_combobox = ttk.Combobox(add_frame, textvariable=status_var, values=["ativado", "desativado"])
        status_combobox.grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)

        button_frame = ttk.Frame(add_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        confirm_button = ttk.Button(button_frame, text="Confirmar",
                                    command=lambda: self.confirm_add(name_entry.get(), url_entry.get(),
                                                                     status_var.get(), add_window))
        confirm_button.pack(side=tk.LEFT, padx=5)

        close_button = ttk.Button(button_frame, text="Fechar", command=add_window.destroy)
        close_button.pack(side=tk.RIGHT, padx=5)

    def confirm_add(self, name, url, status, add_window):
        if name and url:
            insert_repository(name, url, status)
            messagebox.showinfo("Sucesso", "Repositório adicionado com sucesso!")
            add_window.destroy()
            self.display_repositories()
        else:
            messagebox.showwarning("Erro", "Nome e URL não podem estar vazios.")

    def edit_repository(self):
        selected_item = self.repo_tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um repositório para editar.")
            return

        repo_id = self.repo_tree.item(selected_item)["values"][0]
        edit_window = tk.Toplevel(self)
        edit_window.title("Editar Repositório")
        edit_window.geometry("400x250")

        edit_frame = ttk.Frame(edit_window)
        edit_frame.pack(expand=1, fill='both', padx=10, pady=10)

        edit_frame.columnconfigure(1, weight=1)

        name_label = ttk.Label(edit_frame, text="Nome:")
        name_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        name_entry = ttk.Entry(edit_frame)
        name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

        url_label = ttk.Label(edit_frame, text="URL:")
        url_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        url_entry = ttk.Entry(edit_frame)
        url_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)

        status_label = ttk.Label(edit_frame, text="Status:")
        status_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        status_var = tk.StringVar(value="ativado")
        status_combobox = ttk.Combobox(edit_frame, textvariable=status_var, values=["ativado", "desativado"])
        status_combobox.grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)

        button_frame = ttk.Frame(edit_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        confirm_button = ttk.Button(button_frame, text="Confirmar",
                                    command=lambda: self.confirm_edit(repo_id, name_entry.get(), url_entry.get(),
                                                                      status_var.get(), edit_window))
        confirm_button.pack(side=tk.LEFT, padx=5)

        close_button = ttk.Button(button_frame, text="Fechar", command=edit_window.destroy)
        close_button.pack(side=tk.RIGHT, padx=5)

        current_values = self.repo_tree.item(selected_item)["values"]
        name_entry.insert(0, current_values[1])
        url_entry.insert(0, current_values[2])
        status_var.set(current_values[3])

    def confirm_edit(self, repo_id, new_name, new_url, new_status, edit_window):
        if new_name and new_url:
            update_repository(repo_id, new_name, new_url)
            update_repository_status(repo_id, new_status)
            messagebox.showinfo("Sucesso", "Repositório atualizado com sucesso!")
            edit_window.destroy()
            self.display_repositories()
        else:
            messagebox.showwarning("Erro", "Nome e URL não podem estar vazios.")

    def delete_repository(self):
        selected_item = self.repo_tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um repositório para excluir.")
            return

        repo_id = self.repo_tree.item(selected_item)["values"][0]
        confirm = messagebox.askyesno("Confirmar", "Você tem certeza que deseja excluir este repositório?")
        if confirm:
            delete_repository(repo_id)
            messagebox.showinfo("Sucesso", "Repositório excluído com sucesso!")
            self.display_repositories()

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


def create_admin_window(version):
    admin_window = AdminWindow(version)
    admin_window.mainloop()


def create_login_window(version):
    from ui.login_window import LoginWindow
    login_window = LoginWindow(version)
    login_window.mainloop()
