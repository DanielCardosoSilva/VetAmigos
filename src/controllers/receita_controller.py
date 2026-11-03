"""Controlador de receita."""
class ReceitaController:
    def __init__(self, service, repo, prescrito_service):
        self.service, self.repo, self.prescrito_service = service, repo, prescrito_service
    def emitir(self, consulta):
        return self.service.emitir_receita(consulta)
    def adicionar(self, receita, medicamento, quantidade, posologia):
        return self.prescrito_service.registar(receita, medicamento, quantidade, posologia)
    def listar_por_consulta(self, consulta):
        return self.repo.listar_por_consulta(consulta)
    def medicamentos(self, receita):
        return self.prescrito_service.listar_por_receita(receita)
