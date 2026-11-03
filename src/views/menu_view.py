
"""src/views/menu_view.py"""

from src.models.proprietario import Proprietario
from src.models.medico_veterinario import MedicoVeterinario
from src.models.recepcionista import Rececionista

from src.views.common_view import texto

from src.views import (
    cliente_view,
    animal_view,
    consulta_view,
    vacina_view,
    medicamento_view,
    receita_view,
    fatura_view,
    relatorio_view,
    funcionario_view
)


def abrir(funcionario, controllers):
    opcoes = {
        "Gerir clientes": lambda: cliente_view.abrir(
            controllers["cliente"]
        ),
        "Gerir animais": lambda: animal_view.abrir(
            controllers["animal"]
        ),
        "Gerir consultas": lambda: consulta_view.abrir(
            controllers["consulta"]
        ),
        "Gerir vacinação": lambda: vacina_view.abrir(
            controllers["vacina"]
        ),
        "Gerir medicamentos": lambda: medicamento_view.abrir(
            controllers["medicamento"]
        ),
        "Gerir receitas": lambda: receita_view.abrir(
            controllers["receita"]
        ),
        "Gerir faturas e pagamentos": lambda: fatura_view.abrir(
            controllers["fatura"]
        ),
        "Consultar relatórios": lambda: relatorio_view.abrir(
            controllers["relatorio"]
        ),
        "Gerir funcionários": lambda: funcionario_view.abrir(
            controllers["funcionario"],
            funcionario
        )
    }

    if isinstance(funcionario, Proprietario):
        nomes = list(opcoes)

    elif isinstance(funcionario, MedicoVeterinario):
        nomes = [
            "Gerir consultas",
            "Gerir vacinação",
            "Gerir medicamentos",
            "Gerir receitas"
        ]

    elif isinstance(funcionario, Rececionista):
        nomes = [
            "Gerir clientes",
            "Gerir animais",
            "Gerir consultas",
            "Gerir faturas e pagamentos"
        ]

    else:
        print(
            "\nTipo de funcionário não reconhecido."
        )
        return

    while True:
        print("\n========== VETAMIGOS ==========")
        print(
            f"Utilizador: {funcionario.nome} | "
            f"Perfil: {funcionario.tipo}"
        )

        for numero, nome in enumerate(nomes, 1):
            print(f"{numero}. {nome}")

        print("0. Terminar sessão")

        opcao = texto("\nEscolha uma opção: ")

        if opcao == "0":
            print("\nSessão terminada.")
            return

        if (
            not opcao.isdigit()
            or not 1 <= int(opcao) <= len(nomes)
        ):
            print("\nOpção inválida.")
            continue

        opcoes[nomes[int(opcao) - 1]]()
