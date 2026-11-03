"""tests/test_recepcionista.py"""

import unittest

from src.models.funcionario import Funcionario
from src.models.recepcionista import Rececionista


class TestRececionista(unittest.TestCase):

    def test_criar_recepcionista(self):
        rececionista = Rececionista(
            "Ana Silva",
            "ana",
            "hash_exemplo"
        )

        self.assertIsNone(rececionista.id)
        self.assertEqual(rececionista.nome, "Ana Silva")
        self.assertEqual(rececionista.nome_utilizador, "ana")

    def test_heranca_funcionario(self):
        rececionista = Rececionista(
            "Ana Silva",
            "ana",
            "hash_exemplo"
        )

        self.assertIsInstance(rececionista, Funcionario)


if __name__ == "__main__":
    unittest.main()
