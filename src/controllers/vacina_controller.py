"""Controlador de vacina."""
from datetime import date

class VacinaController:
    def __init__(self, service):
        self.service = service
    def registar(self, animal, nome, administracao, proxima):
        return self.service.registar(animal, nome, administracao, proxima)
    def historico(self, animal):
        return self.service.listar_por_animal(animal)
    def atrasadas(self):
        return [v for v in self.service.listar_todos() if v.data_proxima_dose and v.data_proxima_dose < date.today()]
