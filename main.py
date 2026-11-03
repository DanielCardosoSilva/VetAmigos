
"""main.py"""

from getpass import getpass

from db.connection import inicializar_bd

from src.models.proprietario import Proprietario
from src.models.medico_veterinario import MedicoVeterinario
from src.models.recepcionista import Rececionista

from src.repositories.cliente_repository import ClienteRepository
from src.repositories.animal_repository import AnimalRepository
from src.repositories.consulta_repository import ConsultaRepository
from src.repositories.registo_vacina_repository import RegistoVacinaRepository
from src.repositories.medicamento_repository import MedicamentoRepository
from src.repositories.medicamento_prescrito_repository import MedicamentoPrescritoRepository
from src.repositories.receita_repository import ReceitaRepository
from src.repositories.fatura_repository import FaturaRepository
from src.repositories.funcionario_repository import FuncionarioRepository

from src.services.cliente_service import ClienteService
from src.services.animal_service import AnimalService
from src.services.registo_vacina_service import RegistoVacinaService
from src.services.medicamento_service import MedicamentoService
from src.services.medicamento_prescrito_service import MedicamentoPrescritoService
from src.services.receita_service import ReceitaService
from src.services.fatura_service import FaturaService
from src.services.funcionario_service import FuncionarioService


def registar_proprietario_inicial(funcionario_repo, funcionario_service):
    if funcionario_repo.listar_todos():
        return

    print("\n========== CONFIGURAÇÃO INICIAL ==========")
    print("Não existem funcionários registados.")
    print("É necessário criar a conta do proprietário.")

    while True:
        nome = input("\nNome: ").strip()
        nome_utilizador = input("Nome de utilizador: ").strip()
        palavra_passe = getpass("Palavra-passe: ")
        confirmar = getpass("Confirmar palavra-passe: ")

        if not nome or not nome_utilizador or not palavra_passe:
            print("\nErro: Todos os campos são obrigatórios.")
            continue

        if palavra_passe != confirmar:
            print("\nErro: As palavras-passe não coincidem.")
            continue

        proprietario = Proprietario(nome, nome_utilizador, "")

        try:
            funcionario_service.registar(proprietario, palavra_passe)
            print("\nConta do proprietário criada com sucesso!")
            return

        except ValueError as erro:
            print(f"\nErro: {erro}")


def iniciar_sessao(funcionario_service):
    while True:
        print("\n========== INICIAR SESSÃO ==========")
        print("Introduza 0 no nome de utilizador para sair.")

        nome_utilizador = input("\nNome de utilizador: ").strip()

        if nome_utilizador == "0":
            return None

        palavra_passe = getpass("Palavra-passe: ")

        try:
            funcionario = funcionario_service.iniciar_sessao(
                nome_utilizador, palavra_passe
            )

            print(f"\nBem-vindo(a), {funcionario.nome}!")
            return funcionario

        except ValueError as erro:
            print(f"\nErro: {erro}")


def registar_novo_funcionario(funcionario_atual, funcionario_service):
    if not isinstance(funcionario_atual, Proprietario):
        print("\nErro: Não tem permissão para registar funcionários.")
        return

    while True:
        print("\n========== REGISTAR FUNCIONÁRIO ==========")
        print("1. Proprietário")
        print("2. Médico Veterinário")
        print("3. Rececionista")
        print("0. Voltar")

        tipo = input("\nEscolha o tipo de funcionário: ").strip()

        if tipo == "0":
            return

        if tipo not in ("1", "2", "3"):
            print("\nOpção inválida.")
            continue

        nome = input("\nNome: ").strip()
        nome_utilizador = input("Nome de utilizador: ").strip()

        cedula_profissional = None

        if tipo == "2":
            cedula_profissional = input("Cédula profissional: ").strip()

        palavra_passe = getpass("Palavra-passe: ")
        confirmar = getpass("Confirmar palavra-passe: ")

        if not nome or not nome_utilizador or not palavra_passe:
            print("\nErro: Todos os campos são obrigatórios.")
            continue

        if tipo == "2" and not cedula_profissional:
            print("\nErro: A cédula profissional é obrigatória.")
            continue

        if palavra_passe != confirmar:
            print("\nErro: As palavras-passe não coincidem.")
            continue

        if tipo == "1":
            novo_funcionario = Proprietario(
                nome, nome_utilizador, ""
            )

        elif tipo == "2":
            novo_funcionario = MedicoVeterinario(
                nome, nome_utilizador, "", cedula_profissional
            )

        else:
            novo_funcionario = Rececionista(
                nome, nome_utilizador, ""
            )

        try:
            funcionario_service.registar_por_proprietario(
                novo_funcionario,
                palavra_passe,
                funcionario_atual
            )

            print("\nFuncionário registado com sucesso!")
            return

        except ValueError as erro:
            print(f"\nErro: {erro}")


def menu_principal(funcionario, funcionario_service):
    if isinstance(funcionario, Proprietario):
        opcoes = {
            "1": "Gerir clientes",
            "2": "Gerir animais",
            "3": "Gerir consultas",
            "4": "Gerir vacinação",
            "5": "Gerir medicamentos",
            "6": "Gerir receitas",
            "7": "Gerir faturas e pagamentos",
            "8": "Consultar relatórios",
            "9": "Registar funcionário"
        }

    elif isinstance(funcionario, MedicoVeterinario):
        opcoes = {
            "1": "Gerir consultas",
            "2": "Gerir vacinação",
            "3": "Gerir medicamentos",
            "4": "Gerir receitas"
        }

    elif isinstance(funcionario, Rececionista):
        opcoes = {
            "1": "Gerir clientes",
            "2": "Gerir animais",
            "3": "Gerir consultas",
            "4": "Gerir faturas e pagamentos"
        }

    else:
        print("\nErro: Tipo de funcionário não reconhecido.")
        return

    while True:
        print("\n" + "=" * 40)
        print("           VETAMIGOS")
        print(f"Utilizador: {funcionario.nome}")
        print(f"Perfil: {funcionario.tipo}")
        print("=" * 40)

        for numero, descricao in opcoes.items():
            print(f"{numero}. {descricao}")

        print("0. Terminar sessão")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "0":
            print("\nSessão terminada.")
            return

        elif opcao not in opcoes:
            print("\nOpção inválida. Tente novamente.")

        elif isinstance(funcionario, Proprietario) and opcao == "9":
            registar_novo_funcionario(
                funcionario, funcionario_service
            )

        else:
            print("\nFuncionalidade ainda não implementada.")


def main():
    inicializar_bd()

    # Repositórios
    cliente_repo = ClienteRepository()
    animal_repo = AnimalRepository()
    consulta_repo = ConsultaRepository()
    vacina_repo = RegistoVacinaRepository()
    medicamento_repo = MedicamentoRepository()
    medicamento_prescrito_repo = MedicamentoPrescritoRepository()
    receita_repo = ReceitaRepository()
    fatura_repo = FaturaRepository()
    funcionario_repo = FuncionarioRepository()

    # Serviços
    cliente_service = ClienteService(cliente_repo)
    animal_service = AnimalService(animal_repo, cliente_repo)
    vacina_service = RegistoVacinaService(vacina_repo, animal_repo)
    medicamento_service = MedicamentoService(medicamento_repo)

    medicamento_prescrito_service = MedicamentoPrescritoService(
        medicamento_prescrito_repo,
        receita_repo,
        medicamento_repo
    )

    receita_service = ReceitaService(receita_repo, consulta_repo)
    fatura_service = FaturaService(fatura_repo, consulta_repo)
    funcionario_service = FuncionarioService(funcionario_repo)

    print("=" * 40)
    print("           VETAMIGOS")
    print("  Sistema de Gestão Veterinária")
    print("=" * 40)

    # Configuração inicial do proprietário
    registar_proprietario_inicial(
        funcionario_repo,
        funcionario_service
    )

    # Autenticação e menu principal
    while True:
        funcionario = iniciar_sessao(funcionario_service)

        if funcionario is None:
            print("\nAplicação encerrada. Até à próxima!")
            break

        menu_principal(funcionario, funcionario_service)


if __name__ == "__main__":
    main()
