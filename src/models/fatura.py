# src/models/fatura.py
from datetime import date

class Fatura:
    """
    Representa a Fatura de uma consulta com valor total, estado e pagamento (US-10 / RF11).
    """
    def __init__(self, id_consulta: int, valor_total: float, estado: str = "Pendente", 
                 metodo_pagamento: str = None, data_pagamento: date = None, id: int = None):
        self.id = id
        self.id_consulta = id_consulta
        self.valor_total = valor_total
        self.estado = estado  # "Pendente" ou "Pago"
        self.metodo_pagamento = metodo_pagamento
        self.data_pagamento = data_pagamento

    def __str__(self) -> str:
        return f"Fatura(id: {self.id} — Total: {self.valor_total}€ — Estado: {self.estado})"