# tests/test_cliente_service.py
import unittest
from unittest.mock import MagicMock
from src.services.cliente_service import ClienteService
from src.models.cliente import Cliente

class TestClienteService(unittest.TestCase):

    def setUp(self):
        # Substitui o repositório real por um mock para isolar os testes
        self.mock_repo = MagicMock()
        self.svc = ClienteService(self.mock_repo)

    def test_nome_vazio_levanta_erro(self):
        """Testa se tentar registar um cliente com nome vazio gera erro."""
        with self.assertRaises(ValueError) as ctx:
            self.svc.registar("   ", "123456789", "910000000", "cliente@email.com")
        self.assertIn("nome do cliente não pode estar vazio", str(ctx.exception))

    def test_nif_invalido_levanta_erro(self):
        """Testa se um NIF com letras ou tamanho incorreto levanta erro (RNF13)."""
        with self.assertRaises(ValueError) as ctx:
            self.svc.registar("Maria Silva", "12345", "910000000", "maria@email.com")
        self.assertIn("NIF inválido", str(ctx.exception))

    def test_nif_duplicado_levanta_erro(self):
        """Testa se registar um NIF que já existe na base de dados levanta erro."""
        # Simula que o repositório encontrou um cliente existente com o mesmo NIF
        self.mock_repo.obter_por_nif.return_value = Cliente("Existente", "123456789", "999", "e@email.com" id=1)

        with self.assertRaises(ValueError) as ctx:
            self.svc.registar("Novo Cliente", "123456789", "910000000", "novo@email.com")
        self.assertIn("Já existe um cliente registado com este NIF", str(ctx.exception))

    def test_registar_cliente_valido_chama_repo(self):
        """Testa o registo com dados válidos e confirma chamada ao repositório."""
        self.mock_repo.obter_por_nif.return_value = None  # NIF não existe previamente

        cliente_registado = self.svc.registar("Paulo Carvalho", "123456789", "912345678", "paulo@vetamigos.pt")

        self.mock_repo.inserir.assert_called_once()
        self.assertEqual(cliente_registado.nome, "Paulo Carvalho")
        self.assertEqual(cliente_registado.nif, "123456789")

    def test_listar_chama_repo(self):
        """Testa se o método listar invoca o método correto do repositório."""
        self.svc.listar()
        self.mock_repo.listar_todos.assert_called_once()

if __name__ == "__main__":
    unittest.main()

# Para executar o teste no terminal utilizar o comando:python -m unittest discover -v tests/