"""tests/test_medicamento_prescrito.py"""

import unittest
from unittest.mock import MagicMock

from src.models.medicamento_prescrito import MedicamentoPrescrito
from src.services.medicamento_prescrito_service import MedicamentoPrescritoService


class TestMedicamentoPrescrito(unittest.TestCase):

    def setUp(self):
        self.repo = MagicMock()
        self.receita_repo = MagicMock()
        self.medicamento_repo = MagicMock()

        self.service = MedicamentoPrescritoService(
            self.repo,
            self.receita_repo,
            self.medicamento_repo
        )

    def test_criar_medicamento_prescrito(self):
        medicamento = MedicamentoPrescrito(1, 2, 10, "De 8 em 8 horas")

        self.assertIsNone(medicamento.id)
        self.assertEqual(medicamento.id_receita, 1)
        self.assertEqual(medicamento.id_medicamento, 2)
        self.assertEqual(medicamento.quantidade, 10)

    def test_registar_medicamento_prescrito(self):
        self.receita_repo.obter_por_id.return_value = MagicMock()
        self.medicamento_repo.obter_por_id.return_value = MagicMock()
        self.repo.inserir.side_effect = lambda medicamento: medicamento

        resultado = self.service.registar(
            1, 2, 10, "De 8 em 8 horas"
        )

        self.assertIsInstance(resultado, MedicamentoPrescrito)
        self.repo.inserir.assert_called_once()

    def test_receita_inexistente(self):
        self.receita_repo.obter_por_id.return_value = None

        with self.assertRaises(ValueError):
            self.service.registar(999, 2, 10, "Diariamente")

        self.repo.inserir.assert_not_called()

    def test_medicamento_inexistente(self):
        self.receita_repo.obter_por_id.return_value = MagicMock()
        self.medicamento_repo.obter_por_id.return_value = None

        with self.assertRaises(ValueError):
            self.service.registar(1, 999, 10, "Diariamente")

        self.repo.inserir.assert_not_called()

    def test_quantidade_invalida(self):
        with self.assertRaises(ValueError):
            self.service.registar(1, 2, -5, "Diariamente")

        self.repo.inserir.assert_not_called()

    def test_posologia_vazia(self):
        with self.assertRaises(ValueError):
            self.service.registar(1, 2, 10, "")

        self.repo.inserir.assert_not_called()

    def test_listar_por_receita(self):
        self.receita_repo.obter_por_id.return_value = MagicMock()
        self.repo.listar_por_receita.return_value = []

        resultado = self.service.listar_por_receita(1)

        self.assertEqual(resultado, [])
        self.repo.listar_por_receita.assert_called_once_with(1)


if __name__ == "__main__":
    unittest.main()
