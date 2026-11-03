"""tests/test_medico_veterinario.py"""

import unittest

from src.models.funcionario import Funcionario
from src.models.medico_veterinario import MedicoVeterinario


class TestMedicoVeterinario(unittest.TestCase):

    def test_criar_medico_veterinario(self):
        medico = MedicoVeterinario(
            "Dr. João",
            "joao",
            "hash_exemplo",
            "12345"
        )

        self.assertIsNone(medico.id)
        self.assertEqual(medico.nome, "Dr. João")
        self.assertEqual(medico.cedula_profissional, "12345")

    def test_heranca_funcionario(self):
        medico = MedicoVeterinario(
            "Dr. João",
            "joao",
            "hash_exemplo",
            "12345"
        )

        self.assertIsInstance(medico, Funcionario)


if __name__ == "__main__":
    unittest.main()
