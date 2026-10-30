"""src/services/medicamento_service.py"""

from src.models.medicamento import Medicamento
from src.repositories.medicamento_repository import MedicamentoRepository


class MedicamentoService:
    def __init__(self, repo: MedicamentoRepository):
        self._repo = repo

    def registar(self, nome: str, tipo: str, dose: str, quantidade: int) -> Medicamento:
        """Valida e regista um novo medicamento."""

        if not nome or not nome.strip():
            raise ValueError("O nome do medicamento é obrigatório.")

        if not tipo or not tipo.strip():
            raise ValueError("O tipo de medicamento é obrigatório.")

        if not dose or not dose.strip():
            raise ValueError("A dose do medicamento é obrigatória.")

        if not isinstance(quantidade, int) or isinstance(quantidade, bool) or quantidade < 0:
            raise ValueError("A quantidade deve ser um número inteiro igual ou superior a zero.")

        medicamento = Medicamento(
            nome=nome.strip(),
            tipo=tipo.strip(),
            dose=dose.strip(),
            quantidade=quantidade
        )

        return self._repo.inserir(medicamento)

    def listar(self) -> list[Medicamento]:
        """Obtém todos os medicamentos registados."""
        return self._repo.listar_todos()

    def atualizar_quantidade(self, id_medicamento: int, quantidade: int):
        """Valida e atualiza a quantidade de um medicamento."""

        if self._repo.obter_por_id(id_medicamento) is None:
            raise ValueError("Medicamento não encontrado.")

        if not isinstance(quantidade, int) or isinstance(quantidade, bool) or quantidade < 0:
            raise ValueError("A quantidade deve ser um número inteiro igual ou superior a zero.")

        self._repo.atualizar_quantidade(id_medicamento, quantidade)
