"""Menu principal gráfico do VetAmigos com controlo RBAC."""

import tkinter as tk
from tkinter import ttk, messagebox

from src.rbac import PERMISSOES, autorizar_modulo
from src.views.cliente_view_gui import ClienteViewGUI
from src.views.animal_view_gui import AnimalViewGUI
from src.views import (
    consulta_view_gui,
    vacina_view_gui,
    fatura_view_gui,
    relatorio_view_gui
)


class MenuViewGUI:
    """Apresenta os módulos autorizados ao funcionário autenticado."""

    def __init__(
        self, root, funcionario, controllers, token, on_logout
    ):
        """Guarda a sessão e apresenta o menu correspondente ao perfil."""
        self.root = root
        self.funcionario = funcionario
        self.controllers = controllers
        self.token = token
        self.on_logout = on_logout

        self.root.title("VetAmigos - Menu Principal")
        self.root.geometry("780x590")
        self.root.resizable(False, False)

        self._criar_widgets()

    def _executar(self, modulo, operacao):
        """Verifica o JWT e o RBAC antes de abrir um módulo."""
        try:
            autorizar_modulo(self.token, modulo)
            operacao()
        except PermissionError as erro:
            messagebox.showerror(
                "Acesso negado",
                str(erro),
                parent=self.root
            )

            if (
                "Sessão" in str(erro)
                or "sessão" in str(erro)
                or "Não autenticado" in str(erro)
                or "Conta inexistente" in str(erro)
                or "Conta desativada" in str(erro)
            ):
                self.terminar_sessao()
        except Exception as erro:
            messagebox.showerror(
                "Erro ao abrir módulo",
                str(erro),
                parent=self.root
            )

    def _criar_widgets(self):
        """Cria os botões e aplica as permissões do perfil autenticado."""
        topo = ttk.Frame(self.root, padding=15)
        topo.pack(fill="x")

        ttk.Label(
            topo,
            text="VetAmigos",
            font=("Arial", 18, "bold")
        ).pack(side="left")

        ttk.Button(
            topo,
            text="Terminar Sessão",
            command=self.terminar_sessao
        ).pack(side="right")

        ttk.Label(
            self.root,
            text=(
                f"Utilizador: {self.funcionario.nome} | "
                f"Perfil: {self.funcionario.tipo}"
            ),
            font=("Arial", 11)
        ).pack(anchor="w", padx=20, pady=(0, 12))

        quadro = ttk.LabelFrame(
            self.root,
            text="Módulos disponíveis",
            padding=20
        )
        quadro.pack(
            fill="both", expand=True, padx=20, pady=10
        )

        for coluna in range(3):
            quadro.columnconfigure(coluna, weight=1)

        modulos = [
            ("Gerir Clientes", "cliente", self.abrir_clientes),
            ("Gerir Animais", "animal", self.abrir_animais),
            ("Gerir Consultas", "consulta", self.abrir_consultas),
            ("Gerir Vacinação", "vacina", self.abrir_vacinacao),
            ("Gerir Medicamentos", "medicamento", None),
            ("Gerir Receitas", "receita", None),
            ("Gerir Faturas", "fatura", self.abrir_faturas),
            ("Consultar Relatórios", "relatorio", self.abrir_relatorios),
            ("Gerir Funcionários", "funcionario", None)
        ]

        for indice, (titulo, modulo, operacao) in enumerate(modulos):
            # Ativar apenas funcionalidades implementadas e permitidas.
            permitido = (
                self.funcionario.tipo in PERMISSOES[modulo]
                and operacao is not None
            )

            ttk.Button(
                quadro,
                text=titulo,
                width=23,
                state="normal" if permitido else "disabled",
                command=(
                    lambda m=modulo, f=operacao:
                    self._executar(m, f)
                ) if permitido else None
            ).grid(
                row=indice // 3,
                column=indice % 3,
                padx=8,
                pady=15,
                ipadx=5,
                ipady=12,
                sticky="ew"
            )

        ttk.Label(
            quadro,
            text=(
                "Os módulos sem interface gráfica própria "
                "permanecem temporariamente indisponíveis."
            ),
            wraplength=650,
            foreground="gray"
        ).grid(
            row=3, column=0, columnspan=3,
            pady=(25, 0)
        )

    def terminar_sessao(self):
        """Termina a sessão e regressa ao login."""
        self.on_logout()

    def abrir_clientes(self):
        """Abre a gestão de clientes."""
        ClienteViewGUI(
            self.root,
            self.controllers["cliente"]
        )

    def abrir_animais(self):
        """Abre a gestão de animais."""
        AnimalViewGUI(
            self.root,
            self.controllers["animal"],
            self.controllers["cliente"]
        )

    def abrir_consultas(self):
        """Abre a gestão de consultas."""
        consulta_view_gui.abrir(
            self.controllers["consulta"],
            self.controllers["animal"],
            funcionario=self.funcionario,
            pai=self.root
        )

    def abrir_vacinacao(self):
        """Abre a gestão de vacinação."""
        vacina_view_gui.abrir(
            self.controllers["vacina"],
            self.controllers["animal"],
            pai=self.root
        )

    def abrir_faturas(self):
        """Abre a gestão de faturas."""
        fatura_view_gui.abrir(
            self.controllers["fatura"],
            self.controllers["consulta"],
            self.controllers["animal"],
            self.controllers["cliente"],
            pai=self.root
        )

    def abrir_relatorios(self):
        """Abre os relatórios de gestão."""
        relatorio_view_gui.abrir(
            self.controllers["relatorio"],
            pai=self.root
        )