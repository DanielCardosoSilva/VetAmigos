"""Vista CLI de login."""
from getpass import getpass
from src.views.common_view import texto

def iniciar_sessao(controller):
    while True:
        print("\n========== INICIAR SESSÃO ==========")
        print("Introduza 0 no nome de utilizador para sair.")
        utilizador = texto("Nome de utilizador: ")
        if utilizador == "0":
            return None
        try:
            funcionario = controller.iniciar_sessao(utilizador, getpass("Palavra-passe: "))
            print(f"Bem-vindo(a), {funcionario.nome}!")
            return funcionario
        except ValueError as erro:
            print(f"Erro: {erro}")
#----------------------- alteracoes 17/11/2026------------------------
"""
Módulo de Login GUI (Tkinter) VetAmigos.
"""
import tkinter as tk
from tkinter import messagebox

class LoginViewGUI:
    """Janela gráfica de autenticação de utilizadores."""
    
    def __init__(self, root, auth_controller, on_login_success):
        self.root = root
        self.auth_controller = auth_controller
        self.on_login_success = on_login_success
        
        self.root.title("VetAmigos - Login")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Variáveis de controlo para os campos de entrada
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        
        self._criar_widgets()

    def _criar_widgets(self):
        """Cria e posiciona os componentes visuais da janela de login (T1.1)."""
        # Título principal da clínica
        lbl_titulo = tk.Label(self.root, text="VetAmigos - Clínica Veterinária", font=("Arial", 14, "bold"))
        lbl_titulo.pack(pady=20)
        
        # LabelFrame de Autenticação (T1.1)
        frame_auth = tk.LabelFrame(self.root, text=" Autenticação ", font=("Arial", 11, "bold"), padx=20, pady=20)
        frame_auth.pack(padx=20, pady=5, fill="both", expand=True)
        
        # Campo Nome de Utilizador
        lbl_user = tk.Label(frame_auth, text="Nome de Utilizador:", font=("Arial", 10))
        lbl_user.pack(anchor="w", pady=(0, 2))
        self.entry_user = tk.Entry(frame_auth, textvariable=self.username_var, font=("Arial", 11), width=25)
        self.entry_user.pack(anchor="w", pady=(0, 10))
        self.entry_user.focus()  # Dar foco inicial ao campo de utilizador
        
        # Campo Palavra-passe
        lbl_pass = tk.Label(frame_auth, text="Palavra-passe:", font=("Arial", 10))
        lbl_pass.pack(anchor="w", pady=(0, 2))
        self.entry_pass = tk.Entry(frame_auth, textvariable=self.password_var, show="*", font=("Arial", 11), width=25)
        self.entry_pass.pack(anchor="w", pady=(0, 15))
        self.entry_pass.bind("<Return>", lambda event: self.tentar_login())
        
        # Botão Entrar que chama o auth_controller.autenticar() (T1.1)
        btn_entrar = tk.Button(
            frame_auth, text="Entrar", bg="#4CAF50", fg="white", 
            font=("Arial", 11, "bold"), width=15, command=self.tentar_login
        )
        btn_entrar.pack(anchor="center")

    def tentar_login(self):
        """Valida as credenciais introduzidas e gere o sucesso ou erro de autenticação (T1.1 e T1.2)."""
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        
        if not username or not password:
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.")
            return
            
        # Autenticar através do controller existente
        funcionario = self.auth_controller.autenticar(username, password)
        
        if funcionario:
            messagebox.showinfo("Sucesso", f"Bem-vindo(a), {funcionario.nome}!")
            self.on_login_success(funcionario)
        else:
            # Tratamento de erro (T1.2): messagebox.showerror, limpar campos e focar no utilizador
            messagebox.showerror("Erro de Autenticação", "Nome de utilizador ou palavra-passe incorretos.")
            self.username_var.set("")
            self.password_var.set("")
            self.entry_user.focus()
