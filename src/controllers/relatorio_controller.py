"""Controlador de relatorio."""

from datetime import datetime, date, timedelta


class RelatorioController:
    def __init__(self, cliente_service, animal_repo, consulta_repo, fatura_repo):
        # Guardar os serviços e repositórios necessários.
        self.cliente_service, self.animal_repo = cliente_service, animal_repo
        self.consulta_repo, self.fatura_repo = consulta_repo, fatura_repo

    def _consultas(self):
        # Obter as consultas de todos os animais registados.
        return [
            c for animal in self.animal_repo.listar_todos()
            for c in self.consulta_repo.listar_por_animal(animal.id)
        ]

    def resumo(self):
        # Calcular os indicadores gerais existentes.
        consultas = self._consultas()
        return {
            "clientes": len(self.cliente_service.listar()),
            "animais": len(self.animal_repo.listar_todos()),
            "consultas": len(consultas),
            "canceladas": sum(c.estado == "Cancelada" for c in consultas)
        }

    def mensal(self, periodo):
        # Gerar o relatório mensal original por médico.
        datetime.strptime(periodo, "%Y-%m")
        consultas = [
            c for c in self._consultas()
            if c.horario.strftime("%Y-%m") == periodo
        ]
        por_medico = {}
        faturado = 0.0
        for c in consultas:
            por_medico[c.cedula_profissional] = (
                por_medico.get(c.cedula_profissional, 0) + 1
            )
            fatura = self.fatura_repo.obter_por_consulta(c.id)
            if fatura:
                faturado += fatura.valor_total
        return {
            "consultas": len(consultas),
            "faturado": faturado,
            "por_medico": por_medico
        }

    def por_periodo(self, periodo):
        # Calcular indicadores filtrados pela data da consulta.
        hoje = date.today()

        if periodo == "Hoje":
            inicio = hoje
        elif periodo == "Semana":
            inicio = hoje - timedelta(days=hoje.weekday())
        elif periodo == "Mês":
            inicio = hoje.replace(day=1)
        elif periodo == "Ano":
            inicio = hoje.replace(month=1, day=1)
        else:
            raise ValueError("Período de relatório inválido.")

        consultas = [
            consulta for consulta in self._consultas()
            if inicio <= consulta.horario.date() <= hoje
        ]

        faturado = 0.0
        recebido = 0.0
        pendente = 0.0
        por_medico = {}

        for consulta in consultas:
            cedula = consulta.cedula_profissional
            por_medico[cedula] = por_medico.get(cedula, 0) + 1

            fatura = self.fatura_repo.obter_por_consulta(consulta.id)

            if fatura is None or fatura.estado == "Anulada":
                continue

            faturado += fatura.valor_total

            if fatura.estado == "Pago":
                recebido += fatura.valor_total
            elif fatura.estado == "Pendente":
                pendente += fatura.valor_total

        return {
            "periodo": periodo,
            "inicio": inicio,
            "fim": hoje,
            "clientes": len(self.cliente_service.listar()),
            "consultas": len(consultas),
            "canceladas": sum(
                consulta.estado == "Cancelada" for consulta in consultas
            ),
            "faturado": faturado,
            "recebido": recebido,
            "pendente": pendente,
            "por_medico": por_medico
        }
