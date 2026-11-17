"""Controlador de animal."""
class AnimalController:
    def __init__(self, service, repo):
        self.service, self.repo = service, repo
    def registar(self, nome, especie, nascimento, peso, nif):
        return self.service.registar(nome, especie, nascimento, peso, nif)
    def listar(self):
        return self.repo.listar_todos()
    def consultar(self, identificador):
        return self.repo.obter_por_id(identificador)
    def atualizar(self, id_animal, nome, especie, nascimento, peso, nif):
        return self.service.atualizar(id_animal, nome, especie, nascimento, peso, nif)
    def definir_ativo(self, id_animal, ativo):
        return self.service.definir_ativo(id_animal, ativo)
