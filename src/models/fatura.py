"""src/models/fatura.py"""

from datetime import date


class Fatura:
    """
    Representa a fatura de uma consulta, com valor total,
    estado e informação de pagamento (US-10 / RF11).
    """

    def __init__(
        self,
        id_consulta: int,
        valor_total: float,
        estado: str = "Pendente",
        metodo_pagamento: str = None,
        data_pagamento: date = None
    ):
        self.id = None
        self.id_consulta = id_consulta
        self.valor_total = valor_total
        self.estado = estado
        self.metodo_pagamento = metodo_pagamento
        self.data_pagamento = data_pagamento

    def __str__(self) -> str:
        return (
            f"Fatura({self.id}: "
            f"Consulta: {self.id_consulta}, "
            f"Total: {self.valor_total}€, "
            f"Estado: {self.estado})"
        )
    