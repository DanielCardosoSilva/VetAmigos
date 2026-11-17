"""Vista gráfica de gestão de vacinação."""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


def abrir(controller, animal_controller, pai=None):
    # Criar a janela gráfica de vacinação.
    janela = tk.Toplevel(pai) if pai is not None else tk.Tk()
    janela.title("VetAmigos - Gestão de Vacinação")
    janela.geometry("1000x690")
    janela.minsize(800, 550)

    animais = []
    animais_ativos = []
    registos = []
    filtro_ids = []

    filtro_var = tk.StringVar()
    animal_var = tk.StringVar()
    vacina_var = tk.StringVar()
    administracao_var = tk.StringVar()
    proxima_var = tk.StringVar()

    # Criar a área de histórico com painel lateral.
    area = ttk.Frame(janela, padding=10)
    area.pack(fill="both", expand=True)
    area.columnconfigure(0, weight=3)
    area.columnconfigure(1, weight=2)
    area.rowconfigure(1, weight=1)

    ttk.Label(area, text="Filtrar por animal:").grid(
        row=0, column=0, sticky="w", pady=5
    )

    combo_filtro = ttk.Combobox(
        area, textvariable=filtro_var, state="readonly", width=45
    )
    combo_filtro.grid(row=0, column=0, sticky="e", pady=5)

    quadro_lista = ttk.LabelFrame(area, text="Histórico de Vacinação")
    quadro_lista.grid(
        row=1, column=0, sticky="nsew", padx=(0, 8)
    )

    barra = ttk.Scrollbar(quadro_lista)
    barra.pack(side="right", fill="y")

    lista = tk.Listbox(
        quadro_lista, yscrollcommand=barra.set,
        exportselection=False, width=60
    )
    lista.pack(fill="both", expand=True, padx=5, pady=5)
    barra.config(command=lista.yview)

    quadro_detalhes = ttk.LabelFrame(
        area, text="Detalhes da Vacinação"
    )
    quadro_detalhes.grid(row=1, column=1, sticky="nsew")

    detalhes = tk.Text(
        quadro_detalhes, state="disabled",
        wrap="word", width=35
    )
    detalhes.pack(fill="both", expand=True, padx=6, pady=6)

    # Criar o formulário de vacinação.
    quadro_form = ttk.LabelFrame(
        janela, text="Registar Vacina", padding=10
    )
    quadro_form.pack(fill="x", padx=10, pady=8)
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

    ttk.Label(quadro_form, text="Nome da vacina:").grid(
        row=1, column=0, sticky="w", padx=5, pady=5
    )
    ttk.Entry(
        quadro_form, textvariable=vacina_var
    ).grid(row=1, column=1, sticky="ew", padx=5, pady=5)

    ttk.Label(
        quadro_form, text="Administração (DD-MM-AAAA):"
    ).grid(row=2, column=0, sticky="w", padx=5, pady=5)

    ttk.Entry(
        quadro_form, textvariable=administracao_var
    ).grid(row=2, column=1, sticky="ew", padx=5, pady=5)

    ttk.Label(
        quadro_form, text="Próxima dose (DD-MM-AAAA):"
    ).grid(row=3, column=0, sticky="w", padx=5, pady=5)

    ttk.Entry(
        quadro_form, textvariable=proxima_var
    ).grid(row=3, column=1, sticky="ew", padx=5, pady=5)

    ttk.Label(
        quadro_form,
        text="A próxima dose é opcional."
    ).grid(row=4, column=1, sticky="w", padx=5)

    def erro(mensagem):
        # Apresentar uma mensagem de erro.
        messagebox.showerror(
            "VetAmigos", str(mensagem), parent=janela
        )

    def data_texto(valor):
        # Formatar uma data para apresentação.
        return valor.strftime("%d-%m-%Y") if valor else "—"

    def ler_data(valor, obrigatoria=True):
        # Validar uma data introduzida no formulário.
        valor = valor.strip()

        if not valor:
            if obrigatoria:
                raise ValueError("A data de administração é obrigatória.")
            return None

        try:
            return datetime.strptime(valor, "%d-%m-%Y").date()
        except ValueError:
            raise ValueError(
                "Data inválida. Utilize DD-MM-AAAA."
            ) from None

    def limpar_detalhes():
        # Limpar o painel de detalhes.
        detalhes.config(state="normal")
        detalhes.delete("1.0", tk.END)
        detalhes.config(state="disabled")

    def selecionar(evento=None):
        # Apresentar os detalhes do registo selecionado.
        indices = lista.curselection()
        limpar_detalhes()

        if not indices:
            return

        registo = registos[indices[0]]
        nomes = {a.id: a.nome for a in animais}

        linhas = [
            f"Registo: #{registo.id}",
            f"Animal: {nomes.get(registo.id_animal, 'Desconhecido')}",
            f"Vacina: {registo.nome_vacina}",
            f"Administração: {data_texto(registo.data_administracao)}",
            f"Próxima dose: {data_texto(registo.data_proxima_dose)}"
        ]

        detalhes.config(state="normal")
        detalhes.insert("1.0", "\n".join(linhas))
        detalhes.config(state="disabled")

    def carregar_animais():
        # Carregar animais para os filtros e o formulário.
        nonlocal animais, animais_ativos, filtro_ids

        animais = animal_controller.listar()
        animais_ativos = [
            a for a in animais if getattr(a, "ativo", True)
        ]

        filtro_ids = [None] + [a.id for a in animais]

        combo_filtro["values"] = ["Todos os animais"] + [
            f"{a.id} - {a.nome}" for a in animais
        ]
        combo_animal["values"] = [
            f"{a.id} - {a.nome}" for a in animais_ativos
        ]

        combo_filtro.current(0)

    def apresentar_registos(resultados):
        # Preencher o histórico com os registos recebidos.
        nonlocal registos

        registos = sorted(
            resultados,
            key=lambda r: r.data_administracao,
            reverse=True
        )

        lista.delete(0, tk.END)
        limpar_detalhes()

        nomes = {a.id: a.nome for a in animais}

        for registo in registos:
            lista.insert(
                tk.END,
                f"#{registo.id} | "
                f"{nomes.get(registo.id_animal, 'Desconhecido')} | "
                f"{registo.nome_vacina} | "
                f"{data_texto(registo.data_administracao)} | "
                f"Próxima: {data_texto(registo.data_proxima_dose)}"
            )

    def carregar_historico():
        # Consultar os registos do animal selecionado.
        indice = combo_filtro.current()
        if indice < 0:
            indice = 0

        identificador = filtro_ids[indice]
        selecionados = (
            animais if identificador is None
            else [a for a in animais if a.id == identificador]
        )

        try:
            resultados = []
            for animal in selecionados:
                resultados.extend(controller.historico(animal.id))

            apresentar_registos(resultados)
        except Exception as exc:
            erro(exc)

    def mostrar_atrasadas():
        # Apresentar as vacinas com próxima dose em atraso.
        try:
            apresentar_registos(controller.atrasadas())
        except Exception as exc:
            erro(exc)

    def guardar():
        # Validar os campos e registar a vacina.
        indice = combo_animal.current()

        if indice < 0:
            messagebox.showwarning(
                "Campo obrigatório",
                "Selecione um animal.",
                parent=janela
            )
            return

        nome = vacina_var.get().strip()
        if not nome:
            messagebox.showwarning(
                "Campo obrigatório",
                "Introduza o nome da vacina.",
                parent=janela
            )
            return

        try:
            administracao = ler_data(administracao_var.get())
            proxima = ler_data(proxima_var.get(), obrigatoria=False)

            registo = controller.registar(
                animais_ativos[indice].id,
                nome,
                administracao,
                proxima
            )
        except Exception as exc:
            erro(exc)
            return

        messagebox.showinfo(
            "Vacinação",
            f"Vacina registada com ID #{registo.id}.",
            parent=janela
        )

        vacina_var.set("")
        administracao_var.set("")
        proxima_var.set("")
        carregar_historico()

    # Criar os botões e associar os eventos.
    botoes = ttk.Frame(janela, padding=10)
    botoes.pack(fill="x")

    ttk.Button(
        botoes, text="Registar Vacina", command=guardar
    ).pack(side="left", padx=4)

    ttk.Button(
        botoes, text="Atualizar Histórico", command=carregar_historico
    ).pack(side="left", padx=4)

    ttk.Button(
        botoes, text="Doses em Atraso", command=mostrar_atrasadas
    ).pack(side="left", padx=4)

    ttk.Button(
        botoes, text="Fechar", command=janela.destroy
    ).pack(side="right", padx=4)

    combo_filtro.bind(
        "<<ComboboxSelected>>", lambda evento: carregar_historico()
    )
    lista.bind("<<ListboxSelect>>", selecionar)

    try:
        carregar_animais()
        carregar_historico()
    except Exception as exc:
        erro(exc)

    if pai is None:
        janela.mainloop()

    return janela
