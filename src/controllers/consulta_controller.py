"""Controlador de consulta."""
from src.models.medico_veterinario import MedicoVeterinario

class ConsultaController:
    def __init__(self, service, repo, funcionario_repo):
        self.service, self.repo, self.funcionario_repo = service, repo, funcionario_repo
    def medicos(self):
        return [f for f in self.funcionario_repo.listar_todos() if isinstance(f, MedicoVeterinario)]
    def agendar(self, id_animal, cedula, horario, motivo=""):
        if cedula not in {m.cedula_profissional for m in self.medicos()}:
            raise ValueError("Cédula não corresponde a um médico registado.")
        return self.service.agendar(id_animal, cedula, horario, motivo)
    def concluir(self, identificador, medico, diagnostico, tratamento, sumario, custo, peso):
        return self.service.concluir(identificador, medico, diagnostico, tratamento, sumario, custo, peso)
    def historico(self, id_animal):
        return self.service.listar_por_animal(id_animal)
    def consultar(self, identificador):
        return self.repo.obter_por_id(identificador)
    def cancelar(self, identificador):
        return self.service.cancelar(identificador)
