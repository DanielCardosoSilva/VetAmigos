"""Controlador de fatura."""
class FaturaController:
    def __init__(self, service, repo):
        self.service, self.repo = service, repo
    def emitir(self, consulta, valor, metodo):
        return self.service.gerar_fatura(consulta, valor, metodo)
    def consultar(self, consulta):
        return self.repo.obter_por_consulta(consulta)
