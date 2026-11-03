"""Vista CLI de consulta."""
from src.views.common_view import menu, texto, inteiro, horario, mostrar

def abrir(controller):
    def agendar():
        medicos = controller.medicos()
        if not medicos:
            print("Não existem médicos veterinários registados.")
            return
        for medico in medicos:
            print(f"{medico.nome} — Cédula: {medico.cedula_profissional}")
        consulta = controller.agendar(inteiro("ID do animal: "), texto("Cédula do médico: "), horario("Data e hora"))
        print(f"Consulta agendada com ID {consulta.id}.")
    def consultar():
        consulta = controller.consultar(inteiro("ID da consulta: "))
        mostrar(consulta)
        if consulta:
            print(f"Diagnóstico: {consulta.diagnostico} | Tratamento: {consulta.tratamento} | Custo: {consulta.custo:.2f} € | Peso: {consulta.peso_registado}")
    def cancelar():
        controller.cancelar(inteiro("ID da consulta: "))
        print("Consulta cancelada.")
    menu("Gerir consultas", {"1": ("Agendar consulta", agendar), "2": ("Histórico por animal", lambda: mostrar(controller.historico(inteiro("ID do animal: ")))), "3": ("Consultar por ID", consultar), "4": ("Cancelar consulta", cancelar)})
