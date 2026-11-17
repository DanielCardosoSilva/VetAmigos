"""Vista gráfica de faturação."""

import tkinter as tk
from tkinter import ttk, messagebox


def abrir(controller, consulta_controller, animal_controller,
          cliente_controller, pai=None):
    # Criar a janela de faturação.
    janela = tk.Toplevel(pai) if pai is not None else tk.Tk()
    janela.title("VetAmigos - Gestão de Faturas")
    janela.geometry("1050x720")
    janela.minsize(850, 600)

    faturas = []
    consultas = []
    animais = {}
    clientes = {}
    opcoes_consulta = {}

    estado_var = tk.StringVar(value="Pendente")
    metodo_var = tk.StringVar()
    consulta_var = tk.StringVar()

    # Construir a lista de faturas.
    quadro_lista = ttk.LabelFrame(janela, text="Lista de Faturas")
    quadro_lista.pack(fill="both", expand=True, padx=12, pady=8)

    area_lista = ttk.Frame(quadro_lista)
    area_lista.pack(fill="both", expand=True, padx=8, pady=8)

    barra = ttk.Scrollbar(area_lista)
    barra.pack(side="right", fill="y")

    lista = tk.Listbox(
        area_lista, height=11, exportselection=False,
        yscrollcommand=barra.set
    )
    lista.pack(side="left", fill="both", expand=True)
    barra.config(command=lista.yview)

    # Criar o formulário de emissão.
    quadro_emissao = ttk.LabelFrame(janela, text="Emitir Nova Fatura")
    quadro_emissao.pack(fill="x", padx=12, pady=8)
    quadro_emissao.columnconfigure(1, weight=1)

    ttk.Label(quadro_emissao, text="Consulta:").grid(
        row=0, column=0, sticky="w", padx=8, pady=5
    )
    combo_consulta = ttk.Combobox(
        quadro_emissao, textvariable=consulta_var, state="readonly"
    )
    combo_consulta.grid(
        row=0, column=1, sticky="ew", padx=8, pady=5
    )

    ttk.Label(quadro_emissao, text="Valor total (€):").grid(
        row=1, column=0, sticky="w", padx=8, pady=5
    )
    entrada_valor = ttk.Entry(quadro_emissao)
    entrada_valor.grid(
        row=1, column=1, sticky="ew", padx=8, pady=5
    )

    ttk.Label(quadro_emissao, text="Método de pagamento:").grid(
        row=2, column=0, sticky="w", padx=8, pady=5
    )
    combo_metodo = ttk.Combobox(
        quadro_emissao, state="readonly",
        values=["Pendente", "Numerário", "Multibanco", "Transferência", "MB WAY"]
    )
    combo_metodo.current(0)
    combo_metodo.grid(
        row=2, column=1, sticky="ew", padx=8, pady=5
    )

    # Criar a área de consulta e alteração de estado.
    quadro_estado = ttk.LabelFrame(janela, text="Estado da Fatura Selecionada")
    quadro_estado.pack(fill="x", padx=12, pady=8)

    for texto in ("Pendente", "Pago", "Anulada"):
        ttk.Radiobutton(
            quadro_estado, text=texto,
            variable=estado_var, value=texto
        ).pack(side="left", padx=12, pady=8)

    ttk.Label(quadro_estado, text="Pagamento:").pack(side="left", padx=5)

    combo_pagamento = ttk.Combobox(
        quadro_estado, textvariable=metodo_var, width=18,
        values=["Numerário", "Multibanco", "Transferência", "MB WAY"]
    )
    combo_pagamento.pack(side="left", padx=5)

    # Mostrar os detalhes da fatura.
    quadro_detalhes = ttk.LabelFrame(janela, text="Detalhes")
    quadro_detalhes.pack(fill="x", padx=12, pady=8)

    detalhes = tk.Text(
        quadro_detalhes, height=5, state="disabled", wrap="word"
    )
    detalhes.pack(fill="x", padx=8, pady=5)

    def mostrar_erro(erro):
        # Apresentar erros de validação e acesso aos dados.
        messagebox.showerror("Faturação", str(erro), parent=janela)

    def cliente_da_consulta(consulta):
        # Identificar o cliente associado ao animal da consulta.
        animal = animais.get(consulta.id_animal)
        if animal is None:
            return "Cliente desconhecido"

        cliente = clientes.get(str(animal.nif_cliente))
        return cliente.nome if cliente else str(animal.nif_cliente)

    def carregar_referencias():
        # Carregar clientes, animais e consultas para os formulários.
        nonlocal consultas, animais, clientes, opcoes_consulta

        animais_lista = animal_controller.listar()
        animais = {animal.id: animal for animal in animais_lista}

        clientes_lista = cliente_controller.listar()
        clientes = {str(cliente.nif): cliente for cliente in clientes_lista}

        consultas = []
        for animal in animais_lista:
            consultas.extend(consulta_controller.historico(animal.id))

        existentes = {f.id_consulta for f in controller.listar()}
        opcoes_consulta = {}

        for consulta in consultas:
            if consulta.id in existentes:
                continue

            animal = animais.get(consulta.id_animal)
            nome_animal = animal.nome if animal else "Desconhecido"
            nome_cliente = cliente_da_consulta(consulta)

            descricao = (
                f"#{consulta.id} | {nome_animal} | {nome_cliente}"
            )
            opcoes_consulta[descricao] = consulta.id

        combo_consulta["values"] = list(opcoes_consulta)
        consulta_var.set("")

    def carregar_faturas():
        # Atualizar a lista com todas as faturas registadas.
        nonlocal faturas

        faturas = controller.listar()
        lista.delete(0, tk.END)

        referencias = {c.id: c for c in consultas}

        for fatura in faturas:
            consulta = referencias.get(fatura.id_consulta)
            cliente = (
                cliente_da_consulta(consulta)
                if consulta is not None else "Desconhecido"
            )

            lista.insert(
                tk.END,
                f"Fatura #{fatura.id} | Consulta #{fatura.id_consulta} | "
                f"{cliente} | {fatura.valor_total:.2f} € | {fatura.estado}"
            )

        detalhes.config(state="normal")
        detalhes.delete("1.0", tk.END)
        detalhes.config(state="disabled")

    def obter_selecionada():
        # Obter a fatura selecionada na lista.
        indices = lista.curselection()
        if not indices:
            return None
        return faturas[indices[0]]

    def selecionar_fatura(evento=None):
        # Preencher o estado e os detalhes da fatura selecionada.
        fatura = obter_selecionada()
        if fatura is None:
            return

        estado_var.set(fatura.estado)
        metodo_var.set(fatura.metodo_pagamento or "")

        linhas = [
            f"Fatura: #{fatura.id}",
            f"Consulta: #{fatura.id_consulta}",
            f"Valor: {fatura.valor_total:.2f} €",
            f"Estado: {fatura.estado}",
            f"Método de pagamento: {fatura.metodo_pagamento or '—'}",
            f"Data de pagamento: "
            f"{fatura.data_pagamento.strftime('%d-%m-%Y') if fatura.data_pagamento else '—'}"
        ]

        detalhes.config(state="normal")
        detalhes.delete("1.0", tk.END)
        detalhes.insert("1.0", "\n".join(linhas))
        detalhes.config(state="disabled")

    def emitir():
        # Validar e emitir uma fatura associada à consulta escolhida.
        descricao = consulta_var.get()

        if descricao not in opcoes_consulta:
            messagebox.showwarning(
                "Consulta obrigatória",
                "Selecione uma consulta.",
                parent=janela
            )
            return

        try:
            valor = float(
                entrada_valor.get().strip().replace(",", ".")
            )
            metodo = combo_metodo.get()
            metodo = None if metodo == "Pendente" else metodo

            fatura = controller.emitir(
                opcoes_consulta[descricao],
                valor,
                metodo
            )
        except (ValueError, TypeError, RuntimeError) as erro:
            mostrar_erro(erro)
            return

        messagebox.showinfo(
            "Fatura emitida",
            f"Fatura #{fatura.id} emitida com sucesso.",
            parent=janela
        )

        entrada_valor.delete(0, tk.END)
        combo_metodo.current(0)
        atualizar()

    def guardar_estado():
        # Guardar o novo estado da fatura selecionada.
        fatura = obter_selecionada()

        if fatura is None:
            messagebox.showwarning(
                "Seleção obrigatória",
                "Selecione uma fatura.",
                parent=janela
            )
            return

        estado = estado_var.get()
        metodo = metodo_var.get().strip() if estado == "Pago" else None

        if estado == "Anulada":
            confirmado = messagebox.askyesno(
                "Anular fatura",
                f"Deseja anular a fatura #{fatura.id}?",
                parent=janela
            )
            if not confirmado:
                return

        try:
            controller.atualizar_estado(fatura.id, estado, metodo)
        except (ValueError, TypeError, RuntimeError) as erro:
            mostrar_erro(erro)
            return

        messagebox.showinfo(
            "Estado atualizado",
            "O estado da fatura foi atualizado.",
            parent=janela
        )
        atualizar()

    def atualizar():
        # Recarregar os dados depois de cada operação.
        try:
            carregar_referencias()
            carregar_faturas()
        except (ValueError, TypeError, RuntimeError) as erro:
            mostrar_erro(erro)

    # Criar os botões e associar os eventos.
    quadro_botoes = ttk.Frame(janela)
    quadro_botoes.pack(fill="x", padx=12, pady=8)

    ttk.Button(
        quadro_botoes, text="Emitir Fatura", command=emitir
    ).pack(side="left", padx=5)

    ttk.Button(
        quadro_botoes, text="Guardar Estado", command=guardar_estado
    ).pack(side="left", padx=5)

    ttk.Button(
        quadro_botoes, text="Atualizar Lista", command=atualizar
    ).pack(side="left", padx=5)

    ttk.Button(
        quadro_botoes, text="Fechar", command=janela.destroy
    ).pack(side="right", padx=5)

    lista.bind("<<ListboxSelect>>", selecionar_fatura)

    atualizar()

    if pai is None:
        janela.mainloop()

    return janela
