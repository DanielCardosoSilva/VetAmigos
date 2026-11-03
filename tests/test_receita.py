"""tests/test_receita.py"""

import unittest
from unittest.mock import MagicMock
from datetime import date

from src.models.receita import Receita
from src.services.receita_service import ReceitaService


class TestReceita(unittest.TestCase):

    def setUp(self):
        self.repo = MagicMock()
        self.consulta_repo = MagicMock()
        self.service = ReceitaService(self.repo, self.consulta_repo)

    def test_criar_receita(self):
        receita = Receita(1, date(2026, 11, 3))

        self.assertIsNone(receita.id)
        self.assertEqual(receita.id_consulta, 1)
        self.assertEqual(receita.data_emissao, date(2026, 11, 3))

    def test_emitir_receita(self):
        self.consulta_repo.obter_por_id.return_value = MagicMock()
        self.repo.inserir.side_effect = lambda receita: receita

        resultado = self.service.emitir_receita(1)

        self.assertIsInstance(resultado, Receita)
        self.assertEqual(resultado.data_emissao, date.today())
        self.repo.inserir.assert_called_once()

    def test_consulta_inexistente(self):
        self.consulta_repo.obter_por_id.return_value = None

        with self.assertRaises(ValueError):
            self.service.emitir_receita(999)

        self.repo.inserir.assert_not_called()

    def test_id_consulta_invalido(self):
        with self.assertRaises(ValueError):
            self.service.emitir_receita(None)

        self.repo.inserir.assert_not_called()


if __name__ == "__main__":
    unittest.main()
