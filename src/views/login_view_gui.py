"""Interface gráfica de autenticação do VetAmigos."""

import tkinter as tk
from tkinter import ttk, messagebox


class LoginViewGUI:
    """Apresenta o formulário de autenticação dos funcionários."""

    def __init__(self, root, auth_controller, on_login_success):
        # Guardar as dependências e preparar o formulário de login.
        self.root = root
        self.auth_controller = auth_controller
        self.on_login_success = on_login_success

        self.root.title("VetAmigos - Login")
        self.root.geometry("420x320")
        self.root.resizable(False, False)

        self.username_var = tk.StringVar(master=root)
        self.password_var = tk.StringVar(master=root)

        self._criar_widgets()

    def _criar_widgets(self):
        # Construir os campos de autenticação e o botão de entrada.
        ttk.Label(
            self.root,
            text="VetAmigos - Clínica Veterinária",
            font=("Arial", 15, "bold")
        ).pack(pady=(25, 15))

        frame_auth = ttk.LabelFrame(
            self.root, text="Autenticação", padding=20
        )
        frame_auth.pack(fill="both", expand=True, padx=25, pady=(0, 20))

        ttk.Label(
            frame_auth, text="Nome de utilizador:"
        ).pack(anchor="w", pady=(0, 3))

        self.entry_user = ttk.Entry(
            frame_auth,
            textvariable=self.username_var,
            width=30
        )
        self.entry_user.pack(fill="x", pady=(0, 12))

        ttk.Label(
            frame_auth, text="Palavra-passe:"
        ).pack(anchor="w", pady=(0, 3))

        self.entry_pass = ttk.Entry(
            frame_auth,
            textvariable=self.password_var,
            show="*",
            width=30
        )
        self.entry_pass.pack(fill="x", pady=(0, 18))
        self.entry_pass.bind("<Return>", lambda evento: self.tentar_login())

        ttk.Button(
            frame_auth,
            text="Entrar",
            command=self.tentar_login
        ).pack()

        self.entry_user.focus_set()

    def tentar_login(self):
        # Validar os campos e autenticar através do controller existente.
        utilizador = self.username_var.get().strip()
        palavra_passe = self.password_var.get()

        if not utilizador or not palavra_passe:
            messagebox.showwarning(
                "Campos obrigatórios",
                "Introduza o nome de utilizador e a palavra-passe.",
                parent=self.root
            )
            self.entry_user.focus_set()
            return

        try:
            funcionario = self.auth_controller.iniciar_sessao(
                utilizador, palavra_passe
            )
        except Exception as erro:
            messagebox.showerror(
                "Erro de autenticação",
                str(erro),
                parent=self.root
            )
            self.password_var.set("")
            self.entry_pass.focus_set()
            return

        if funcionario is None:
            messagebox.showerror(
                "Autenticação falhada",
                "Nome de utilizador ou palavra-passe incorretos.",
                parent=self.root
            )
            self.username_var.set("")
            self.password_var.set("")
            self.entry_user.focus_set()
            return

        self.password_var.set("")
        self.on_login_success(funcionario)
