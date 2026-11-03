"""Vista CLI de animal."""
from src.views.common_view import menu, texto, inteiro, decimal, data, mostrar

def abrir(controller):
    def registar():
        animal = controller.registar(texto("Nome: "), texto("Espécie: "), data("Data de nascimento"), decimal("Peso (kg): "), texto("NIF do cliente: "))
        print(f"Animal registado com ID {animal.id}.")
    menu("Gerir animais", {"1": ("Registar animal", registar), "2": ("Listar animais", lambda: mostrar(controller.listar())), "3": ("Consultar por ID", lambda: mostrar(controller.consultar(inteiro("ID do animal: "))))})
