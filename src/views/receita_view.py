"""Vista CLI de receita."""
from src.views.common_view import menu, texto, inteiro, mostrar

def abrir(controller):
    def emitir():
        receita = controller.emitir(inteiro("ID da consulta: "))
        print(f"Receita emitida com ID {receita.id}.")
    def adicionar():
        prescrito = controller.adicionar(inteiro("ID da receita: "), inteiro("ID do medicamento: "), inteiro("Quantidade: "), texto("Posologia: "))
        print(f"Medicamento associado à receita (ID {prescrito.id}).")
    menu("Gerir receitas", {"1": ("Emitir receita", emitir), "2": ("Adicionar medicamento", adicionar), "3": ("Listar receitas por consulta", lambda: mostrar(controller.listar_por_consulta(inteiro("ID da consulta: ")))), "4": ("Medicamentos de uma receita", lambda: mostrar(controller.medicamentos(inteiro("ID da receita: "))))})
