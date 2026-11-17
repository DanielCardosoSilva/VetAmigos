"""Vista gráfica de gestão de consultas."""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from src.models.medico_veterinario import MedicoVeterinario


def abrir(controller, animal_controller, funcionario=None, pai=None):
    # Criar a janela gráfica de consultas.
    janela = tk.Toplevel(pai) if pai is not None else tk.Tk()
    janela.title("VetAmigos - Gestão de Consultas")
    janela.geometry("1000x750")
    janela.minsize(800, 600)

    animais = []
    medicos = []
    consultas = []

    # Criar o painel de histórico.
    quadro_historico = ttk.LabelFrame(janela, text="Histórico de consultas")
    quadro_historico.pack(fill="both", expand=True, padx=10, pady=8)

    filtro = ttk.Frame(quadro_historico)
    filtro.pack(fill="x", padx=8, pady=5)

    ttk.Label(filtro, text="Animal:").pack(side="left", padx=5)
    combo_filtro = ttk.Combobox(filtro, state="readonly", width=45)
    combo_filtro.pack(side="left", padx=5)

    quadro_lista = ttk.Frame(quadro_historico)
    quadro_lista.pack(fill="both", expand=True, padx=8, pady=5)

    barra = ttk.Scrollbar(quadro_lista)
    barra.pack(side="right", fill="y")

    lista = tk.Listbox(
        quadro_lista, height=9, exportselection=False,
        yscrollcommand=barra.set
    )
    lista.pack(side="left", fill="both", expand=True)
    barra.config(command=lista.yview)

    # Criar o painel de detalhes.
    quadro_detalhes = ttk.LabelFrame(janela, text="Detalhes da consulta")
    quadro_detalhes.pack(fill="x", padx=10, pady=5)

    detalhes = tk.Text(
        quadro_detalhes, height=8, wrap="word", state="disabled"
    )
    detalhes.pack(fill="x", padx=8, pady=6)

    # Criar o formulário de agendamento.
    quadro_form = ttk.LabelFrame(janela, text="Agendar consulta")
    quadro_form.pack(fill="x", padx=10, pady=8)
    quadro_form.columnconfigure(1, weight=1)

    ttk.Label(quadro_form, text="Animal:").grid(
        row=0, column=0, sticky="w", padx=6, pady=4
    )
    combo_animal = ttk.Combobox(
        quadro_form, state="readonly", width=45
    )
    combo_animal.grid(
        row=0, column=1, sticky="ew", padx=6, pady=4
    )

    ttk.Label(quadro_form, text="Médico veterinário:").grid(
        row=1, column=0, sticky="w", padx=6, pady=4
    )
    combo_medico = ttk.Combobox(
        quadro_form, state="readonly", width=45
    )
    combo_medico.grid(
        row=1, column=1, sticky="ew", padx=6, pady=4
    )

    ttk.Label(quadro_form, text="Data/hora (DD-MM-AAAA HH:MM):").grid(
        row=2, column=0, sticky="w", padx=6, pady=4
    )
    entrada_data = ttk.Entry(quadro_form)
    entrada_data.grid(
        row=2, column=1, sticky="ew", padx=6, pady=4
    )

    ttk.Label(quadro_form, text="Motivo:").grid(
        row=3, column=0, sticky="nw", padx=6, pady=4
    )
    entrada_motivo = tk.Text(quadro_form, height=3)
    entrada_motivo.grid(
        row=3, column=1, sticky="ew", padx=6, pady=4
    )

    def mostrar_erro(erro):
        # Apresentar os erros devolvidos pela aplicação.
        messagebox.showerror("VetAmigos", str(erro), parent=janela)

    def formatar_data(valor):
        # Converter datas para uma apresentação legível.
        if valor is None:
            return "—"
        if hasattr(valor, "strftime"):
            return valor.strftime("%d-%m-%Y %H:%M")
        return str(valor)

    def limpar_detalhes():
        # Limpar os detalhes da consulta anteriormente selecionada.
        detalhes.config(state="normal")
        detalhes.delete("1.0", tk.END)
        detalhes.config(state="disabled")

    def obter_selecionada():
        # Identificar a consulta selecionada no histórico.
        indices = lista.curselection()
        if not indices:
            return None
        return consultas[indices[0]]

    def selecionar_consulta(evento=None):
        # Apresentar todos os detalhes disponíveis da consulta.
        consulta = obter_selecionada()
        limpar_detalhes()

        if consulta is None:
            return

        linhas = [
            f"ID: {consulta.id}",
            f"Animal: {consulta.id_animal}",
            f"Médico: {consulta.cedula_profissional}",
            f"Data/hora: {formatar_data(consulta.horario)}",
            f"Estado: {consulta.estado}",
            f"Motivo: {consulta.motivo or '—'}",
            f"Diagnóstico: {consulta.diagnostico or '—'}",
            f"Tratamento: {consulta.tratamento or '—'}",
            f"Sumário: {consulta.sumario or '—'}",
            f"Custo: {consulta.custo:.2f} €",
            f"Peso registado: {consulta.peso_registado if consulta.peso_registado is not None else '—'}",
            f"Data de conclusão: {formatar_data(consulta.data_conclusao)}"
        ]

        detalhes.config(state="normal")
        detalhes.insert("1.0", "\n".join(linhas))
        detalhes.config(state="disabled")

    def carregar_animais():
        # Obter os animais registados através do respetivo controller.
        nonlocal animais
        animais = animal_controller.listar()

        combo_filtro["values"] = ["Todos os animais"] + [
            f"{animal.id} - {animal.nome}" for animal in animais
        ]

        combo_animal["values"] = [
            f"{animal.id} - {animal.nome}"
            for animal in animais
            if getattr(animal, "ativo", True)
        ]

        combo_filtro.current(0)

    def carregar_medicos():
        # Obter apenas os médicos veterinários ativos.
        nonlocal medicos
        medicos = [
            medico for medico in controller.medicos()
            if getattr(medico, "ativo", True)
        ]

        combo_medico["values"] = [
            f"{medico.cedula_profissional} - {medico.nome}"
            for medico in medicos
        ]

    def carregar_historico():
        # Atualizar a lista de consultas do animal selecionado.
        nonlocal consultas
        consultas = []
        lista.delete(0, tk.END)
        limpar_detalhes()

        indice = combo_filtro.current()
        selecionados = animais if indice <= 0 else [animais[indice - 1]]

        try:
            for animal in selecionados:
                for consulta in controller.historico(animal.id):
                    consultas.append(consulta)

            consultas.sort(
                key=lambda consulta: consulta.horario,
                reverse=True
            )

            nomes = {animal.id: animal.nome for animal in animais}

            for consulta in consultas:
                nome = nomes.get(consulta.id_animal, "Desconhecido")
                lista.insert(
                    tk.END,
                    f"#{consulta.id} | "
                    f"{formatar_data(consulta.horario)} | "
                    f"{nome} | {consulta.estado} | {consulta.motivo}"
                )
        except (ValueError, TypeError, RuntimeError) as erro:
            mostrar_erro(erro)

    def agendar():
        # Validar o formulário e registar a nova consulta.
        indice_animal = combo_animal.current()
        indice_medico = combo_medico.current()

        if indice_animal < 0 or indice_medico < 0:
            messagebox.showwarning(
                "Campos obrigatórios",
                "Selecione um animal e um médico veterinário.",
                parent=janela
            )
            return

        try:
            horario = datetime.strptime(
                entrada_data.get().strip(), "%d-%m-%Y %H:%M"
            )
        except ValueError:
            messagebox.showerror(
                "Data inválida",
                "Utilize o formato DD-MM-AAAA HH:MM.",
                parent=janela
            )
            return

        motivo = entrada_motivo.get("1.0", tk.END).strip()
        if not motivo:
            messagebox.showwarning(
                "Campos obrigatórios",
                "Introduza o motivo da consulta.",
                parent=janela
            )
            return

        try:
            identificador = int(
                combo_animal.get().split(" - ", 1)[0]
            )
            medico = medicos[indice_medico]

            consulta = controller.agendar(
                identificador,
                medico.cedula_profissional,
                horario,
                motivo
            )
        except (ValueError, TypeError, RuntimeError) as erro:
            mostrar_erro(erro)
            return

        messagebox.showinfo(
            "Consulta agendada",
            f"Consulta #{consulta.id} agendada com sucesso.",
            parent=janela
        )

        entrada_data.delete(0, tk.END)
        entrada_motivo.delete("1.0", tk.END)
        carregar_historico()

    def cancelar():
        # Cancelar a consulta selecionada após confirmação.
        consulta = obter_selecionada()

        if consulta is None:
            messagebox.showwarning(
                "Seleção obrigatória",
                "Selecione uma consulta no histórico.",
                parent=janela
            )
            return

        if not messagebox.askyesno(
            "Cancelar consulta",
            f"Deseja cancelar a consulta #{consulta.id}?",
            parent=janela
        ):
            return

        try:
            controller.cancelar(consulta.id)
            carregar_historico()
            messagebox.showinfo(
                "Consulta cancelada",
                "Consulta cancelada com sucesso.",
                parent=janela
            )
        except (ValueError, TypeError, RuntimeError) as erro:
            mostrar_erro(erro)

    def concluir():
        # Permitir a conclusão apenas por um médico veterinário autenticado.
        consulta = obter_selecionada()

        if consulta is None:
            messagebox.showwarning(
                "Seleção obrigatória",
                "Selecione uma consulta.",
                parent=janela
            )
            return

        if not isinstance(funcionario, MedicoVeterinario):
            mostrar_erro("Apenas médicos veterinários podem concluir consultas.")
            return

        dialogo = tk.Toplevel(janela)
        dialogo.title(f"Concluir consulta #{consulta.id}")
        dialogo.geometry("550x510")
        dialogo.transient(janela)
        dialogo.grab_set()
        dialogo.columnconfigure(1, weight=1)

        campos = {}

        for linha, nome in enumerate(
            ("Diagnóstico", "Tratamento", "Sumário", "Custo (€)", "Peso (kg)")
        ):
            ttk.Label(dialogo, text=f"{nome}:").grid(
                row=linha, column=0, sticky="nw", padx=10, pady=8
            )

            if linha < 3:
                campo = tk.Text(dialogo, height=3, width=40)
            else:
                campo = ttk.Entry(dialogo, width=40)

            campo.grid(
                row=linha, column=1, sticky="ew", padx=10, pady=8
            )
            campos[nome] = campo

        def guardar_conclusao():
            # Recolher os dados clínicos e concluir a consulta.
            diagnostico = campos["Diagnóstico"].get("1.0", tk.END).strip()
            tratamento = campos["Tratamento"].get("1.0", tk.END).strip()
            sumario = campos["Sumário"].get("1.0", tk.END).strip()

            try:
                custo = float(
                    campos["Custo (€)"].get().strip().replace(",", ".")
                )
                peso = float(
                    campos["Peso (kg)"].get().strip().replace(",", ".")
                )

                controller.concluir(
                    consulta.id,
                    funcionario,
                    diagnostico,
                    tratamento,
                    sumario,
                    custo,
                    peso
                )
            except (ValueError, TypeError, RuntimeError) as erro:
                messagebox.showerror(
                    "Erro ao concluir",
                    str(erro),
                    parent=dialogo
                )
                return

            dialogo.destroy()
            carregar_historico()
            messagebox.showinfo(
                "Consulta concluída",
                "Consulta concluída com sucesso.",
                parent=janela
            )

        ttk.Button(
            dialogo, text="Guardar conclusão", command=guardar_conclusao
        ).grid(row=5, column=1, sticky="e", padx=10, pady=12)

    # Associar os eventos e os botões às operações.
    combo_filtro.bind(
        "<<ComboboxSelected>>",
        lambda evento: carregar_historico()
    )
    lista.bind("<<ListboxSelect>>", selecionar_consulta)

    quadro_botoes = ttk.Frame(janela)
    quadro_botoes.pack(fill="x", padx=10, pady=8)

    ttk.Button(
        quadro_botoes, text="Agendar consulta", command=agendar
    ).pack(side="left", padx=4)

    ttk.Button(
        quadro_botoes, text="Atualizar histórico", command=carregar_historico
    ).pack(side="left", padx=4)

    ttk.Button(
        quadro_botoes, text="Cancelar selecionada", command=cancelar
    ).pack(side="left", padx=4)

    if isinstance(funcionario, MedicoVeterinario):
        ttk.Button(
            quadro_botoes, text="Concluir selecionada", command=concluir
        ).pack(side="left", padx=4)

    ttk.Button(
        quadro_botoes, text="Fechar", command=janela.destroy
    ).pack(side="right", padx=4)

    # Carregar os dados iniciais da janela.
    try:
        carregar_animais()
        carregar_medicos()
        carregar_historico()
    except (ValueError, TypeError, RuntimeError) as erro:
        mostrar_erro(erro)

    if pai is None:
        janela.mainloop()

    return janela
