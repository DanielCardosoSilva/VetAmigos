
"""src/views/funcionario_view.py"""

from getpass import getpass

from src.views.common_view import menu, texto, inteiro


def pedir_credenciais():
    nome = texto("Nome: ")
    utilizador = texto("Nome de utilizador: ")
    palavra_passe = getpass("Palavra-passe: ")

    confirmar = getpass(
        "Confirmar palavra-passe: "
    )

    if palavra_passe != confirmar:
        raise ValueError(
            "As palavras-passe não coincidem."
        )

    if not nome or not utilizador or not palavra_passe:
        raise ValueError(
            "Todos os campos são obrigatórios."
        )

    return nome, utilizador, palavra_passe


def registar_inicial(controller):
    if not controller.necessita_proprietario():
        return

    print("\n========== CONFIGURAÇÃO INICIAL ==========")
    print("É necessário criar a conta do proprietário.")

    while True:
        try:
            controller.registar_inicial(
                *pedir_credenciais()
            )

            print(
                "\nProprietário criado com sucesso."
            )
            return

        except ValueError as erro:
            print(f"\nErro: {erro}")


def mostrar_funcionario(funcionario):
    estado = (
        "Ativo"
        if funcionario.ativo
        else "Inativo"
    )

    print(
        f"ID: {funcionario.id} | "
        f"Nome: {funcionario.nome} | "
        f"Utilizador: {funcionario.nome_utilizador}"
    )

    print(
        f"Perfil: {funcionario.tipo} | "
        f"Estado: {estado}"
    )

    cedula = getattr(
        funcionario,
        "cedula_profissional",
        None
    )

    if cedula:
        print(f"Cédula profissional: {cedula}")


def abrir(controller, funcionario_atual):

    def registar(tipo):
        nome = texto("Nome: ")
        utilizador = texto(
            "Nome de utilizador: "
        )

        cedula = None

        if tipo == "2":
            cedula = texto(
                "Cédula profissional: "
            )

        palavra_passe = getpass(
            "Palavra-passe: "
        )

        confirmar = getpass(
            "Confirmar palavra-passe: "
        )

        if palavra_passe != confirmar:
            raise ValueError(
                "As palavras-passe não coincidem."
            )

        controller.registar(
            funcionario_atual,
            tipo,
            nome,
            utilizador,
            palavra_passe,
            cedula
        )

        print(
            "\nFuncionário registado com sucesso."
        )

    def listar():
        funcionarios = controller.listar(
            funcionario_atual
        )

        if not funcionarios:
            print(
                "\nNão existem funcionários registados."
            )
            return

        print(
            "\n========== FUNCIONÁRIOS REGISTADOS =========="
        )

        for funcionario in funcionarios:
            mostrar_funcionario(funcionario)
            print("-" * 45)

        ativos = sum(
            funcionario.ativo
            for funcionario in funcionarios
        )

        print(
            f"Total: {len(funcionarios)} | "
            f"Ativos: {ativos} | "
            f"Inativos: {len(funcionarios) - ativos}"
        )

    def escolher_funcionario(ativo):
        funcionarios = [
            funcionario
            for funcionario in controller.listar(
                funcionario_atual
            )
            if funcionario.ativo == ativo
        ]

        if not funcionarios:
            estado = (
                "ativos" if ativo else "inativos"
            )
            print(
                f"\nNão existem funcionários {estado}."
            )
            return None

        for funcionario in funcionarios:
            mostrar_funcionario(funcionario)
            print("-" * 45)

        id_funcionario = inteiro(
            "\nID do funcionário: "
        )

        funcionario = next(
            (
                f for f in funcionarios
                if f.id == id_funcionario
            ),
            None
        )

        if funcionario is None:
            raise ValueError(
                "Funcionário não encontrado "
                "na lista apresentada."
            )

        return funcionario

    def desativar():
        print(
            "\n========== DESATIVAR FUNCIONÁRIO =========="
        )

        funcionario = escolher_funcionario(True)

        if funcionario is None:
            return

        if funcionario.id == funcionario_atual.id:
            raise ValueError(
                "Não pode desativar a sua própria conta."
            )

        print("\nFuncionário selecionado:")
        mostrar_funcionario(funcionario)

        confirmacao = texto(
            "\nConfirma a desativação? (S/N): "
        ).lower()

        if confirmacao != "s":
            print("\nOperação cancelada.")
            return

        if controller.desativar(
            funcionario.id,
            funcionario_atual
        ):
            print(
                "\nFuncionário desativado com sucesso."
            )

    def reativar():
        print(
            "\n========== REATIVAR FUNCIONÁRIO =========="
        )

        funcionario = escolher_funcionario(False)

        if funcionario is None:
            return

        print("\nFuncionário selecionado:")
        mostrar_funcionario(funcionario)

        confirmacao = texto(
            "\nConfirma a reativação? (S/N): "
        ).lower()

        if confirmacao != "s":
            print("\nOperação cancelada.")
            return

        if controller.reativar(
            funcionario.id,
            funcionario_atual
        ):
            print(
                "\nFuncionário reativado com sucesso."
            )

    menu(
        "Gerir funcionários",
        {
            "1": (
                "Registar proprietário",
                lambda: registar("1")
            ),
            "2": (
                "Registar médico veterinário",
                lambda: registar("2")
            ),
            "3": (
                "Registar rececionista",
                lambda: registar("3")
            ),
            "4": (
                "Listar funcionários",
                listar
            ),
            "5": (
                "Desativar funcionário",
                desativar
            ),
            "6": (
                "Reativar funcionário",
                reativar
            )
        }
    )
