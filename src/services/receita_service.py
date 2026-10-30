# src/services/receita_service.py
from datetime import date
from src.models.receita import Receita
from src.repositories.receita_repository import ReceitaRepository

class ReceitaService:
    def __init__(self, repo: ReceitaRepository):
        self._repo = repo

    def emitir_receita(self, id_consulta: int) -> Receita:
        if not id_consulta:
            raise ValueError("A receita deve estar associada a uma consulta válida.")
        
        receita = Receita(id_consulta=id_consulta, data_emissao=date.today())
        return self._repo.inserir(receita)