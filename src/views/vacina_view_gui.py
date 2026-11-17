"""Vista gráfica de gestão de vacinação."""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


def abrir(controller, animal_controller, pai=None):
    # Criar a janela gráfica de vacinação.
    janela = tk.Toplevel(pai) if pai is not None else tk.Tk()
    janela.title("VetAmigos - Gestão de Vacinação")
    janela.geometry("950x700")
    janela.minsize(750, 550)

    animais = []
    registos = []

    # Criar o painel de histórico de vacinação.
    quadro_historico = ttk.LabelFrame(janela, text="Histórico de vacinação")
    quadro_historico.pack(fill="both", expand=True, padx=10, pady=8)

    quadro_filtro = ttk.Frame(quadro_historico)
    quadro_filtro.pack(fill="x", padx=8, pady=5)

    ttk.Label(quadro_filtro, text="Animal:").pack(side="left", padx=5)

    combo_filtro = ttk.Combobox(
        quadro_filtro, state="readonly", width=45
    )
    combo_filtro.pack(side="left", padx=5)

    quadro_lista = ttk.Frame(quadro_historico)
    quadro_lista.pack(fill="both", expand=True, padx=8, pady=5)

    barra = ttk.Scrollbar(quadro_lista)
    barra.pack(side="right", fill="y")

    lista = tk.Listbox(
        quadro_lista,
        height=10,
        exportselection=False,
        yscrollcommand=barra.set
    )
    lista.pack(side="left", fill="both", expand=True)
    barra.config(command=lista.yview)

    # Criar o painel de detalhes do registo selecionado.
    quadro_detalhes = ttk.LabelFrame(janela, text="Detalhes da vacinação")
    quadro_detalhes.pack(fill="x", padx=10, pady=5)

    detalhes = tk.Text(
        quadro_detalhes,
        height=5,
        state="disabled",
        wrap="word"
    )
    detalhes.pack(fill="x", padx=8, pady=6)

    # Criar o formulário de registo de vacinas.
    quadro_form = ttk.LabelFrame(janela, text="Registar vacina")
    quadro_form.pack(fill="x", padx=10, pady=8)
    quadro_form.columnconfigure(1, weight=1)

    ttk.Label(quadro_form, text="Animal:").grid(
        row=0, column=0, sticky="w", padx=6, pady=5
    )
    combo_animal = ttk.Combobox(
        quadro_form, state="readonly", width=45
    )
    combo_animal.grid(
        row=0, column=1, sticky="ew", padx=6, pady=5
    )

    ttk.Label(quadro_form, text="Vacina:").grid(
        row=1, column=0, sticky="w", padx=6, pady=5
    )
    entrada_vacina = ttk.Entry(quadro_form)
    entrada_vacina.grid(
        row=1, column=1, sticky="ew", padx=6, pady=5
    )

    ttk.Label(quadro_form, text="Data de administração (DD-MM-AAAA):").grid(
        row=2, column=0, sticky="w", padx=6, pady=5
    )
    entrada_administracao = ttk.Entry(quadro_form)
    entrada_administracao.grid(
        row=2, column=1, sticky="ew", padx=6, pady=5
    )

    ttk.Label(quadro_form, text="Próxima dose (opcional):").grid(
        row=3, column=0, sticky="w", padx=6, pady=5
    )
    entrada_proxima = ttk.Entry(quadro_form)
    entrada_proxima.grid(
        row=3, column=1, sticky="ew", padx=6, pady=5
    )

    ttk.Label(
        quadro_form,
        text="Formato: DD-MM-AAAA. Deixe a próxima dose vazia se não aplicável."
    ).grid(
        row=4, column=0, columnspan=2,
        sticky="w", padx=6, pady=5
    )

    def mostrar_erro(erro):
        # Apresentar erros de validação ou de acesso aos dados.
        messagebox.showerror(
            "VetAmigos", str(erro), parent=janela
        )

    def ler_data(valor, obrigatoria=True):
        # Validar as datas introduzidas no formulário.
        valor = valor.strip()

        if not valor:
            if obrigatoria:
                raise ValueError("A data de administração é obrigatória.")
            return None

        try:
            return datetime.strptime(valor, "%d-%m-%Y").date()
        except ValueError:
            raise ValueError(
                "Data inválida. Utilize o formato DD-MM-AAAA."
            ) from None

    def limpar_detalhes():
        # Limpar o painel de detalhes.
        detalhes.config(state="normal")
        detalhes.delete("1.0", tk.END)
        detalhes.config(state="disabled")

    def selecionar_registo(evento=None):
        # Mostrar os detalhes do registo selecionado.
        indices = lista.curselection()
        limpar_detalhes()

        if not indices:
            return

        registo = registos[indices[0]]

        proxima = (
            registo.data_proxima_dose.strftime("%d-%m-%Y")
            if registo.data_proxima_dose else "Não aplicável"
        )

        linhas = [
            f"ID do registo: {registo.id}",
            f"ID do animal: {registo.id_animal}",
            f"Vacina: {registo.nome_vacina}",
            f"Data de administração: {registo.data_administracao:%d-%m-%Y}",
            f"Próxima dose: {proxima}"
        ]

        detalhes.config(state="normal")
        detalhes.insert("1.0", "\n".join(linhas))
        detalhes.config(state="disabled")

    def carregar_animais():
        # Obter os animais através do controller existente.
        nonlocal animais

        animais = animal_controller.listar()

        combo_filtro["values"] = ["Todos os animais"] + [
            f"{animal.id} - {animal.nome}"
            for animal in animais
        ]

        combo_animal["values"] = [
            f"{animal.id} - {animal.nome}"
            for animal in animais
            if getattr(animal, "ativo", True)
        ]

        combo_filtro.current(0)

    def apresentar_registos(novos_registos):
        # Preencher a lista com os registos recebidos.
        nonlocal registos

        registos = sorted(
            novos_registos,
            key=lambda registo: registo.data_administracao,
            reverse=True
        )

        lista.delete(0, tk.END)
        limpar_detalhes()

        nomes = {
            animal.id: animal.nome for animal in animais
        }

        for registo in registos:
            nome = nomes.get(registo.id_animal, "Desconhecido")
            proxima = (
                registo.data_proxima_dose.strftime("%d-%m-%Y")
                if registo.data_proxima_dose else "—"
            )

            lista.insert(
                tk.END,
                f"#{registo.id} | {nome} | "
                f"{registo.nome_vacina} | "
                f"{registo.data_administracao:%d-%m-%Y} | "
                f"Próxima: {proxima}"
            )

    def carregar_historico():
        # Recarregar o histórico do animal selecionado.
        indice = combo_filtro.current()
        selecionados = animais if indice <= 0 else [animais[indice - 1]]

        try:
            resultados = []

            for animal in selecionados:
                resultados.extend(controller.historico(animal.id))

            apresentar_registos(resultados)
        except (ValueError, TypeError, RuntimeError) as erro:
            mostrar_erro(erro)

    def mostrar_atrasadas():
        # Apresentar as próximas doses cuja data já passou.
        try:
            apresentar_registos(controller.atrasadas())
        except (ValueError, TypeError, RuntimeError) as erro:
            mostrar_erro(erro)

    def registar():
        # Validar o formulário e registar a vacinação.
        if combo_animal.current() < 0:
            messagebox.showwarning(
                "Seleção obrigatória",
                "Selecione um animal.",
                parent=janela
            )
            return

        nome = entrada_vacina.get().strip()

        if not nome:
            messagebox.showwarning(
                "Campo obrigatório",
                "Introduza o nome da vacina.",
                parent=janela
            )
            return

        try:
            identificador = int(
                combo_animal.get().split(" - ", 1)[0]
            )

            administracao = ler_data(
                entrada_administracao.get()
            )
            proxima = ler_data(
                entrada_proxima.get(), obrigatoria=False
            )

            registo = controller.registar(
                identificador,
                nome,
                administracao,
                proxima
            )
        except (ValueError, TypeError, RuntimeError) as erro:
            mostrar_erro(erro)
            return

        messagebox.showinfo(
            "Vacina registada",
            f"Vacinação #{registo.id} registada com sucesso.",
            parent=janela
        )

        entrada_vacina.delete(0, tk.END)
        entrada_administracao.delete(0, tk.END)
        entrada_proxima.delete(0, tk.END)

        carregar_historico()

    # Associar os eventos e criar os botões de ação.
    combo_filtro.bind(
        "<<ComboboxSelected>>",
        lambda evento: carregar_historico()
    )
    lista.bind("<<ListboxSelect>>", selecionar_registo)

    quadro_botoes = ttk.Frame(janela)
    quadro_botoes.pack(fill="x", padx=10, pady=10)

    ttk.Button(
        quadro_botoes, text="Registar vacina", command=registar
    ).pack(side="left", padx=4)

    ttk.Button(
        quadro_botoes, text="Atualizar histórico", command=carregar_historico
    ).pack(side="left", padx=4)

    ttk.Button(
        quadro_botoes, text="Doses em atraso", command=mostrar_atrasadas
    ).pack(side="left", padx=4)

    ttk.Button(
        quadro_botoes, text="Fechar", command=janela.destroy
    ).pack(side="right", padx=4)

    # Carregar os dados iniciais.
    try:
        carregar_animais()
        carregar_historico()
    except (ValueError, TypeError, RuntimeError) as erro:
        mostrar_erro(erro)

    if pai is None:
        janela.mainloop()

    return janela
