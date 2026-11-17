"""src/services/fatura_service.py"""

from datetime import date
from src.models.fatura import Fatura
from src.repositories.fatura_repository import FaturaRepository
from src.repositories.consulta_repository import ConsultaRepository


class FaturaService:
    def __init__(self, repo: FaturaRepository, consulta_repo: ConsultaRepository):
        # Guardar os repositórios necessários à faturação.
        self._repo = repo
        self._consulta_repo = consulta_repo

    def gerar_fatura(self, id_consulta: int, valor_total: float, metodo_pagamento: str = None) -> Fatura:
        # Validar a consulta e emitir uma fatura sem duplicações.
        if not id_consulta:
            raise ValueError("A fatura deve estar obrigatoriamente associada a uma consulta.")

        if not self._consulta_repo.obter_por_id(id_consulta):
            raise ValueError("A consulta indicada não existe.")
        if not isinstance(valor_total, (int, float)) or isinstance(valor_total, bool) or valor_total <= 0:
            raise ValueError("O valor total da fatura deve ser superior a zero.")

        if self._repo.obter_por_consulta(id_consulta) is not None:
            raise ValueError("Já existe uma fatura emitida para esta consulta.")

        estado = "Pago" if metodo_pagamento else "Pendente"
        data_pag = date.today() if metodo_pagamento else None
        fatura = Fatura(
            id_consulta=id_consulta,
            valor_total=valor_total,
            estado=estado,
            metodo_pagamento=metodo_pagamento,
            data_pagamento=data_pag
        )

        return self._repo.inserir(fatura)

    def listar(self):
        # Devolver todas as faturas existentes.
        return self._repo.listar_todas()

    def atualizar_estado(self, identificador, estado, metodo_pagamento=None):
        # Validar e atualizar o estado de uma fatura existente.
        fatura = self._repo.obter_por_id(identificador)

        if fatura is None:
            raise ValueError("A fatura indicada não existe.")

        if estado not in ("Pendente", "Pago", "Anulada"):
            raise ValueError("O estado da fatura é inválido.")

        if fatura.estado == "Anulada" and estado != "Anulada":
            raise ValueError("Uma fatura anulada não pode ser reativada.")

        if estado == "Pago":
            metodo_pagamento = (metodo_pagamento or "").strip()

            if not metodo_pagamento:
                raise ValueError(
                    "É obrigatório indicar o método de pagamento."
                )

            if fatura.estado == "Pago" and fatura.metodo_pagamento == metodo_pagamento:
                return fatura

            data_pagamento = (
                fatura.data_pagamento
                if fatura.estado == "Pago" and fatura.data_pagamento
                else date.today()
            )
        else:
            metodo_pagamento = None
            data_pagamento = None

        atualizado = self._repo.atualizar_estado(
            identificador,
            estado,
            metodo_pagamento,
            data_pagamento
        )

        if not atualizado:
            raise ValueError("Não foi possível atualizar a fatura.")

        return self._repo.obter_por_id(identificador)
