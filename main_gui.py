"""Ponto de entrada da aplicação VetAmigos em modo gráfico."""

import tkinter as tk
from tkinter import ttk, messagebox

from db.connection import inicializar_bd
from main import construir_controllers
from src.models.proprietario import Proprietario
from src.views.login_view_gui import LoginViewGUI
from src.views.mfa_view_gui import MfaViewGUI
from src.views.menu_view_gui import MenuViewGUI


def iniciar_aplicacao():
    """Inicializa a base de dados e inicia o ciclo gráfico da aplicação."""
    inicializar_bd()
    controllers = construir_controllers()

    root = tk.Tk()
    root.title("VetAmigos")
    root.geometry("420x320")

    def limpar_janela():
        """Remove os widgets atuais sem destruir a janela principal."""
        for widget in root.winfo_children():
            widget.destroy()

    def alternar_para_login():
        """Apresenta o formulário de autenticação."""
        limpar_janela()

        LoginViewGUI(
            root,
            controllers["auth"],
            apos_login_sucesso
        )

    def apos_login_sucesso(funcionario):
        """Encaminha para verificação MFA se for Proprietário ou abre diretamente o menu."""
        if isinstance(funcionario, Proprietario):
            limpar_janela()
            MfaViewGUI(
                root,
                funcionario,
                controllers["auth"],
                on_mfa_success=alternar_para_menu,
                on_mfa_cancel=alternar_para_login
            )
            return

        alternar_para_menu(funcionario)

    def alternar_para_menu(funcionario):
        """Apresenta o menu correspondente ao funcionário autenticado."""
        limpar_janela()

        MenuViewGUI(
            root,
            funcionario,
            controllers,
            on_logout=alternar_para_login
        )

    def configuracao_inicial():
        """Cria a primeira conta de proprietário quando necessário."""
        limpar_janela()

        root.title("VetAmigos - Configuração Inicial")
        root.geometry("440x410")

        quadro = ttk.LabelFrame(
            root,
            text="Criar conta de proprietário",
            padding=20
        )
        quadro.pack(fill="both", expand=True, padx=20, pady=20)

        ttk.Label(
            quadro,
            text="Configuração inicial da clínica",
            font=("Arial", 13, "bold")
        ).pack(pady=(0, 15))

        nome_var = tk.StringVar(master=root)
        utilizador_var = tk.StringVar(master=root)
        palavra_passe_var = tk.StringVar(master=root)
        confirmar_var = tk.StringVar(master=root)

        campos = [
            ("Nome:", nome_var, False),
            ("Nome de utilizador:", utilizador_var, False),
            ("Palavra-passe:", palavra_passe_var, True),
            ("Confirmar palavra-passe:", confirmar_var, True)
        ]

        for rotulo, variavel, secreta in campos:
            ttk.Label(quadro, text=rotulo).pack(
                anchor="w", pady=(4, 2)
            )

            ttk.Entry(
                quadro,
                textvariable=variavel,
                show="*" if secreta else "",
                width=35
            ).pack(fill="x", pady=(0, 6))

        def guardar_proprietario():
            """Valida os dados e regista a conta inicial."""
            nome = nome_var.get().strip()
            utilizador = utilizador_var.get().strip()
            palavra_passe = palavra_passe_var.get()
            confirmar = confirmar_var.get()

            if not nome or not utilizador or not palavra_passe:
                messagebox.showwarning(
                    "Campos obrigatórios",
                    "Preencha todos os campos.",
                    parent=root
                )
                return

            if palavra_passe != confirmar:
                messagebox.showerror(
                    "Palavras-passe diferentes",
                    "As palavras-passe não coincidem.",
                    parent=root
                )
                return

            try:
                controllers["funcionario"].registar_inicial(
                    nome,
                    utilizador,
                    palavra_passe
                )
            except Exception as erro:
                messagebox.showerror(
                    "Erro na configuração",
                    str(erro),
                    parent=root
                )
                return

            messagebox.showinfo(
                "Configuração concluída",
                "A conta de proprietário foi criada com sucesso.",
                parent=root
            )
            alternar_para_login()

        ttk.Button(
            quadro,
            text="Criar Proprietário",
            command=guardar_proprietario
        ).pack(pady=15)

    if controllers["funcionario"].necessita_proprietario():
        configuracao_inicial()
    else:
        alternar_para_login()

    root.mainloop()


if __name__ == "__main__":
    iniciar_aplicacao()