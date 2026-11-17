"""tests/test_consulta.py"""

import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta

from src.models.consulta import Consulta
from src.models.medico_veterinario import MedicoVeterinario
from src.repositories.consulta_repository import ConsultaRepository
from src.services.consulta_service import ConsultaService


class TestConsultaRepository(unittest.TestCase):

    def setUp(self):
        self.repo = ConsultaRepository()

    @patch("src.repositories.consulta_repository.get_connection")
    def test_agendar_consulta(self, mock_get_connection):
        conn = MagicMock()
        mock_get_connection.return_value.__enter__.return_value = conn
        conn.execute.return_value.lastrowid = 1

        consulta = Consulta(
            id_animal=1,
            cedula_profissional="12345",
            horario=datetime(2026, 11, 10, 10, 30),
            motivo="Falta de apetite"
        )

        resultado = self.repo.agendar(consulta)

        self.assertEqual(resultado.id, 1)
        self.assertEqual(resultado.motivo, "Falta de apetite")
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

    @patch("src.repositories.consulta_repository.get_connection")
    def test_concluir_consulta_atualiza_peso(self, mock_get_connection):
        conn = MagicMock()
        mock_get_connection.return_value.__enter__.return_value = conn
        conn.execute.return_value.rowcount = 1

        resultado = self.repo.concluir(
            id_consulta=1,
            cedula_profissional="MV1",
            diagnostico="Virose",
            tratamento="Repouso",
            sumario="Reavaliar em 48 horas",
            custo=25.0,
            peso_registado=12.5,
            data_conclusao=datetime(2026, 11, 10, 11, 0)
        )

        self.assertTrue(resultado)
        self.assertEqual(conn.execute.call_count, 2)

        primeira_chamada = conn.execute.call_args_list[0]
        segunda_chamada = conn.execute.call_args_list[1]

        self.assertIn("UPDATE consultas", primeira_chamada.args[0])
        self.assertIn("UPDATE animais", segunda_chamada.args[0])
        self.assertEqual(segunda_chamada.args[1], (12.5, 1))

    @patch("src.repositories.consulta_repository.get_connection")
    def test_concluir_consulta_falha_nao_atualiza_peso(
        self, mock_get_connection
    ):
        conn = MagicMock()
        mock_get_connection.return_value.__enter__.return_value = conn
        conn.execute.return_value.rowcount = 0

        resultado = self.repo.concluir(
            1,
            "MV1",
            "Virose",
            "Repouso",
            "Reavaliar",
            25.0,
            12.5,
            datetime(2026, 11, 10, 11, 0)
        )

        self.assertFalse(resultado)
        conn.execute.assert_called_once()


class TestConsultaService(unittest.TestCase):

    def setUp(self):
        self.repo = MagicMock()
        self.animal_repo = MagicMock()
        self.service = ConsultaService(
            self.repo,
            self.animal_repo
        )

        self.animal_repo.obter_por_id.return_value = MagicMock()

        self.medico = MedicoVeterinario(
            "Dr. João",
            "joao",
            "hash",
            "MV1"
        )
        self.medico.ativo = True

        self.consulta = Consulta(
            id_animal=1,
            cedula_profissional="MV1",
            horario=datetime.now() + timedelta(days=1),
            motivo="Falta de apetite"
        )
        self.consulta.id = 1

    def test_agendar_consulta_com_motivo(self):
        self.repo.listar_por_animal.return_value = []
        self.repo.agendar.side_effect = lambda consulta: consulta

        resultado = self.service.agendar(
            1,
            "MV1",
            datetime.now() + timedelta(days=1),
            " Falta de apetite "
        )

        self.assertEqual(resultado.motivo, "Falta de apetite")
        self.repo.agendar.assert_called_once()

    def test_agendar_consulta_sem_motivo(self):
        with self.assertRaisesRegex(ValueError, "motivo"):
            self.service.agendar(
                1,
                "MV1",
                datetime.now() + timedelta(days=1),
                ""
            )

        self.repo.agendar.assert_not_called()

    def test_agendar_consulta_motivo_apenas_espacos(self):
        with self.assertRaisesRegex(ValueError, "motivo"):
            self.service.agendar(
                1,
                "MV1",
                datetime.now() + timedelta(days=1),
                "   "
            )

        self.repo.agendar.assert_not_called()

    def test_concluir_consulta(self):
        self.repo.obter_por_id.return_value = self.consulta
        self.repo.concluir.return_value = True

        resultado = self.service.concluir(
            1,
            self.medico,
            "Virose",
            "Repouso",
            "Reavaliar em 48 horas",
            25.0,
            12.5
        )

        self.assertEqual(resultado.motivo, "Falta de apetite")
        self.repo.concluir.assert_called_once()

        argumentos = self.repo.concluir.call_args.args

        self.assertEqual(argumentos[0], 1)
        self.assertEqual(argumentos[1], "MV1")
        self.assertEqual(argumentos[2], "Virose")
        self.assertEqual(argumentos[3], "Repouso")
        self.assertEqual(argumentos[4], "Reavaliar em 48 horas")
        self.assertEqual(argumentos[5], 25.0)
        self.assertEqual(argumentos[6], 12.5)
        self.assertIsInstance(argumentos[7], datetime)

    def test_outro_veterinario_nao_pode_concluir(self):
        self.repo.obter_por_id.return_value = self.consulta

        outro_medico = MedicoVeterinario(
            "Dra. Ana",
            "ana",
            "hash",
            "MV2"
        )

        with self.assertRaisesRegex(ValueError, "responsável"):
            self.service.concluir(
                1,
                outro_medico,
                "Virose",
                "Repouso",
                "Reavaliar",
                25.0,
                12.5
            )

        self.repo.concluir.assert_not_called()

    def test_consulta_concluida_nao_pode_ser_concluida(self):
        self.consulta.estado = "Concluída"
        self.repo.obter_por_id.return_value = self.consulta

        with self.assertRaisesRegex(ValueError, "agendadas"):
            self.service.concluir(
                1,
                self.medico,
                "Virose",
                "Repouso",
                "Reavaliar",
                25.0,
                12.5
            )

        self.repo.concluir.assert_not_called()

    def test_consulta_cancelada_nao_pode_ser_concluida(self):
        self.consulta.estado = "Cancelada"
        self.repo.obter_por_id.return_value = self.consulta

        with self.assertRaises(ValueError):
            self.service.concluir(
                1,
                self.medico,
                "Virose",
                "Repouso",
                "Reavaliar",
                25.0,
                12.5
            )

        self.repo.concluir.assert_not_called()

    def test_concluir_consulta_sem_diagnostico(self):
        self.repo.obter_por_id.return_value = self.consulta

        with self.assertRaisesRegex(ValueError, "diagnóstico"):
            self.service.concluir(
                1,
                self.medico,
                "",
                "Repouso",
                "Reavaliar",
                25.0,
                12.5
            )

        self.repo.concluir.assert_not_called()

    def test_concluir_consulta_sem_sumario(self):
        self.repo.obter_por_id.return_value = self.consulta

        with self.assertRaisesRegex(ValueError, "sumário"):
            self.service.concluir(
                1,
                self.medico,
                "Virose",
                "Repouso",
                "",
                25.0,
                12.5
            )

        self.repo.concluir.assert_not_called()

    def test_concluir_consulta_peso_invalido(self):
        self.repo.obter_por_id.return_value = self.consulta

        with self.assertRaisesRegex(ValueError, "peso"):
            self.service.concluir(
                1,
                self.medico,
                "Virose",
                "Repouso",
                "Reavaliar",
                25.0,
                -5.0
            )

        self.repo.concluir.assert_not_called()

    def test_concluir_consulta_custo_negativo(self):
        self.repo.obter_por_id.return_value = self.consulta

        with self.assertRaisesRegex(ValueError, "custo"):
            self.service.concluir(
                1,
                self.medico,
                "Virose",
                "Repouso",
                "Reavaliar",
                -10.0,
                12.5
            )

        self.repo.concluir.assert_not_called()


if __name__ == "__main__":
    unittest.main()
