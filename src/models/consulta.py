"""src/models/consulta.py"""

from datetime import datetime


class Consulta:
    def __init__(
        self,
        id_animal,
        cedula_profissional,
        horario,
        diagnostico="",
        tratamento="",
        custo=0.0,
        peso_registado=None,
        estado="Agendada"
    ):
        self.id = None
        self.id_animal = id_animal
        self.cedula_profissional = cedula_profissional
        self.horario = horario
        self.diagnostico = diagnostico
        self.tratamento = tratamento
        self.custo = custo
        self.peso_registado = peso_registado
        self.estado = estado

    def __str__(self):
        return (
            f"Consulta({self.id}: "
            f"{self.horario.strftime('%Y-%m-%d %H:%M')} - "
            f"Animal {self.id_animal} [{self.estado}])"
        )

    @property
    def data(self):
        return self.horario.date()

    @property
    def hora(self):
        return self.horario.time()
