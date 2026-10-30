# src/services/fatura_service.py
from datetime import date
from src.models.fatura import Fatura
from src.repositories.fatura_repository import FaturaRepository

class FaturaService:
    def __init__(self, repo: FaturaRepository):
        self._repo = repo

    def gerar_fatura(self, id_consulta: int, valor_total: float, metodo_pagamento: str = None) -> Fatura:
        if not id_consulta:
            raise ValueError("A fatura deve estar obrigatoriamente associada a uma consulta.")
        if valor_total <= 0:
            raise ValueError("O valor total da fatura deve ser superior a zero.")

        # Verifica se já existe fatura para esta consulta (regra de fatura única)
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