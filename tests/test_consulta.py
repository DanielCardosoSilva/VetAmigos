"""tests/test_consulta.py"""

import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime

from src.repositories.consulta_repository import ConsultaRepository


class TestConsulta(unittest.TestCase):

    def setUp(self):
        self.repo = ConsultaRepository()

    @patch("src.repositories.consulta_repository.get_connection")
    def test_agendar_consulta(self, mock_get_connection):
        conn = MagicMock()
        mock_get_connection.return_value.__enter__.return_value = conn
        conn.execute.return_value.lastrowid = 1

        consulta = MagicMock()
        consulta.id_animal = 1
        consulta.cedula_profissional = "12345"
        consulta.horario = datetime(2026, 11, 10, 10, 30)
        consulta.diagnostico = ""
        consulta.tratamento = ""
        consulta.custo = 0.0
        consulta.peso_registado = None
        consulta.estado = "Agendada"

        resultado = self.repo.agendar(consulta)

        self.assertEqual(resultado.id, 1)
        conn.execute.assert_called_once()

    @patch("src.repositories.consulta_repository.get_connection")
    def test_cancelar_consulta(self, mock_get_connection):
        conn = MagicMock()
        mock_get_connection.return_value.__enter__.return_value = conn
        conn.execute.return_value.rowcount = 1

        resultado = self.repo.cancelar(1)

        self.assertTrue(resultado)
        conn.execute.assert_called_once()

    @patch("src.repositories.consulta_repository.get_connection")
    def test_cancelar_consulta_inexistente(self, mock_get_connection):
        conn = MagicMock()
        mock_get_connection.return_value.__enter__.return_value = conn
        conn.execute.return_value.rowcount = 0

        resultado = self.repo.cancelar(999)

        self.assertFalse(resultado)


if __name__ == "__main__":
    unittest.main()
