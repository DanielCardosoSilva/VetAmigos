"""Controlador de medicamento."""
class MedicamentoController:
    def __init__(self, service):
        self.service = service
    def registar(self, nome, tipo, dose, quantidade):
        return self.service.registar(nome, tipo, dose, quantidade)
    def listar(self):
        return self.service.listar()
    def atualizar(self, identificador, quantidade):
        return self.service.atualizar_quantidade(identificador, quantidade)
