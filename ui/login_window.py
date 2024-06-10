import tkinter as tk
from tkinter import ttk, messagebox
from ui.main_window import create_main_window
from ui.admin_window import create_admin_window

class LoginWindow(tk.Tk):
    def __init__(self, version):
        super().__init__()
        self.title(f"Motor Executor - Login")
        self.geometry("400x200")
        self.resizable(False, False)

        self.create_widgets()
        self.version = version

    def create_widgets(self):
        self.username_label = ttk.Label(self, text="Username:")
        self.username_label.pack(pady=5)

        self.username_var = tk.StringVar()
        self.username_combobox = ttk.Combobox(self, textvariable=self.username_var, state="readonly")
        self.username_combobox['values'] = ("IH8", "admin")
        self.username_combobox.current(0)
        self.username_combobox.pack(pady=5)
        self.username_combobox.bind("<<ComboboxSelected>>", self.on_user_change)

        self.password_label = ttk.Label(self, text="Password:")
        self.password_label.pack(pady=5)
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        self.set_default_password()

        self.login_button = ttk.Button(self, text="Login", command=self.check_credentials)
        self.login_button.pack(pady=20)

        # Bind the Enter key to the password entry field
        self.password_entry.bind("<Return>", lambda event: self.check_credentials())

    def set_default_password(self):
        if self.username_var.get() == "IH8":
            self.password_entry.insert(0, "123456")
        else:
            self.password_entry.delete(0, tk.END)

    def on_user_change(self, event):
        self.password_entry.delete(0, tk.END)
        if self.username_var.get() == "IH8":
            self.set_default_password()

    def check_credentials(self):
        username = self.username_var.get()
        password = self.password_entry.get()
        if username == "IH8" and password == "123456":
            self.destroy()
            create_main_window(self.version)
        elif username == "admin" and password == "123":
            self.destroy()
            create_admin_window(self.version)
        else:
            messagebox.showerror("Error", "Invalid credentials")

def create_login_window(version):
    login_window = LoginWindow(version)
    login_window.mainloop()
