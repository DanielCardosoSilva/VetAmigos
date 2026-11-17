"""tests/test_cliente.py"""

import unittest
from unittest.mock import MagicMock

from src.models.cliente import Cliente
from src.services.cliente_service import ClienteService


class TestCliente(unittest.TestCase):

    def setUp(self):
        self.repo = MagicMock()
        self.service = ClienteService(self.repo)

    def test_criar_cliente(self):
        cliente = Cliente(
            nome="João Silva",
            nif="123456789",
            telefone="912345678",
            email="joao@email.com"
        )

        self.assertIsNone(cliente.id)
        self.assertEqual(cliente.nome, "João Silva")
        self.assertEqual(cliente.nif, "123456789")

    def test_registar_cliente(self):
        self.repo.obter_por_nif.return_value = None
        self.repo.inserir.side_effect = lambda cliente: cliente

        cliente = self.service.registar(
            "João Silva",
            "123456789",
            "912345678",
            "joao@email.com"
        )

        self.assertIsInstance(cliente, Cliente)
        self.repo.inserir.assert_called_once()

    def test_registar_cliente_nif_duplicado(self):
        self.repo.obter_por_nif.return_value = MagicMock()

        with self.assertRaises(ValueError):
            self.service.registar(
                "João Silva",
                "123456789",
                "912345678",
                "joao@email.com"
            )

        self.repo.inserir.assert_not_called()

    def test_registar_cliente_nome_vazio(self):
        with self.assertRaises(ValueError):
            self.service.registar(
                "",
                "123456789",
                "912345678",
                "joao@email.com"
            )

        self.repo.inserir.assert_not_called()

    def test_registar_cliente_telefone_curto(self):
        with self.assertRaisesRegex(ValueError, "9 dígitos"):
            self.service.registar(
                "João Silva",
                "123456789",
                "91234",
                "joao@email.com"
            )

        self.repo.inserir.assert_not_called()

    def test_registar_cliente_telefone_longo(self):
        with self.assertRaisesRegex(ValueError, "9 dígitos"):
            self.service.registar(
                "João Silva",
                "123456789",
                "9123456789",
                "joao@email.com"
            )

        self.repo.inserir.assert_not_called()

    def test_registar_cliente_telefone_com_letras(self):
        with self.assertRaises(ValueError):
            self.service.registar(
                "João Silva",
                "123456789",
                "91234ABCD",
                "joao@email.com"
            )

        self.repo.inserir.assert_not_called()

    def test_registar_cliente_email_sem_arroba(self):
        with self.assertRaisesRegex(ValueError, "@"):
            self.service.registar(
                "João Silva",
                "123456789",
                "912345678",
                "joao.email.com"
            )

        self.repo.inserir.assert_not_called()

    def test_registar_cliente_email_valido(self):
        self.repo.obter_por_nif.return_value = None
        self.repo.inserir.side_effect = lambda cliente: cliente

        cliente = self.service.registar(
            "João Silva",
            "123456789",
            "912345678",
            "joao@email.com"
        )

        self.assertEqual(cliente.telefone, "912345678")
        self.assertEqual(cliente.email, "joao@email.com")
        self.repo.inserir.assert_called_once()

    def test_listar_clientes(self):
        clientes = [
            Cliente(
                "João",
                "123456789",
                "912345678",
                "joao@email.com"
            ),
            Cliente(
                "Maria",
                "987654321",
                "923456789",
                "maria@email.com"
            )
        ]

        self.repo.listar_todos.return_value = clientes

        resultado = self.service.listar()

        self.assertEqual(resultado, clientes)
        self.repo.listar_todos.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
