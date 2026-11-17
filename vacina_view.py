"""Vista CLI de vacina."""
from datetime import date
from src.views.common_view import menu, texto, inteiro, data, mostrar

def abrir(controller):
    def registar():
        animal = inteiro("ID do animal: ")
        nome = texto("Vacina: ")
        administracao = data("Data de administração")
        proxima_texto = texto("Próxima dose (AAAA-MM-DD, vazio se não aplicável): ")
        proxima = date.fromisoformat(proxima_texto) if proxima_texto else None
        registo = controller.registar(animal, nome, administracao, proxima)
        print(f"Vacina registada com ID {registo.id}.")
    menu("Gerir vacinação", {"1": ("Registar vacina", registar), "2": ("Histórico por animal", lambda: mostrar(controller.historico(inteiro("ID do animal: ")))), "3": ("Próximas doses em atraso", lambda: mostrar(controller.atrasadas()))})

    # ---------- T3.3: Janela Gestão de Vacinação ----------
    janela = tk.Tk()
    janela.title("Gestão de Vacinação")

    # Lista de registos de vacinas do animal selecionado
    quadro_lista = tk.LabelFrame(janela, text="Registos de vacinas")
    quadro_lista.pack(fill="both", expand=True, padx=10, pady=5)
    barra = tk.Scrollbar(quadro_lista)
    barra.pack(side="right", fill="y")
    lista = tk.Listbox(quadro_lista, width=70, height=10, yscrollcommand=barra.set)
    lista.pack(side="left", fill="both", expand=True)
    barra.config(command=lista.yview)

    # Formulário: Combobox (animal), Entry (vacina/lote, data de aplicação, próxima dose)
    quadro_form = tk.LabelFrame(janela, text="Nova vacina")
    quadro_form.pack(fill="x", padx=10, pady=5)

    tk.Label(quadro_form, text="Animal:").grid(row=0, column=0, sticky="w", padx=5, pady=3)
    combo_animal = ttk.Combobox(quadro_form, state="readonly", width=40,
                                values=[f"{a.id} - {a.nome}" for a in controller.animais()])
    combo_animal.grid(row=0, column=1, padx=5, pady=3)
    combo_animal.bind("<<ComboboxSelected>>", lambda e: (
        lista.delete(0, "end"),
        [lista.insert("end", f"{r.nome} | Aplicada: {r.data_administracao:%d-%m-%Y} | "
                             f"Próxima: {r.proxima_dose:%d-%m-%Y}" if r.proxima_dose else
                             f"{r.nome} | Aplicada: {r.data_administracao:%d-%m-%Y} | Próxima: —")
        for r in controller.historico(int(combo_animal.get().split(" - ")[0]))]))

    tk.Label(quadro_form, text="Vacina/lote:").grid(row=1, column=0, sticky="w", padx=5, pady=3)
    entrada_vacina = tk.Entry(quadro_form, width=43)
    entrada_vacina.grid(row=1, column=1, padx=5, pady=3)

    tk.Label(quadro_form, text="Data de aplicação:").grid(row=2, column=0, sticky="w", padx=5, pady=3)
    entrada_aplicacao = tk.Entry(quadro_form, width=43)
    entrada_aplicacao.grid(row=2, column=1, padx=5, pady=3)

    tk.Label(quadro_form, text="Próxima dose:").grid(row=3, column=0, sticky="w", padx=5, pady=3)
    entrada_proxima = tk.Entry(quadro_form, width=43)
    entrada_proxima.grid(row=3, column=1, padx=5, pady=3)

    janela.mainloop()