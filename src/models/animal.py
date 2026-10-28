from datetime import date 

#o nome, espécie, raça, data de nascimento e peso do animal e seleciono esse dono de animal
class Animal: 
    def __init__(self, nome, especie, data_nasc, peso_animal, nif_cliente, id=None): 
        self.id         = id
        self.nome       = nome
        self.especie    = especie
        self.data_nasc  = data_nasc
        self.peso_animal= peso_animal
        self.nif_cliente= nif_cliente

    def __str__(self): 
            return (f'Animal({self.id}: {self.nome}, [{self.especie}], {self.data_nasc}, {self.peso_animal}, {self.nif_cliente})') 

    @property 
    def idade_anos(self): 
        delta = date.today() - self.data_nasc
        return delta.days // 365 