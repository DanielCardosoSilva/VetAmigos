"""Vista CLI de medicamento."""
from src.views.common_view import menu, texto, inteiro, mostrar

def abrir(controller):
    def registar():
        medicamento = controller.registar(texto("Nome: "), texto("Tipo: "), texto("Dose: "), inteiro("Quantidade: "))
        print(f"Medicamento registado com ID {medicamento.id}.")
    def atualizar():
        controller.atualizar(inteiro("ID do medicamento: "), inteiro("Nova quantidade: "))
        print("Quantidade atualizada.")
    menu("Gerir medicamentos", {"1": ("Registar medicamento", registar), "2": ("Listar medicamentos", lambda: mostrar(controller.listar())), "3": ("Atualizar quantidade", atualizar)})
