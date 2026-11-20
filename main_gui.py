"""Ponto de entrada gráfico do VetAmigos com autenticação segura."""

import tkinter as tk
from tkinter import ttk, messagebox

from db.connection import inicializar_bd
from main import construir_controllers

from src.models.proprietario import Proprietario
from src.services.mfa_service import inicializar_mfa
from src.services.session import criar_token, terminar_sessao
from src.seguranca_controllers import proteger_controllers

from src.views.login_view_gui import LoginViewGUI
from src.views.mfa_view_gui import MfaViewGUI
from src.views.menu_view_gui import MenuViewGUI


def iniciar_aplicacao():
    """Inicializa a aplicação e gere o ciclo de autenticação."""
    inicializar_bd()
    inicializar_mfa()

    controllers = construir_controllers()

    root = tk.Tk()
    root.title("VetAmigos")
    root.geometry("420x320")

    token_atual = None

    def limpar_janela():
        """Remove os widgets e as janelas secundárias existentes."""
        for widget in root.winfo_children():
            widget.destroy()

    def encerrar_sessao():
        """Revoga o JWT atual antes de regressar ao login."""
        nonlocal token_atual

        if token_atual:
            terminar_sessao(token_atual)
            token_atual = None

        alternar_para_login()

    def alternar_para_login():
        """Apresenta o formulário de autenticação."""
        limpar_janela()

        LoginViewGUI(
            root,
            controllers["auth"],
            apos_login_sucesso
        )

    def apos_login_sucesso(funcionario):
        """Encaminha o proprietário para o MFA."""
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
        """Emite o JWT e apresenta o menu com controllers protegidos."""
        nonlocal token_atual

        try:
            token_atual = criar_token(
                funcionario,
                mfa_confirmado=isinstance(funcionario, Proprietario)
            )

            controllers_protegidos = proteger_controllers(
                controllers,
                token_atual
            )
        except Exception as erro:
            token_atual = None

            messagebox.showerror(
                "Erro na sessão",
                str(erro),
                parent=root
            )
            alternar_para_login()
            return

        limpar_janela()

        MenuViewGUI(
            root,
            funcionario,
            controllers_protegidos,
            token=token_atual,
            on_logout=encerrar_sessao
        )

    def configuracao_inicial():
        """Apresenta o registo inicial do proprietário."""
        limpar_janela()

        root.title("VetAmigos - Configuração Inicial")
        root.geometry("440x410")

        quadro = ttk.LabelFrame(
            root,
            text="Criar conta de proprietário",
            padding=20
        )
        quadro.pack(
            fill="both", expand=True, padx=20, pady=20
        )

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
            # Criar os campos de identificação e palavra-passe.
            ttk.Label(
                quadro, text=rotulo
            ).pack(anchor="w", pady=(4, 2))

            ttk.Entry(
                quadro,
                textvariable=variavel,
                show="*" if secreta else "",
                width=35
            ).pack(fill="x", pady=(0, 6))

        def guardar_proprietario():
            """Valida os dados e regista o proprietário inicial."""
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

            if (
                len(palavra_passe) < 8
                or len(palavra_passe.encode("utf-8")) > 72
            ):
                messagebox.showwarning(
                    "Palavra-passe inválida",
                    "Utilize pelo menos 8 caracteres e no máximo 72 bytes.",
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

    def fechar_aplicacao():
        """Revoga a sessão antes de fechar a aplicação."""
        nonlocal token_atual

        if token_atual:
            terminar_sessao(token_atual)
            token_atual = None

        root.destroy()

    root.protocol("WM_DELETE_WINDOW", fechar_aplicacao)

    if controllers["funcionario"].necessita_proprietario():
        configuracao_inicial()
    else:
        alternar_para_login()

    root.mainloop()


if __name__ == "__main__":
    iniciar_aplicacao()