"""src/services/animal_service.py"""

from datetime import date
from src.models.animal import Animal
from src.repositories.cliente_repository import ClienteRepository

class AnimalService:
    def __init__(self, repo, cliente_repo: ClienteRepository):
        self._repo = repo
        self._cliente_repo = cliente_repo

    def registar(self, nome, especie, data_nasc, peso_animal, nif_cliente):
        """Aplica as regras de negócio e validações para registar um animal."""

        # Validação 1: Campos obrigatórios
        if not nome or not nome.strip():
            raise ValueError("O nome não pode estar vazio.")

        if not especie or not especie.strip():
            raise ValueError("A espécie é obrigatória.")

        # Validação 2: Data de nascimento
        if not isinstance(data_nasc, date):
            raise ValueError("A data de nascimento é inválida.")

        if data_nasc > date.today():
            raise ValueError("A data de nascimento não pode ser futura.")

        # Validação 3: Peso
        if peso_animal <= 0:
            raise ValueError("O peso deve ser superior a zero.")

        # Validação 4: Cliente associado
        if not nif_cliente or self._cliente_repo.obter_por_nif(nif_cliente) is None:
            raise ValueError("Não existe um cliente registado com esse NIF.")

        if not self._cliente_repo.obter_por_nif(nif_cliente).ativo:
            raise ValueError("O cliente está arquivado.")

        # Criação do objeto e persistência
        animal = Animal(
            nome=nome.strip(),
            especie=especie.strip(),
            data_nasc=data_nasc,
            peso_animal=peso_animal,
            nif_cliente=nif_cliente
        )

        return self._repo.inserir(animal)

    def atualizar(self, id_animal, nome, especie, data_nasc, peso_animal, nif_cliente):
        """Valida os dados editáveis e atualiza um animal existente."""
        animal = self._repo.obter_por_id(id_animal)
        if animal is None:
            raise ValueError("O animal não existe.")
        if not nome or not nome.strip():
            raise ValueError("O nome não pode estar vazio.")
        if not especie or not especie.strip():
            raise ValueError("A espécie é obrigatória.")
        if not isinstance(data_nasc, date) or data_nasc > date.today():
            raise ValueError("A data de nascimento é inválida.")
        if peso_animal <= 0:
            raise ValueError("O peso deve ser superior a zero.")
        cliente = self._cliente_repo.obter_por_nif(nif_cliente)
        if cliente is None or not cliente.ativo:
            raise ValueError("O proprietário não existe ou está arquivado.")
        animal.nome = nome.strip()
        animal.especie = especie.strip()
        animal.data_nasc = data_nasc
        animal.peso_animal = peso_animal
        animal.nif_cliente = nif_cliente
        self._repo.atualizar(animal)
        return animal

    def definir_ativo(self, id_animal, ativo):
        """Arquiva ou reativa o animal sem eliminar o histórico clínico."""
        animal = self._repo.obter_por_id(id_animal)
        if animal is None:
            raise ValueError("O animal não existe.")
        if not ativo and self._repo.tem_consultas_futuras(id_animal):
            raise ValueError("Existem consultas futuras agendadas para este animal.")
        if ativo:
            cliente = self._cliente_repo.obter_por_nif(animal.nif_cliente)
            if cliente is None or not cliente.ativo:
                raise ValueError("Reativa primeiro o proprietário do animal.")
        self._repo.definir_ativo(id_animal, ativo)
        animal.ativo = ativo
        return animal
