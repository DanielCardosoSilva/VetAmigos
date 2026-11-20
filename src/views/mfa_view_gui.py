"""src/views/mfa_view_gui.py - Janela MFA (TOTP) com Tkinter para Proprietário."""

import tkinter as tk
from tkinter import ttk, messagebox


class MfaViewGUI:
    """Ecrã para configuração inicial (se necessário) e validação TOTP de 6 dígitos."""

    def __init__(self, root, funcionario, auth_controller, on_mfa_success, on_mfa_cancel):
        """Inicializa o ecrã MFA para o proprietário autenticado."""
        self.root = root
        self.funcionario = funcionario
        self.auth_controller = auth_controller
        self.on_mfa_success = on_mfa_success
        self.on_mfa_cancel = on_mfa_cancel

        self.root.title("VetAmigos - Autenticação MFA")
        self.root.geometry("460x360")
        self.root.resizable(False, False)

        self.codigo_var = tk.StringVar(master=self.root)
        self.dados_mfa = None

        if not getattr(self.funcionario, "mfa_secret", None):
            self.dados_mfa = self.auth_controller.configurar_mfa(
                self.funcionario.nome_utilizador
            )
            self.funcionario.mfa_secret = self.dados_mfa["secret"]

        self._criar_widgets()

    def _criar_widgets(self):
        """Cria e posiciona os widgets de configuração e validação MFA."""
        quadro = ttk.LabelFrame(
            self.root,
            text=" Verificação Multifator (MFA - TOTP) ",
            padding=15
        )
        quadro.pack(fill="both", expand=True, padx=18, pady=18)

        ttk.Label(
            quadro,
            text=f"Proprietário: {self.funcionario.nome}",
            font=("Arial", 10, "bold")
        ).pack(anchor="w", pady=(0, 8))

        if self.dados_mfa:
            ttk.Label(
                quadro,
                text="MFA configurado pela primeira vez. Registe o segredo na app autenticadora:",
                wraplength=400,
                font=("Arial", 9)
            ).pack(anchor="w", pady=(0, 4))

            txt_info = tk.Text(quadro, height=4, width=48, font=("Consolas", 9))
            txt_info.insert(
                "1.0",
                f"Segredo: {self.dados_mfa['secret']}\nURI: {self.dados_mfa['uri']}"
            )
            txt_info.configure(state="disabled")
            txt_info.pack(fill="x", pady=(0, 10))

        ttk.Label(
            quadro,
            text="Código de 6 dígitos:",
            font=("Arial", 10)
        ).pack(anchor="w", pady=(2, 2))

        entry_codigo = ttk.Entry(
            quadro,
            textvariable=self.codigo_var,
            font=("Arial", 12),
            width=16
        )
        entry_codigo.pack(anchor="w", pady=(0, 14))
        entry_codigo.focus()
        entry_codigo.bind("<Return>", lambda _event: self._validar_codigo())

        frame_botoes = ttk.Frame(quadro)
        frame_botoes.pack(fill="x", pady=(4, 0))

        ttk.Button(
            frame_botoes,
            text="Validar Código",
            command=self._validar_codigo
        ).pack(side="left", padx=(0, 8))

        ttk.Button(
            frame_botoes,
            text="Cancelar",
            command=self._cancelar
        ).pack(side="left")

    def _validar_codigo(self):
        """Valida o código TOTP introduzido e avança para o menu se for válido."""
        codigo = self.codigo_var.get().strip()
        if not codigo:
            messagebox.showwarning(
                "Código em falta",
                "Introduza o código MFA de 6 dígitos.",
                parent=self.root
            )
            return

        valido = self.auth_controller.verificar_mfa(
            self.funcionario.nome_utilizador,
            codigo
        )

        if valido:
            self.on_mfa_success(self.funcionario)
        else:
            messagebox.showerror(
                "MFA Inválido",
                "Código MFA incorreto ou expirado.",
                parent=self.root
            )
            self.codigo_var.set("")

    def _cancelar(self):
        """Cancela a verificação MFA e regressa ao ecrã de login."""
        self.on_mfa_cancel()