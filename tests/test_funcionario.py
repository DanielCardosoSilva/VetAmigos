"""tests/test_funcionario.py"""

import unittest
from unittest.mock import MagicMock

from src.models.funcionario import Funcionario
from src.models.recepcionista import Rececionista
from src.services.funcionario_service import FuncionarioService


class TestFuncionario(unittest.TestCase):

    def setUp(self):
        self.repo = MagicMock()
        self.service = FuncionarioService(self.repo)

    def test_criar_funcionario(self):
        funcionario = Funcionario(
            "João Silva",
            "joao",
            "hash_exemplo"
        )

        self.assertIsNone(funcionario.id)
        self.assertEqual(funcionario.nome, "João Silva")
        self.assertEqual(funcionario.nome_utilizador, "joao")

    def test_registar_funcionario(self):
        self.repo.obter_por_nome_utilizador.return_value = None
        self.repo.inserir.side_effect = lambda funcionario: funcionario

        funcionario = Rececionista("Ana", "ana", "")

        resultado = self.service.registar(funcionario, "senha123")

        self.assertIsInstance(resultado, Rececionista)
        self.assertNotEqual(resultado.palavra_passe_hash, "senha123")
        self.repo.inserir.assert_called_once()

    def test_utilizador_duplicado(self):
        self.repo.obter_por_nome_utilizador.return_value = MagicMock()

        funcionario = Rececionista("Ana", "ana", "")

        with self.assertRaises(ValueError):
            self.service.registar(funcionario, "senha123")

        self.repo.inserir.assert_not_called()

    def test_nome_vazio(self):
        funcionario = Rececionista("", "ana", "")

        with self.assertRaises(ValueError):
            self.service.registar(funcionario, "senha123")

        self.repo.inserir.assert_not_called()

    
    def test_iniciar_sessao(self):
        self.repo.obter_por_nome_utilizador.return_value = None

        with self.assertRaises(ValueError):
            self.service.iniciar_sessao("inexistente", "senha123")

        self.repo.obter_por_nome_utilizador.assert_called_once_with("inexistente")
        self.repo.inserir.assert_not_called()



if __name__ == "__main__":
    unittest.main()
