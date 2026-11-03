"""Vista CLI de cliente."""
from src.views.common_view import menu, texto, mostrar

def abrir(controller):
    def registar():
        cliente = controller.registar(texto("Nome: "), texto("NIF: "), texto("Telefone: "), texto("Email: "))
        print(f"Cliente registado com ID {cliente.id}.")
    menu("Gerir clientes", {"1": ("Registar cliente", registar), "2": ("Listar clientes", lambda: mostrar(controller.listar())), "3": ("Consultar por NIF", lambda: mostrar(controller.consultar(texto("NIF: "))))})
