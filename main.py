"""Ponto de entrada da aplicação VetAmigos (CLI + MVC)."""
from db.connection import inicializar_bd
from src.repositories.cliente_repository import ClienteRepository
from src.repositories.animal_repository import AnimalRepository
from src.repositories.consulta_repository import ConsultaRepository
from src.repositories.registo_vacina_repository import RegistoVacinaRepository
from src.repositories.medicamento_repository import MedicamentoRepository
from src.repositories.medicamento_prescrito_repository import MedicamentoPrescritoRepository
from src.repositories.receita_repository import ReceitaRepository
from src.repositories.fatura_repository import FaturaRepository
from src.repositories.funcionario_repository import FuncionarioRepository
from src.services.cliente_service import ClienteService
from src.services.animal_service import AnimalService
from src.services.consulta_service import ConsultaService
from src.services.registo_vacina_service import RegistoVacinaService
from src.services.medicamento_service import MedicamentoService
from src.services.medicamento_prescrito_service import MedicamentoPrescritoService
from src.services.receita_service import ReceitaService
from src.services.fatura_service import FaturaService
from src.services.funcionario_service import FuncionarioService
from src.controllers.cliente_controller import ClienteController
from src.controllers.animal_controller import AnimalController
from src.controllers.consulta_controller import ConsultaController
from src.controllers.vacina_controller import VacinaController
from src.controllers.medicamento_controller import MedicamentoController
from src.controllers.receita_controller import ReceitaController
from src.controllers.fatura_controller import FaturaController
from src.controllers.relatorio_controller import RelatorioController
from src.controllers.funcionario_controller import FuncionarioController
from src.controllers.auth_controller import AuthController
from src.views import login_view, menu_view, funcionario_view

def construir_controllers():
    cliente_repo = ClienteRepository()
    animal_repo = AnimalRepository()
    consulta_repo = ConsultaRepository()
    vacina_repo = RegistoVacinaRepository()
    medicamento_repo = MedicamentoRepository()
    prescrito_repo = MedicamentoPrescritoRepository()
    receita_repo = ReceitaRepository()
    fatura_repo = FaturaRepository()
    funcionario_repo = FuncionarioRepository()
    cliente_service = ClienteService(cliente_repo)
    animal_service = AnimalService(animal_repo, cliente_repo)
    consulta_service = ConsultaService(consulta_repo, animal_repo)
    vacina_service = RegistoVacinaService(vacina_repo, animal_repo)
    medicamento_service = MedicamentoService(medicamento_repo)
    prescrito_service = MedicamentoPrescritoService(prescrito_repo, receita_repo, medicamento_repo)
    receita_service = ReceitaService(receita_repo, consulta_repo)
    fatura_service = FaturaService(fatura_repo, consulta_repo)
    funcionario_service = FuncionarioService(funcionario_repo)
    return {
        "cliente": ClienteController(cliente_service, cliente_repo),
        "animal": AnimalController(animal_service, animal_repo),
        "consulta": ConsultaController(consulta_service, consulta_repo, funcionario_repo),
        "vacina": VacinaController(vacina_service),
        "medicamento": MedicamentoController(medicamento_service),
        "receita": ReceitaController(receita_service, receita_repo, prescrito_service),
        "fatura": FaturaController(fatura_service, fatura_repo),
        "relatorio": RelatorioController(cliente_service, animal_repo, consulta_repo, fatura_repo),
        "funcionario": FuncionarioController(funcionario_service, funcionario_repo),
        "auth": AuthController(funcionario_service)
    }

def main():
    inicializar_bd()
    controllers = construir_controllers()
    print("========== VETAMIGOS ==========")
    funcionario_view.registar_inicial(controllers["funcionario"])
    while True:
        funcionario = login_view.iniciar_sessao(controllers["auth"])
        if funcionario is None:
            print("Aplicação encerrada. Até à próxima!")
            break
        menu_view.abrir(funcionario, controllers)

if __name__ == "__main__":
    main()
