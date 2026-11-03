"""tests/test_animal.py"""

import unittest
from unittest.mock import MagicMock
from datetime import date

from src.models.animal import Animal
from src.services.animal_service import AnimalService


class TestAnimal(unittest.TestCase):

    def setUp(self):
        self.repo = MagicMock()
        self.cliente_repo = MagicMock()
        self.service = AnimalService(self.repo, self.cliente_repo)

    def test_criar_animal(self):
        animal = Animal(
            nome="Rex",
            especie="Cão",
            data_nasc=date(2022, 5, 10),
            peso_animal=15.5,
            nif_cliente="123456789"
        )

        self.assertIsNone(animal.id)
        self.assertEqual(animal.nome, "Rex")
        self.assertEqual(animal.especie, "Cão")
        self.assertEqual(animal.peso_animal, 15.5)

    def test_registar_animal(self):
        self.cliente_repo.obter_por_nif.return_value = MagicMock()
        self.repo.inserir.side_effect = lambda animal: animal

        animal = self.service.registar(
            "Rex",
            "Cão",
            date(2022, 5, 10),
            15.5,
            "123456789"
        )

        self.assertIsInstance(animal, Animal)
        self.repo.inserir.assert_called_once()

    def test_registar_animal_cliente_inexistente(self):
        self.cliente_repo.obter_por_nif.return_value = None

        with self.assertRaises(ValueError):
            self.service.registar(
                "Rex",
                "Cão",
                date(2022, 5, 10),
                15.5,
                "123456789"
            )

        self.repo.inserir.assert_not_called()

    def test_registar_animal_peso_invalido(self):
        with self.assertRaises(ValueError):
            self.service.registar(
                "Rex",
                "Cão",
                date(2022, 5, 10),
                -5,
                "123456789"
            )

        self.repo.inserir.assert_not_called()

    def test_registar_animal_data_futura(self):
        with self.assertRaises(ValueError):
            self.service.registar(
                "Rex",
                "Cão",
                date(2099, 1, 1),
                15.5,
                "123456789"
            )

        self.repo.inserir.assert_not_called()


if __name__ == "__main__":
    unittest.main()
