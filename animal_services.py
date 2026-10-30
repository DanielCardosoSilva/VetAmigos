from datetime import date
from animal import Animal


class AnimalService:
    def __init__(self, repo):
        self._repo = repo

    def registar(self, nome, especie, data_nasc, peso_animal, nif_cliente, id=None):
        if nome.strip() == "":
            raise ValueError("O nome não pode estar vazio.")

        if data_nasc > date.today():
            raise ValueError("A data não pode ser futura.")

        animal = Animal(
            nome=nome,
            especie=especie,
            data_nasc=data_nasc,
            peso_animal=peso_animal,
            nif_cliente=nif_cliente,
        )

        return self._repo.inserir(animal)