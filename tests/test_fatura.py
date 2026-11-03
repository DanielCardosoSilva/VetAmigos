"""tests/test_fatura.py"""

import unittest
from unittest.mock import MagicMock

from src.models.fatura import Fatura
from src.services.fatura_service import FaturaService


class TestFatura(unittest.TestCase):

    def setUp(self):
        self.repo = MagicMock()
        self.consulta_repo = MagicMock()
        self.service = FaturaService(self.repo, self.consulta_repo)

    def test_criar_fatura(self):
        fatura = Fatura(id_consulta=1, valor_total=50.0)

        self.assertIsNone(fatura.id)
        self.assertEqual(fatura.id_consulta, 1)
        self.assertEqual(fatura.valor_total, 50.0)
        self.assertEqual(fatura.estado, "Pendente")
        self.assertIsNone(fatura.data_pagamento)

    def test_gerar_fatura(self):
        self.consulta_repo.obter_por_id.return_value = MagicMock()
        self.repo.obter_por_consulta.return_value = None
        self.repo.inserir.side_effect = lambda fatura: fatura

        fatura = self.service.gerar_fatura(1, 50.0)

        self.assertIsInstance(fatura, Fatura)
        self.assertEqual(fatura.estado, "Pendente")
        self.repo.inserir.assert_called_once()

    def test_gerar_fatura_paga(self):
        self.consulta_repo.obter_por_id.return_value = MagicMock()
        self.repo.obter_por_consulta.return_value = None
        self.repo.inserir.side_effect = lambda fatura: fatura

        fatura = self.service.gerar_fatura(1, 50.0, "Multibanco")

        self.assertEqual(fatura.estado, "Pago")
        self.assertEqual(fatura.metodo_pagamento, "Multibanco")
        self.assertIsNotNone(fatura.data_pagamento)

    def test_consulta_inexistente(self):
        self.consulta_repo.obter_por_id.return_value = None

        with self.assertRaises(ValueError):
            self.service.gerar_fatura(999, 50.0)

        self.repo.inserir.assert_not_called()

    def test_valor_invalido(self):
        with self.assertRaises(ValueError):
            self.service.gerar_fatura(1, -10.0)

        self.repo.inserir.assert_not_called()

    def test_fatura_duplicada(self):
        self.consulta_repo.obter_por_id.return_value = MagicMock()
        self.repo.obter_por_consulta.return_value = MagicMock()

        with self.assertRaises(ValueError):
            self.service.gerar_fatura(1, 50.0)

        self.repo.inserir.assert_not_called()


if __name__ == "__main__":
    unittest.main()
