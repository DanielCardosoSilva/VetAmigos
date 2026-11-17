"""Vista gráfica de relatórios."""

import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog


def abrir(controller, pai=None):
    # Criar a janela gráfica de relatórios.
    janela = tk.Toplevel(pai) if pai is not None else tk.Tk()
    janela.title("VetAmigos - Relatórios")
    janela.geometry("850x680")
    janela.minsize(700, 550)

    periodo_var = tk.StringVar(value="Mês")
    dados_atuais = None

    # Criar os filtros por período.
    quadro_filtros = ttk.LabelFrame(janela, text="Filtros de Relatório")
    quadro_filtros.pack(fill="x", padx=12, pady=10)

    ttk.Label(quadro_filtros, text="Período:").pack(
        side="left", padx=8, pady=10
    )

    combo_periodo = ttk.Combobox(
        quadro_filtros,
        textvariable=periodo_var,
        state="readonly",
        values=["Hoje", "Semana", "Mês", "Ano"],
        width=18
    )
    combo_periodo.pack(side="left", padx=8, pady=10)

    # Criar o painel de indicadores.
    quadro_resumo = ttk.LabelFrame(janela, text="Resumo")
    quadro_resumo.pack(fill="x", padx=12, pady=10)

    indicadores = [
        ("Clientes registados", "clientes"),
        ("Consultas no período", "consultas"),
        ("Consultas canceladas", "canceladas"),
        ("Total faturado (€)", "faturado"),
        ("Recebido (€)", "recebido"),
        ("Pendente (€)", "pendente")
    ]

    valores = {}

    for indice, (titulo, chave) in enumerate(indicadores):
        # Construir cada indicador com um valor destacado.
        linha = indice // 3
        coluna = indice % 3

        quadro = ttk.Frame(quadro_resumo, padding=12)
        quadro.grid(
            row=linha, column=coluna,
            sticky="nsew", padx=5, pady=8
        )

        ttk.Label(
            quadro, text=titulo, anchor="center"
        ).pack(fill="x")

        valor = ttk.Label(
            quadro,
            text="—",
            font=("Arial", 21, "bold"),
            anchor="center"
        )
        valor.pack(fill="x", pady=5)
        valores[chave] = valor

    for coluna in range(3):
        quadro_resumo.columnconfigure(coluna, weight=1)

    # Criar o painel de consultas por veterinário.
    quadro_medicos = ttk.LabelFrame(
        janela, text="Consultas por Médico Veterinário"
    )
    quadro_medicos.pack(
        fill="both", expand=True, padx=12, pady=10
    )

    area_lista = ttk.Frame(quadro_medicos)
    area_lista.pack(fill="both", expand=True, padx=8, pady=8)

    barra = ttk.Scrollbar(area_lista)
    barra.pack(side="right", fill="y")

    lista_medicos = tk.Listbox(
        area_lista,
        height=8,
        yscrollcommand=barra.set
    )
    lista_medicos.pack(side="left", fill="both", expand=True)
    barra.config(command=lista_medicos.yview)

    texto_periodo = ttk.Label(
        janela, text="", anchor="center"
    )
    texto_periodo.pack(fill="x", padx=12, pady=5)

    def atualizar():
        # Obter e apresentar os indicadores do período selecionado.
        nonlocal dados_atuais

        try:
            dados = controller.por_periodo(periodo_var.get())
        except (ValueError, TypeError, RuntimeError) as erro:
            messagebox.showerror(
                "Relatórios", str(erro), parent=janela
            )
            return

        dados_atuais = dados

        for chave, etiqueta in valores.items():
            valor = dados[chave]

            if chave in ("faturado", "recebido", "pendente"):
                etiqueta.config(text=f"{valor:,.2f} €")
            else:
                etiqueta.config(text=str(valor))

        lista_medicos.delete(0, tk.END)

        for cedula, total in sorted(dados["por_medico"].items()):
            lista_medicos.insert(
                tk.END,
                f"Cédula {cedula}: {total} consulta(s)"
            )

        if not dados["por_medico"]:
            lista_medicos.insert(
                tk.END, "Sem consultas no período selecionado."
            )

        texto_periodo.config(
            text=(
                f"Período: {dados['inicio']:%d-%m-%Y} "
                f"a {dados['fim']:%d-%m-%Y}"
            )
        )

    def exportar_csv():
        # Confirmar a exportação e guardar os indicadores em CSV.
        if dados_atuais is None:
            messagebox.showwarning(
                "Sem dados",
                "Atualize o relatório antes de exportar.",
                parent=janela
            )
            return

        if not messagebox.askyesno(
            "Exportar CSV",
            "Deseja exportar o relatório atual para CSV?",
            parent=janela
        ):
            return

        caminho = filedialog.asksaveasfilename(
            parent=janela,
            title="Guardar relatório CSV",
            defaultextension=".csv",
            filetypes=[("Ficheiros CSV", "*.csv")],
            initialfile=(
                f"relatorio_vetamigos_{periodo_var.get().lower()}.csv"
            )
        )

        if not caminho:
            return

        try:
            with open(
                caminho, "w", newline="", encoding="utf-8-sig"
            ) as ficheiro:
                escritor = csv.writer(ficheiro, delimiter=";")

                escritor.writerow(["VetAmigos - Relatório"])
                escritor.writerow(["Período", dados_atuais["periodo"]])
                escritor.writerow([
                    "Início", dados_atuais["inicio"].isoformat()
                ])
                escritor.writerow([
                    "Fim", dados_atuais["fim"].isoformat()
                ])
                escritor.writerow([])

                escritor.writerow(["Indicador", "Valor"])
                escritor.writerow([
                    "Clientes registados", dados_atuais["clientes"]
                ])
                escritor.writerow([
                    "Consultas", dados_atuais["consultas"]
                ])
                escritor.writerow([
                    "Consultas canceladas", dados_atuais["canceladas"]
                ])
                escritor.writerow([
                    "Total faturado (€)",
                    f"{dados_atuais['faturado']:.2f}"
                ])
                escritor.writerow([
                    "Recebido (€)",
                    f"{dados_atuais['recebido']:.2f}"
                ])
                escritor.writerow([
                    "Pendente (€)",
                    f"{dados_atuais['pendente']:.2f}"
                ])

                escritor.writerow([])
                escritor.writerow([
                    "Cédula profissional", "Número de consultas"
                ])

                for cedula, total in sorted(
                    dados_atuais["por_medico"].items()
                ):
                    escritor.writerow([cedula, total])

        except OSError as erro:
            messagebox.showerror(
                "Erro na exportação", str(erro), parent=janela
            )
            return

        messagebox.showinfo(
            "Exportação concluída",
            "O relatório CSV foi guardado com sucesso.",
            parent=janela
        )

    # Criar os botões de atualização, exportação e saída.
    quadro_botoes = ttk.Frame(janela)
    quadro_botoes.pack(fill="x", padx=12, pady=12)

    ttk.Button(
        quadro_botoes, text="Atualizar", command=atualizar
    ).pack(side="left", padx=5)

    ttk.Button(
        quadro_botoes, text="Exportar CSV", command=exportar_csv
    ).pack(side="left", padx=5)

    ttk.Button(
        quadro_botoes, text="Fechar", command=janela.destroy
    ).pack(side="right", padx=5)

    atualizar()

    if pai is None:
        janela.mainloop()

    return janela
