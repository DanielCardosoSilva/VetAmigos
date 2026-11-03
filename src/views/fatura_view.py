"""Vista CLI de fatura."""
from src.views.common_view import menu, texto, inteiro, decimal, mostrar

def abrir(controller):
    def emitir():
        fatura = controller.emitir(inteiro("ID da consulta: "), decimal("Valor total (€): "), texto("Método de pagamento (vazio se pendente): ") or None)
        print(f"Fatura emitida com ID {fatura.id} ({fatura.estado}).")
    menu("Gerir faturas e pagamentos", {"1": ("Emitir fatura", emitir), "2": ("Consultar por consulta", lambda: mostrar(controller.consultar(inteiro("ID da consulta: "))))})
