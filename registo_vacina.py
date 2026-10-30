#o nome, tipo, dose, quantidade
class Vacina: 
    def __init__(self, id_vacina, nome, tipo, dose, quantidade): 
        self.id         = id_vacina
        self.nome       = nome
        self.tipo       = tipo
        self.dose       = dose
        self.quantidade = quantidade

    def __str__(self): 
        return (f'Vacina({self.id}: {self.nome}, [{self.tipo}], {self.dose}, {self.quantidade})') 