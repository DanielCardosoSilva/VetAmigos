"""tests/test_registo_vacina.py"""

import unittest
from unittest.mock import MagicMock
from datetime import date

from src.models.registo_vacina import RegistoVacina
from src.services.registo_vacina_service import RegistoVacinaService


class TestRegistoVacina(unittest.TestCase):

    def setUp(self):
        self.repo = MagicMock()
        self.animal_repo = MagicMock()
        self.service = RegistoVacinaService(self.repo, self.animal_repo)

    def test_criar_registo_vacina(self):
        registo = RegistoVacina(
            1, "Raiva", date(2026, 10, 1), date(2027, 10, 1)
        )

        self.assertIsNone(registo.id)
        self.assertEqual(registo.id_animal, 1)
        self.assertEqual(registo.nome_vacina, "Raiva")

    def test_registar_vacina(self):
        self.animal_repo.obter_por_id.return_value = MagicMock()
        self.repo.inserir.side_effect = lambda registo: registo

        resultado = self.service.registar(
            1, "Raiva", date(2026, 10, 1), date(2027, 10, 1)
        )

        self.assertIsInstance(resultado, RegistoVacina)
        self.repo.inserir.assert_called_once()

    def test_animal_inexistente(self):
        self.animal_repo.obter_por_id.return_value = None

        with self.assertRaises(ValueError):
            self.service.registar(
                999, "Raiva", date(2026, 10, 1), date(2027, 10, 1)
            )

        self.repo.inserir.assert_not_called()

    def test_nome_vacina_vazio(self):
        with self.assertRaises(ValueError):
            self.service.registar(
                1, "", date(2026, 10, 1), date(2027, 10, 1)
            )

        self.repo.inserir.assert_not_called()

    def test_data_administracao_futura(self):
        with self.assertRaises(ValueError):
            self.service.registar(
                1, "Raiva", date(2099, 1, 1), None
            )

        self.repo.inserir.assert_not_called()

    def test_proxima_dose_anterior(self):
        with self.assertRaises(ValueError):
            self.service.registar(
                1, "Raiva", date(2026, 10, 1), date(2026, 9, 1)
            )

        self.repo.inserir.assert_not_called()

    def test_listar_por_animal(self):
        self.animal_repo.obter_por_id.return_value = MagicMock()
        self.repo.listar_por_animal.return_value = []

        resultado = self.service.listar_por_animal(1)

        self.assertEqual(resultado, [])
        self.repo.listar_por_animal.assert_called_once_with(1)

    def test_listar_animal_inexistente(self):
        self.animal_repo.obter_por_id.return_value = None

        with self.assertRaises(ValueError):
            self.service.listar_por_animal(999)

        self.repo.listar_por_animal.assert_not_called()


if __name__ == "__main__":
    unittest.main()
