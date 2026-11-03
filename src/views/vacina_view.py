"""Vista CLI de vacina."""
from datetime import date
from src.views.common_view import menu, texto, inteiro, data, mostrar

def abrir(controller):
    def registar():
        animal = inteiro("ID do animal: ")
        nome = texto("Vacina: ")
        administracao = data("Data de administração")
        proxima_texto = texto("Próxima dose (AAAA-MM-DD, vazio se não aplicável): ")
        proxima = date.fromisoformat(proxima_texto) if proxima_texto else None
        registo = controller.registar(animal, nome, administracao, proxima)
        print(f"Vacina registada com ID {registo.id}.")
    menu("Gerir vacinação", {"1": ("Registar vacina", registar), "2": ("Histórico por animal", lambda: mostrar(controller.historico(inteiro("ID do animal: ")))), "3": ("Próximas doses em atraso", lambda: mostrar(controller.atrasadas()))})
