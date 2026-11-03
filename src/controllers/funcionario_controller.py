
"""src/controllers/funcionario_controller.py"""

from src.models.proprietario import Proprietario
from src.models.medico_veterinario import MedicoVeterinario
from src.models.recepcionista import Rececionista


class FuncionarioController:

    def __init__(self, service, repo):
        self.service = service
        self.repo = repo

    def necessita_proprietario(self):
        return not bool(self.repo.listar_todos())

    def registar_inicial(
        self,
        nome,
        utilizador,
        palavra_passe
    ):
        if not self.necessita_proprietario():
            raise ValueError(
                "Já existem funcionários registados."
            )

        proprietario = Proprietario(
            nome,
            utilizador,
            ""
        )

        return self.service.registar(
            proprietario,
            palavra_passe
        )

    def registar(
        self,
        atual,
        tipo,
        nome,
        utilizador,
        palavra_passe,
        cedula=None
    ):
        classes = {
            "1": Proprietario,
            "2": MedicoVeterinario,
            "3": Rececionista
        }

        if tipo not in classes:
            raise ValueError(
                "Tipo de funcionário inválido."
            )

        if tipo == "2":
            if not cedula:
                raise ValueError(
                    "A cédula profissional é obrigatória."
                )

            novo = MedicoVeterinario(
                nome,
                utilizador,
                "",
                cedula
            )
        else:
            novo = classes[tipo](
                nome,
                utilizador,
                ""
            )

        return self.service.registar_por_proprietario(
            novo,
            palavra_passe,
            atual
        )

    def listar(self, funcionario_atual):
        return self.service.listar_por_proprietario(
            funcionario_atual
        )

    def desativar(
        self,
        id_funcionario,
        funcionario_atual
    ):
        return self.service.desativar_por_proprietario(
            id_funcionario,
            funcionario_atual
        )

    def reativar(
        self,
        id_funcionario,
        funcionario_atual
    ):
        return self.service.reativar_por_proprietario(
            id_funcionario,
            funcionario_atual
        )
