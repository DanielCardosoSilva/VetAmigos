"""Vista CLI de consultas."""
from src.views.common_view import menu, texto, inteiro, decimal, horario, mostrar
from src.models.medico_veterinario import MedicoVeterinario

def abrir(controller, funcionario=None):
    def agendar():
        medicos = [m for m in controller.medicos() if getattr(m, "ativo", True)]
        if not medicos:
            print("Não existem médicos veterinários ativos registados.")
            return
        for medico in medicos:
            print(f"{medico.nome} — Cédula: {medico.cedula_profissional}")
        consulta = controller.agendar(
            inteiro("ID do animal: "), texto("Cédula do médico: "),
            horario("Data e hora"), texto("Motivo da consulta: ")
        )
        print(f"Consulta agendada com ID {consulta.id}.")

    def consultar():
        consulta = controller.consultar(inteiro("ID da consulta: "))
        mostrar(consulta)
        if consulta:
            print(f"Motivo: {consulta.motivo}")
            print(f"Diagnóstico: {consulta.diagnostico}")
            print(f"Tratamento: {consulta.tratamento}")
            print(f"Sumário: {consulta.sumario}")
            print(f"Custo: {consulta.custo:.2f} € | Peso registado: {consulta.peso_registado}")
            print(f"Data da conclusão: {consulta.data_conclusao or '—'}")

    def cancelar():
        controller.cancelar(inteiro("ID da consulta: "))
        print("Consulta cancelada.")

    def concluir():
        identificador = inteiro("ID da consulta: ")
        consulta = controller.consultar(identificador)
        if consulta is None:
            print("Consulta não encontrada.")
            return
        print(f"Motivo: {consulta.motivo} | Estado: {consulta.estado}")
        diagnostico = texto("Diagnóstico: ")
        tratamento = texto("Tratamento: ")
        sumario = texto("Sumário/conclusão: ")
        custo = decimal("Custo (€): ")
        peso = decimal("Peso observado (kg): ")
        controller.concluir(identificador, funcionario, diagnostico, tratamento, sumario, custo, peso)
        print("Consulta concluída. O peso atual do animal foi atualizado.")

    opcoes = {
        "1": ("Agendar consulta", agendar),
        "2": ("Histórico por animal", lambda: mostrar(controller.historico(inteiro("ID do animal: ")))),
        "3": ("Consultar por ID", consultar),
        "4": ("Cancelar consulta", cancelar),
    }
    if isinstance(funcionario, MedicoVeterinario):
        opcoes["5"] = ("Concluir consulta", concluir)
    menu("Gerir consultas", opcoes)
