"""Controlador de fatura."""

class FaturaController:
    def __init__(self, service, repo):
        # Guardar o serviço e o repositório de faturação.
        self.service, self.repo = service, repo

    def emitir(self, consulta, valor, metodo):
        # Emitir uma fatura através do serviço.
        return self.service.gerar_fatura(consulta, valor, metodo)

    def consultar(self, consulta):
        # Consultar a fatura associada a uma consulta.
        return self.repo.obter_por_consulta(consulta)

    def listar(self):
        # Listar todas as faturas registadas.
        return self.service.listar()

    def atualizar_estado(self, identificador, estado, metodo_pagamento=None):
        # Atualizar o estado da fatura através do serviço.
        return self.service.atualizar_estado(
            identificador, estado, metodo_pagamento
        )
