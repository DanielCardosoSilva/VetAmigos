"""Controlador de relatorio."""
from datetime import datetime

class RelatorioController:
    def __init__(self, cliente_service, animal_repo, consulta_repo, fatura_repo):
        self.cliente_service, self.animal_repo = cliente_service, animal_repo
        self.consulta_repo, self.fatura_repo = consulta_repo, fatura_repo
    def _consultas(self):
        return [c for animal in self.animal_repo.listar_todos() for c in self.consulta_repo.listar_por_animal(animal.id)]
    def resumo(self):
        consultas = self._consultas()
        return {"clientes": len(self.cliente_service.listar()), "animais": len(self.animal_repo.listar_todos()), "consultas": len(consultas), "canceladas": sum(c.estado == "Cancelada" for c in consultas)}
    def mensal(self, periodo):
        datetime.strptime(periodo, "%Y-%m")
        consultas = [c for c in self._consultas() if c.horario.strftime("%Y-%m") == periodo]
        por_medico = {}
        faturado = 0.0
        for c in consultas:
            por_medico[c.cedula_profissional] = por_medico.get(c.cedula_profissional, 0) + 1
            fatura = self.fatura_repo.obter_por_consulta(c.id)
            if fatura:
                faturado += fatura.valor_total
        return {"consultas": len(consultas), "faturado": faturado, "por_medico": por_medico}
