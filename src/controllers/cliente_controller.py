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
    def atualizar(self, nif, nome, telefone, email):
        return self.service.atualizar(nif, nome, telefone, email)
    def definir_ativo(self, nif, ativo):
        return self.service.definir_ativo(nif, ativo)
