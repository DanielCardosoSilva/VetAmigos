"""src/services/receita_service.py"""

from datetime import date
from src.models.receita import Receita
from src.repositories.receita_repository import ReceitaRepository
from src.repositories.consulta_repository import ConsultaRepository

class ReceitaService:
    def __init__(self, repo: ReceitaRepository, consulta_repo: ConsultaRepository):
        self._repo = repo
        self._consulta_repo = consulta_repo

    def emitir_receita(self, id_consulta: int) -> Receita:
        if not id_consulta:
            raise ValueError("A receita deve estar associada a uma consulta válida.")

        if not self._consulta_repo.obter_por_id(id_consulta):
            raise ValueError("A consulta indicada não existe.")

        receita = Receita(id_consulta=id_consulta, data_emissao=date.today())
        return self._repo.inserir(receita)