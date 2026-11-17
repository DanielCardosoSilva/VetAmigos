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

    # ---------- T3.1: Janela Gestão de Consultas ----------
    janela = tk.Tk()
    janela.title("Gestão de Consultas")

    # Histórico: Listbox + Scrollbar (data + animal + motivo)
    quadro_lista = tk.LabelFrame(janela, text="Histórico de consultas")
    quadro_lista.pack(fill="both", expand=True, padx=10, pady=5)
    barra = tk.Scrollbar(quadro_lista)
    barra.pack(side="right", fill="y")
    lista = tk.Listbox(quadro_lista, width=70, height=10, yscrollcommand=barra.set)
    lista.pack(side="left", fill="both", expand=True)
    barra.config(command=lista.yview)

    animais = controller.animais()
    for animal in animais:
        for c in controller.historico(animal.id):
            lista.insert("end", f"{c.data_hora:%d-%m-%Y %H:%M} | {animal.nome} | {c.motivo}")

    # Formulário: Combobox (animal), Entry (data/hora), Text (descrição/diagnóstico)
    quadro_form = tk.LabelFrame(janela, text="Nova consulta")
    quadro_form.pack(fill="x", padx=10, pady=5)

    tk.Label(quadro_form, text="Animal:").grid(row=0, column=0, sticky="w", padx=5, pady=3)
    combo_animal = ttk.Combobox(quadro_form, state="readonly", width=40,
                                values=[f"{a.id} - {a.nome}" for a in animais])
    combo_animal.grid(row=0, column=1, padx=5, pady=3)

    tk.Label(quadro_form, text="Data/hora:").grid(row=1, column=0, sticky="w", padx=5, pady=3)
    entrada_data = tk.Entry(quadro_form, width=43)
    entrada_data.grid(row=1, column=1, padx=5, pady=3)

    tk.Label(quadro_form, text="Descrição/diagnóstico:").grid(row=2, column=0, sticky="nw", padx=5, pady=3)
    texto_descricao = tk.Text(quadro_form, width=43, height=5)
    texto_descricao.grid(row=2, column=1, padx=5, pady=3)

    # ---------- T3.2: Registo de consulta ----------
    quadro_form.pack_forget()
    tk.Button(janela, text="Nova Consulta",
              command=lambda: quadro_form.pack(fill="x", padx=10, pady=5)
              ).pack(pady=5)
    tk.Button(quadro_form, text="Guardar", command=lambda: (
        controller.registar(
            int(combo_animal.get().split(" - ")[0]),
            datetime.strptime(entrada_data.get(), "%d-%m-%Y %H:%M"),
            texto_descricao.get("1.0", "end").strip()),
        messagebox.showinfo("Consulta", "Consulta registada com sucesso."),
        quadro_form.pack_forget())
    ).grid(row=3, column=1, sticky="e", padx=5, pady=5)

    janela.mainloop()


    # ---------- T3.5: Data entries ----------
def ler_data(texto, formato="%d-%m-%Y", pai=None):
    try:
        return datetime.strptime(texto.strip(), formato)
    except ValueError:
        esperado = "dd-mm-aaaa" if formato == "%d-%m-%Y" else "dd-mm-aaaa hh:mm"
        messagebox.showerror("Data inválida", f"Use o formato {esperado}.", parent=pai)  # [T3.5]
        return None