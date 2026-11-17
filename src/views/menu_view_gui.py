"""Interface gráfica do menu principal do VetAmigos."""

import tkinter as tk
from tkinter import ttk

from src.models.proprietario import Proprietario
from src.models.medico_veterinario import MedicoVeterinario
from src.models.recepcionista import Rececionista

from src.views.cliente_view_gui import ClienteViewGUI
from src.views.animal_view_gui import AnimalViewGUI
from src.views import (
    consulta_view_gui,
    vacina_view_gui,
    fatura_view_gui,
    relatorio_view_gui
)


class MenuViewGUI:
    """Menu principal com permissões baseadas no perfil do funcionário."""

    def __init__(self, root, funcionario, controllers, on_logout):
        # Guardar o utilizador, os controllers e a função de saída.
        self.root = root
        self.funcionario = funcionario
        self.controllers = controllers
        self.on_logout = on_logout

        self.root.title("VetAmigos - Menu Principal")
        self.root.geometry("780x590")
        self.root.resizable(False, False)

        self._criar_widgets()

    def _obter_permissoes_por_perfil(self):
        # Aplicar as mesmas permissões de acesso da versão CLI.
        if isinstance(self.funcionario, Proprietario):
            return {
                "cliente", "animal", "consulta", "vacina",
                "medicamento", "receita", "fatura",
                "relatorio", "funcionario"
            }

        if isinstance(self.funcionario, MedicoVeterinario):
            return {
                "consulta", "vacina", "medicamento", "receita"
            }

        if isinstance(self.funcionario, Rececionista):
            return {
                "cliente", "animal", "consulta", "fatura"
            }

        return set()

    def _criar_widgets(self):
        # Construir a identificação do funcionário e o menu de módulos.
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
        quadro.pack(fill="both", expand=True, padx=20, pady=10)

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

        permissoes = self._obter_permissoes_por_perfil()

        for indice, (texto, chave, comando) in enumerate(modulos):
            # Ativar apenas os módulos permitidos e com interface GUI.
            permitido = chave in permissoes and comando is not None

            ttk.Button(
                quadro,
                text=texto,
                command=comando,
                state="normal" if permitido else "disabled",
                width=23
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
            row=3,
            column=0,
            columnspan=3,
            pady=(25, 0)
        )

    def terminar_sessao(self):
        # Voltar ao login sem destruir a janela principal.
        self.on_logout()

    def abrir_clientes(self):
        # Abrir a interface de clientes com o respetivo controller.
        ClienteViewGUI(
            self.root,
            self.controllers["cliente"]
        )

    def abrir_animais(self):
        # Abrir a interface de animais com os dois controllers necessários.
        AnimalViewGUI(
            self.root,
            self.controllers["animal"],
            self.controllers["cliente"]
        )

    def abrir_consultas(self):
        # Abrir a gestão de consultas com o funcionário autenticado.
        consulta_view_gui.abrir(
            self.controllers["consulta"],
            self.controllers["animal"],
            funcionario=self.funcionario,
            pai=self.root
        )

    def abrir_vacinacao(self):
        # Abrir a gestão de vacinação com seleção de animais.
        vacina_view_gui.abrir(
            self.controllers["vacina"],
            self.controllers["animal"],
            pai=self.root
        )

    def abrir_faturas(self):
        # Abrir a faturação com todos os controllers necessários.
        fatura_view_gui.abrir(
            self.controllers["fatura"],
            self.controllers["consulta"],
            self.controllers["animal"],
            self.controllers["cliente"],
            pai=self.root
        )

    def abrir_relatorios(self):
        # Abrir os relatórios utilizando o respetivo controller.
        relatorio_view_gui.abrir(
            self.controllers["relatorio"],
            pai=self.root
        )
