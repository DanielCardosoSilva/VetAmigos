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
        horario,
        motivo=""
    ):
        if not isinstance(motivo, str) or not motivo.strip():
            raise ValueError("O motivo da consulta é obrigatório.")

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
            horario=horario,
            motivo=motivo.strip()
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

    def concluir(self, id_consulta, medico, diagnostico, tratamento,
                 sumario, custo, peso_registado):
        from src.models.medico_veterinario import MedicoVeterinario
        if not isinstance(medico, MedicoVeterinario) or not getattr(medico, "ativo", True):
            raise ValueError("Apenas médicos veterinários ativos podem concluir consultas.")
        consulta = self._repo.obter_por_id(id_consulta)
        if consulta is None:
            raise ValueError("A consulta indicada não existe.")
        if consulta.estado != "Agendada":
            raise ValueError("Apenas consultas agendadas podem ser concluídas.")
        if consulta.cedula_profissional != medico.cedula_profissional:
            raise ValueError("Apenas o veterinário responsável pode concluir esta consulta.")
        for nome, valor in (("diagnóstico", diagnostico), ("tratamento", tratamento), ("sumário", sumario)):
            if not isinstance(valor, str) or not valor.strip():
                raise ValueError(f"O {nome} é obrigatório.")
        try:
            custo = float(custo)
            peso_registado = float(peso_registado)
        except (ValueError, TypeError):
            raise ValueError("O custo e o peso devem ser numéricos.") from None
        from math import isfinite
        if not isfinite(custo) or custo < 0:
            raise ValueError("O custo deve ser um número não negativo.")
        if not isfinite(peso_registado) or peso_registado <= 0:
            raise ValueError("O peso registado deve ser positivo.")
        if self._animal_repo.obter_por_id(consulta.id_animal) is None:
            raise ValueError("O animal da consulta não existe.")
        resultado = self._repo.concluir(
            id_consulta, medico.cedula_profissional, diagnostico.strip(),
            tratamento.strip(), sumario.strip(), custo, peso_registado, datetime.now()
        )
        if not resultado:
            raise ValueError("Não foi possível concluir a consulta; o estado pode ter sido alterado.")
        return self._repo.obter_por_id(id_consulta)
