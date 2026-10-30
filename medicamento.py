class Medicamento: 
    def __init__(self, id_medicamento, nome, tipo, dose, quantidade): 
        self.id         = id_medicamento
        self.nome       = nome
        self.tipo       = tipo
        self.dose       = dose
        self.quantidade = quantidade

    def __str__(self): 
        return (f'Medicamento({self.id}: {self.nome}, [{self.tipo}], {self.dose}, {self.quantidade})')