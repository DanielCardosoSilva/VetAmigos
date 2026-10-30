"""src/services/consulta_service.py"""

from datetime import datetime
from src.models.consulta import Consulta


class ConsultaService:
    def __init__(self, consulta_repo, animal_repo):
        self._repo = consulta_repo
        self._animal_repo = animal_repo

    def agendar(
        self,
        id_animal,
        cedula_profissional,
        horario
    ):
        if not isinstance(horario, datetime):
            raise ValueError("O horário tem de ser uma data válida.")

        if horario < datetime.now():
            raise ValueError("O horário da consulta não pode ser no passado.")

        if self._animal_repo.obter_por_id(id_animal) is None:
            raise ValueError("O animal indicado não existe.")

        if not cedula_profissional.strip():
            raise ValueError("A cédula profissional não pode estar vazia.")

        consultas = self._repo.listar_por_animal(id_animal)

        for consulta in consultas:
            if consulta.horario == horario and consulta.estado != "Cancelada":
                raise ValueError(
                    "O animal já tem uma consulta agendada para esse horário."
                )

        consulta = Consulta(
            id_animal=id_animal,
            cedula_profissional=cedula_profissional.strip(),
            horario=horario
        )

        return self._repo.agendar(consulta)

    def listar_por_animal(self, id_animal):
        if self._animal_repo.obter_por_id(id_animal) is None:
            raise ValueError("O animal indicado não existe.")

        return self._repo.listar_por_animal(id_animal)

    def cancelar(self, id_consulta):
        if id_consulta <= 0:
            raise ValueError("O ID da consulta tem de ser positivo.")

        consulta = self._repo.obter_por_id(id_consulta)

        if consulta is None:
            raise ValueError("A consulta indicada não existe.")

        if consulta.estado == "Cancelada":
            raise ValueError("A consulta já está cancelada.")

        return self._repo.cancelar(id_consulta)