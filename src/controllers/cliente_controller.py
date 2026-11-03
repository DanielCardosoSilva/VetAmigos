"""Controlador de cliente."""
class ClienteController:
    def __init__(self, service, repo):
        self.service, self.repo = service, repo
    def registar(self, nome, nif, telefone, email):
        return self.service.registar(nome, nif, telefone, email)
    def listar(self):
        return self.service.listar()
    def consultar(self, nif):
        return self.repo.obter_por_nif(nif)
