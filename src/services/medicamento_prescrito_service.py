"""src/services/medicamento_prescrito_service.py"""

from src.models.medicamento_prescrito import MedicamentoPrescrito
from src.repositories.medicamento_prescrito_repository import MedicamentoPrescritoRepository


class MedicamentoPrescritoService:
    def __init__(self, repo: MedicamentoPrescritoRepository, receita_repo, medicamento_repo):
        self._repo = repo
        self._receita_repo = receita_repo
        self._medicamento_repo = medicamento_repo

    def registar(self, id_receita: int, id_medicamento: int, quantidade: int, posologia: str) -> MedicamentoPrescrito:
        """Valida e associa um medicamento a uma receita."""

        # Validação 1: Existência da receita
        if self._receita_repo.obter_por_id(id_receita) is None:
            raise ValueError("Receita não encontrada.")

        # Validação 2: Existência do medicamento
        if self._medicamento_repo.obter_por_id(id_medicamento) is None:
            raise ValueError("Medicamento não encontrado.")

        # Validação 3: Quantidade
        if not isinstance(quantidade, int) or isinstance(quantidade, bool) or quantidade <= 0:
            raise ValueError("A quantidade deve ser um número inteiro superior a zero.")

        # Validação 4: Posologia
        if not posologia or not posologia.strip():
            raise ValueError("A posologia é obrigatória.")

        # Criação do objeto e persistência
        medicamento_prescrito = MedicamentoPrescrito(
            id_receita=id_receita,
            id_medicamento=id_medicamento,
            quantidade=quantidade,
            posologia=posologia.strip()
        )

        return self._repo.inserir(medicamento_prescrito)

    def listar_por_receita(self, id_receita: int) -> list[MedicamentoPrescrito]:
        """Obtém os medicamentos associados a uma receita."""

        if self._receita_repo.obter_por_id(id_receita) is None:
            raise ValueError("Receita não encontrada.")

        return self._repo.listar_por_receita(id_receita)
