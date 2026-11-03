"""tests/test_medicamento.py"""

import unittest
from unittest.mock import MagicMock

from src.models.medicamento import Medicamento
from src.services.medicamento_service import MedicamentoService


class TestMedicamento(unittest.TestCase):

    def setUp(self):
        self.repo = MagicMock()
        self.service = MedicamentoService(self.repo)

    def test_criar_medicamento(self):
        medicamento = Medicamento("Amoxicilina", "Antibiótico", "250mg", 20)

        self.assertIsNone(medicamento.id)
        self.assertEqual(medicamento.nome, "Amoxicilina")
        self.assertEqual(medicamento.quantidade, 20)

    def test_registar_medicamento(self):
        self.repo.inserir.side_effect = lambda medicamento: medicamento

        resultado = self.service.registar(
            "Amoxicilina", "Antibiótico", "250mg", 20
        )

        self.assertIsInstance(resultado, Medicamento)
        self.repo.inserir.assert_called_once()

    def test_nome_vazio(self):
        with self.assertRaises(ValueError):
            self.service.registar("", "Antibiótico", "250mg", 20)

        self.repo.inserir.assert_not_called()

    def test_quantidade_negativa(self):
        with self.assertRaises(ValueError):
            self.service.registar(
                "Amoxicilina", "Antibiótico", "250mg", -10
            )

        self.repo.inserir.assert_not_called()

    def test_quantidade_nao_inteira(self):
        with self.assertRaises(ValueError):
            self.service.registar(
                "Amoxicilina", "Antibiótico", "250mg", 2.5
            )

        self.repo.inserir.assert_not_called()

    def test_atualizar_quantidade(self):
        self.repo.obter_por_id.return_value = MagicMock()

        self.service.atualizar_quantidade(1, 30)

        self.repo.atualizar_quantidade.assert_called_once_with(1, 30)

    def test_atualizar_medicamento_inexistente(self):
        self.repo.obter_por_id.return_value = None

        with self.assertRaises(ValueError):
            self.service.atualizar_quantidade(999, 30)

        self.repo.atualizar_quantidade.assert_not_called()

    def test_atualizar_quantidade_negativa(self):
        self.repo.obter_por_id.return_value = MagicMock()

        with self.assertRaises(ValueError):
            self.service.atualizar_quantidade(1, -5)

        self.repo.atualizar_quantidade.assert_not_called()

    def test_listar_medicamentos(self):
        self.repo.listar_todos.return_value = []

        resultado = self.service.listar()

        self.assertEqual(resultado, [])
        self.repo.listar_todos.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
