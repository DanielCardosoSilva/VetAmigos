"""Vista gráfica de gestão de consultas."""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from math import isfinite

from src.models.medico_veterinario import MedicoVeterinario


def abrir(controller, animal_controller, funcionario=None, pai=None):
    # Criar a janela de consultas.
    janela = tk.Toplevel(pai) if pai is not None else tk.Tk()
    janela.title("VetAmigos - Gestão de Consultas")
    janela.geometry("1100x720")
    janela.minsize(850, 550)

    animais = []
    medicos = []
    consultas = []
    animais_ativos = []
    filtro_ids = []

    filtro_var = tk.StringVar()
    animal_var = tk.StringVar()
    medico_var = tk.StringVar()
    data_var = tk.StringVar()
    motivo_var = tk.StringVar()

    # Criar o histórico e o painel lateral de detalhes.
    area = ttk.Frame(janela, padding=10)
    area.pack(fill="both", expand=True)
    area.columnconfigure(0, weight=3)
    area.columnconfigure(1, weight=2)
    area.rowconfigure(1, weight=1)

    ttk.Label(area, text="Filtrar por animal:").grid(
        row=0, column=0, sticky="w", pady=5
    )
    combo_filtro = ttk.Combobox(
        area, textvariable=filtro_var, state="readonly", width=48
    )
    combo_filtro.grid(row=0, column=0, sticky="e", pady=5)

    quadro_lista = ttk.LabelFrame(area, text="Histórico de Consultas")
    quadro_lista.grid(
        row=1, column=0, sticky="nsew", padx=(0, 8)
    )

    barra = ttk.Scrollbar(quadro_lista)
    barra.pack(side="right", fill="y")

    lista = tk.Listbox(
        quadro_lista, exportselection=False,
        yscrollcommand=barra.set, width=60
    )
    lista.pack(fill="both", expand=True, padx=5, pady=5)
    barra.config(command=lista.yview)

    quadro_detalhes = ttk.LabelFrame(area, text="Detalhes da Consulta")
    quadro_detalhes.grid(row=1, column=1, sticky="nsew")

    detalhes = tk.Text(
        quadro_detalhes, state="disabled",
        wrap="word", width=40, height=16
    )
    detalhes.pack(fill="both", expand=True, padx=6, pady=6)

    # Criar o formulário, inicialmente oculto.
    quadro_form = ttk.LabelFrame(
        janela, text="Agendar Nova Consulta", padding=10
    )
    quadro_form.columnconfigure(1, weight=1)

    ttk.Label(quadro_form, text="Animal:").grid(
        row=0, column=0, sticky="w", padx=5, pady=5
    )
    combo_animal = ttk.Combobox(
        quadro_form, textvariable=animal_var, state="readonly"
    )
    combo_animal.grid(
        row=0, column=1, sticky="ew", padx=5, pady=5
    )

    ttk.Label(quadro_form, text="Médico:").grid(
        row=1, column=0, sticky="w", padx=5, pady=5
    )
    combo_medico = ttk.Combobox(
        quadro_form, textvariable=medico_var, state="readonly"
    )
    combo_medico.grid(
        row=1, column=1, sticky="ew", padx=5, pady=5
    )

    ttk.Label(
        quadro_form, text="Data/hora (DD-MM-AAAA HH:MM):"
    ).grid(row=2, column=0, sticky="w", padx=5, pady=5)

    ttk.Entry(
        quadro_form, textvariable=data_var
    ).grid(row=2, column=1, sticky="ew", padx=5, pady=5)

    ttk.Label(quadro_form, text="Motivo:").grid(
        row=3, column=0, sticky="w", padx=5, pady=5
    )
    ttk.Entry(
        quadro_form, textvariable=motivo_var
    ).grid(row=3, column=1, sticky="ew", padx=5, pady=5)

    def erro(mensagem):
        # Apresentar um erro ao utilizador.
        messagebox.showerror("VetAmigos", str(mensagem), parent=janela)

    def data_texto(valor):
        # Formatar datas para apresentação.
        return valor.strftime("%d-%m-%Y %H:%M") if valor else "—"

    def limpar_detalhes():
        # Limpar os detalhes da consulta selecionada.
        detalhes.config(state="normal")
        detalhes.delete("1.0", tk.END)
        detalhes.config(state="disabled")

    def selecionada():
        # Devolver a consulta selecionada.
        indices = lista.curselection()
        return consultas[indices[0]] if indices else None

    def selecionar(evento=None):
        # Mostrar os dados clínicos da consulta selecionada.
        consulta = selecionada()
        limpar_detalhes()

        if consulta is None:
            return

        nomes = {a.id: a.nome for a in animais}
        custo = (
            f"{consulta.custo:.2f} €"
            if consulta.custo is not None else "—"
        )

        linhas = [
            f"Consulta: #{consulta.id}",
            f"Animal: {nomes.get(consulta.id_animal, 'Desconhecido')}",
            f"Médico: {consulta.cedula_profissional}",
            f"Horário: {data_texto(consulta.horario)}",
            f"Estado: {consulta.estado}",
            f"Motivo: {consulta.motivo or '—'}",
            f"Diagnóstico: {consulta.diagnostico or '—'}",
            f"Tratamento: {consulta.tratamento or '—'}",
            f"Sumário: {consulta.sumario or '—'}",
            f"Custo: {custo}",
            f"Peso: {consulta.peso_registado if consulta.peso_registado is not None else '—'}",
            f"Conclusão: {data_texto(consulta.data_conclusao)}"
        ]

        detalhes.config(state="normal")
        detalhes.insert("1.0", "\n".join(linhas))
        detalhes.config(state="disabled")

    def carregar_referencias():
        # Carregar os animais e os médicos disponíveis.
        nonlocal animais, medicos, animais_ativos, filtro_ids

        animais = animal_controller.listar()
        animais_ativos = [
            a for a in animais if getattr(a, "ativo", True)
        ]
        medicos = [
            m for m in controller.medicos()
            if getattr(m, "ativo", True)
        ]

        filtro_ids = [None] + [a.id for a in animais]

        combo_filtro["values"] = ["Todos os animais"] + [
            f"{a.id} - {a.nome}" for a in animais
        ]
        combo_animal["values"] = [
            f"{a.id} - {a.nome}" for a in animais_ativos
        ]
        combo_medico["values"] = [
            f"{m.cedula_profissional} - {m.nome}" for m in medicos
        ]

        if combo_filtro.current() < 0:
            combo_filtro.current(0)

    def carregar_historico():
        # Atualizar o histórico conforme o filtro selecionado.
        nonlocal consultas

        lista.delete(0, tk.END)
        limpar_detalhes()
        consultas = []

        indice = combo_filtro.current()
        if indice < 0:
            indice = 0

        identificador = filtro_ids[indice]
        selecionados = (
            animais if identificador is None
            else [a for a in animais if a.id == identificador]
        )

        try:
            for animal in selecionados:
                consultas.extend(controller.historico(animal.id))

            consultas.sort(key=lambda c: c.horario, reverse=True)

            nomes = {a.id: a.nome for a in animais}

            for consulta in consultas:
                lista.insert(
                    tk.END,
                    f"#{consulta.id} | {data_texto(consulta.horario)} | "
                    f"{nomes.get(consulta.id_animal, 'Desconhecido')} | "
                    f"{consulta.estado} | {consulta.motivo}"
                )
        except Exception as exc:
            erro(exc)

    def nova_consulta():
        # Mostrar ou ocultar o formulário de agendamento.
        if quadro_form.winfo_manager():
            quadro_form.pack_forget()
        else:
            quadro_form.pack(fill="x", padx=10, pady=5)

    def guardar():
        # Validar os campos e agendar a consulta.
        indice_animal = combo_animal.current()
        indice_medico = combo_medico.current()

        if indice_animal < 0 or indice_medico < 0:
            messagebox.showwarning(
                "Campos obrigatórios",
                "Selecione um animal e um médico.",
                parent=janela
            )
            return

        if not motivo_var.get().strip():
            messagebox.showwarning(
                "Campo obrigatório",
                "Introduza o motivo da consulta.",
                parent=janela
            )
            return

        try:
            horario = datetime.strptime(
                data_var.get().strip(), "%d-%m-%Y %H:%M"
            )
        except ValueError:
            erro("Data inválida. Utilize DD-MM-AAAA HH:MM.")
            return

        try:
            consulta = controller.agendar(
                animais_ativos[indice_animal].id,
                medicos[indice_medico].cedula_profissional,
                horario,
                motivo_var.get().strip()
            )
        except Exception as exc:
            erro(exc)
            return

        messagebox.showinfo(
            "Consulta agendada",
            f"Consulta #{consulta.id} agendada com sucesso.",
            parent=janela
        )

        animal_var.set("")
        medico_var.set("")
        data_var.set("")
        motivo_var.set("")
        quadro_form.pack_forget()
        carregar_historico()

    def cancelar():
        # Cancelar a consulta selecionada após confirmação.
        consulta = selecionada()

        if consulta is None:
            messagebox.showwarning(
                "Consulta", "Selecione uma consulta.", parent=janela
            )
            return

        if not messagebox.askyesno(
            "Cancelar",
            f"Cancelar a consulta #{consulta.id}?",
            parent=janela
        ):
            return

        try:
            controller.cancelar(consulta.id)
        except Exception as exc:
            erro(exc)
            return

        carregar_historico()
        messagebox.showinfo(
            "Consulta", "Consulta cancelada.", parent=janela
        )

    def concluir():
        # Abrir o formulário clínico de conclusão da consulta.
        consulta = selecionada()

        if consulta is None:
            messagebox.showwarning(
                "Consulta", "Selecione uma consulta.", parent=janela
            )
            return

        if not isinstance(funcionario, MedicoVeterinario):
            erro("Apenas médicos veterinários podem concluir consultas.")
            return

        dialogo = tk.Toplevel(janela)
        dialogo.title(f"Concluir Consulta #{consulta.id}")
        dialogo.geometry("560x520")
        dialogo.transient(janela)
        dialogo.grab_set()
        dialogo.columnconfigure(1, weight=1)

        campos = {}

        for indice, nome in enumerate(
            ("Diagnóstico", "Tratamento", "Sumário", "Custo (€)", "Peso (kg)")
        ):
            ttk.Label(dialogo, text=nome).grid(
                row=indice, column=0, sticky="nw", padx=10, pady=8
            )

            campo = (
                tk.Text(dialogo, height=3, width=40)
                if indice < 3 else ttk.Entry(dialogo)
            )
            campo.grid(
                row=indice, column=1, sticky="ew", padx=10, pady=8
            )
            campos[nome] = campo

        def guardar_conclusao():
            # Validar e guardar os dados clínicos.
            diagnostico = campos["Diagnóstico"].get("1.0", tk.END).strip()
            tratamento = campos["Tratamento"].get("1.0", tk.END).strip()
            sumario = campos["Sumário"].get("1.0", tk.END).strip()

            try:
                custo = float(
                    campos["Custo (€)"].get().replace(",", ".")
                )
                peso = float(
                    campos["Peso (kg)"].get().replace(",", ".")
                )

                if not isfinite(custo) or not isfinite(peso):
                    raise ValueError("Introduza valores numéricos finitos.")

                controller.concluir(
                    consulta.id, funcionario, diagnostico,
                    tratamento, sumario, custo, peso
                )
            except Exception as exc:
                messagebox.showerror(
                    "Erro", str(exc), parent=dialogo
                )
                return

            dialogo.destroy()
            carregar_historico()
            messagebox.showinfo(
                "Consulta", "Consulta concluída.", parent=janela
            )

        ttk.Button(
            dialogo, text="Guardar conclusão",
            command=guardar_conclusao
        ).grid(row=5, column=1, sticky="e", padx=10, pady=10)

    # Criar os botões de ação.
    botoes = ttk.Frame(janela, padding=10)
    botoes.pack(fill="x")

    ttk.Button(
        botoes, text="Nova Consulta", command=nova_consulta
    ).pack(side="left", padx=4)

    ttk.Button(
        botoes, text="Guardar", command=guardar
    ).pack(side="left", padx=4)

    ttk.Button(
        botoes, text="Cancelar Consulta", command=cancelar
    ).pack(side="left", padx=4)

    if isinstance(funcionario, MedicoVeterinario):
        ttk.Button(
            botoes, text="Concluir Consulta", command=concluir
        ).pack(side="left", padx=4)

    ttk.Button(
        botoes, text="Atualizar", command=carregar_historico
    ).pack(side="left", padx=4)

    ttk.Button(
        botoes, text="Fechar", command=janela.destroy
    ).pack(side="right", padx=4)

    combo_filtro.bind(
        "<<ComboboxSelected>>", lambda evento: carregar_historico()
    )
    lista.bind("<<ListboxSelect>>", selecionar)

    try:
        carregar_referencias()
        carregar_historico()
    except Exception as exc:
        erro(exc)

    if pai is None:
        janela.mainloop()

    return janela
