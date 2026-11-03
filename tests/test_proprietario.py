"""tests/test_proprietario.py"""

import unittest

from src.models.funcionario import Funcionario
from src.models.proprietario import Proprietario


class TestProprietario(unittest.TestCase):

    def test_criar_proprietario(self):
        proprietario = Proprietario(
            "Carlos Silva",
            "carlos",
            "hash_exemplo"
        )

        self.assertIsNone(proprietario.id)
        self.assertEqual(proprietario.nome, "Carlos Silva")
        self.assertEqual(proprietario.nome_utilizador, "carlos")

    def test_heranca_funcionario(self):
        proprietario = Proprietario(
            "Carlos Silva",
            "carlos",
            "hash_exemplo"
        )

        self.assertIsInstance(proprietario, Funcionario)


if __name__ == "__main__":
    unittest.main()
