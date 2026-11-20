"""Janela gráfica de verificação multifator TOTP."""

import tkinter as tk
from tkinter import ttk, messagebox


class MfaViewGUI:
    """Configura e valida o MFA para contas de Proprietário."""

    def __init__(
        self,
        root,
        funcionario,
        auth_controller,
        on_mfa_success,
        on_mfa_cancel
    ):
        """Inicializa o formulário de verificação multifator."""
        self.root = root
        self.funcionario = funcionario
        self.auth_controller = auth_controller
        self.on_mfa_success = on_mfa_success
        self.on_mfa_cancel = on_mfa_cancel

        self.codigo_var = tk.StringVar(master=root)
        self.dados_mfa = None

        self.root.title("VetAmigos - Autenticação MFA")
        self.root.geometry("520x420")
        self.root.resizable(False, False)

        if not getattr(funcionario, "mfa_secret", None):
            try:
                self.dados_mfa = auth_controller.configurar_mfa(
                    funcionario.nome_utilizador
                )
            except Exception as erro:
                messagebox.showerror(
                    "Erro de MFA", str(erro), parent=root
                )
                self.root.after_idle(self.on_mfa_cancel)
                return

        self._criar_widgets()

    def _criar_widgets(self):
        """Cria os campos de configuração e verificação do MFA."""
        quadro = ttk.LabelFrame(
            self.root,
            text="Autenticação Multifator (TOTP)",
            padding=15
        )
        quadro.pack(fill="both", expand=True, padx=18, pady=18)

        ttk.Label(
            quadro,
            text=f"Proprietário: {self.funcionario.nome}",
            font=("Arial", 11, "bold")
        ).pack(anchor="w", pady=(0, 12))

        if self.dados_mfa:
            ttk.Label(
                quadro,
                text=(
                    "Primeira configuração: introduza este segredo "
                    "na aplicação autenticadora e confirme o código."
                ),
                wraplength=460
            ).pack(anchor="w", pady=(0, 8))

            informacao = tk.Text(
                quadro, height=5, width=55, wrap="word"
            )
            informacao.insert(
                "1.0",
                f"Segredo:\n{self.dados_mfa['secret']}\n\n"
                f"URI:\n{self.dados_mfa['uri']}"
            )
            informacao.config(state="disabled")
            informacao.pack(fill="x", pady=(0, 12))
        else:
            ttk.Label(
                quadro,
                text="Introduza o código da sua aplicação autenticadora."
            ).pack(anchor="w", pady=(0, 12))

        ttk.Label(
            quadro,
            text="Código de 6 dígitos:"
        ).pack(anchor="w", pady=(0, 4))

        entrada = ttk.Entry(
            quadro,
            textvariable=self.codigo_var,
            width=18,
            font=("Arial", 13)
        )
        entrada.pack(anchor="w", pady=(0, 16))
        entrada.focus_set()
        entrada.bind(
            "<Return>",
            lambda evento: self._validar_codigo()
        )

        botoes = ttk.Frame(quadro)
        botoes.pack(fill="x", pady=8)

        ttk.Button(
            botoes,
            text="Validar Código",
            command=self._validar_codigo
        ).pack(side="left", padx=(0, 10))

        ttk.Button(
            botoes,
            text="Cancelar",
            command=self._cancelar
        ).pack(side="left")

    def _validar_codigo(self):
        """Confirma o TOTP antes de permitir o acesso ao menu."""
        codigo = self.codigo_var.get().strip()

        if (
            len(codigo) != 6
            or not codigo.isascii()
            or not codigo.isdecimal()
        ):
            messagebox.showwarning(
                "Código inválido",
                "Introduza exatamente 6 dígitos.",
                parent=self.root
            )
            return

        try:
            valido = self.auth_controller.verificar_mfa(
                self.funcionario.nome_utilizador,
                codigo
            )
        except Exception as erro:
            messagebox.showerror(
                "Erro de MFA",
                str(erro),
                parent=self.root
            )
            return

        if valido:
            self.on_mfa_success(self.funcionario)
            return

        self.codigo_var.set("")

        messagebox.showerror(
            "MFA inválido",
            "O código está incorreto, expirou ou já foi utilizado.",
            parent=self.root
        )

    def _cancelar(self):
        """Cancela a autenticação e regressa ao login."""
        self.on_mfa_cancel()