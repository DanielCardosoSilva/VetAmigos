"""Interface gráfica de gestão de animais."""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class AnimalViewGUI:
    def __init__(self, parent, animal_controller, cliente_controller):
        # Guarda os controllers e inicializa a janela de animais.
        self.controller = animal_controller
        self.cliente_controller = cliente_controller
        self.animais = []
        self.donos = {}
        self.selecionado = None
        self.janela = tk.Toplevel(parent) if parent is not None else tk.Tk()
        self.janela.title("VetAmigos - Animais")
        self.janela.geometry("900x520")
        self.campos = {nome: tk.StringVar(master=self.janela) for nome in ("nome", "especie", "data_nasc", "peso_animal")}
        self.dono = tk.StringVar(master=self.janela)
        self.mostrar_arquivados = tk.BooleanVar(master=self.janela)
        self.criar_interface()
        self.carregar()

    def criar_interface(self):
        # Organiza a lista de animais e o formulário de registo.
        painel = ttk.Frame(self.janela, padding=15)
        painel.pack(fill="both", expand=True)
        ttk.Label(painel, text="Gestão de Animais", font=("Arial", 17, "bold")).pack(anchor="w", pady=(0, 12))
        conteudo = ttk.Frame(painel)
        conteudo.pack(fill="both", expand=True)
        esquerda = ttk.LabelFrame(conteudo, text="Lista de Animais", padding=10)
        esquerda.pack(side="left", fill="both", expand=True, padx=(0, 10))
        direita = ttk.LabelFrame(conteudo, text="Dados do Animal", padding=10)
        direita.pack(side="left", fill="both", expand=True)
        lista_frame = ttk.Frame(esquerda)
        lista_frame.pack(fill="both", expand=True)
        self.lista = tk.Listbox(lista_frame, exportselection=False)
        self.lista.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(lista_frame, orient="vertical", command=self.lista.yview)
        scrollbar.pack(side="right", fill="y")
        self.lista.configure(yscrollcommand=scrollbar.set)
        self.lista.bind("<<ListboxSelect>>", self.selecionar)
        ttk.Checkbutton(esquerda, text="Mostrar arquivados", variable=self.mostrar_arquivados,
                        command=self.carregar).pack(anchor="w", pady=8)
        ttk.Button(esquerda, text="Atualizar lista", command=self.carregar).pack(fill="x")
        for linha, (campo, titulo) in enumerate((("nome", "Nome"), ("especie", "Espécie"),
                                                 ("data_nasc", "Nascimento (dd-mm-aaaa)"),
                                                 ("peso_animal", "Peso (kg)"))):
            ttk.Label(direita, text=titulo).grid(row=linha, column=0, sticky="w", pady=7)
            ttk.Entry(direita, textvariable=self.campos[campo], width=28).grid(
                row=linha, column=1, sticky="ew", padx=8, pady=7)
        ttk.Label(direita, text="Proprietário").grid(row=4, column=0, sticky="w", pady=7)
        self.combo = ttk.Combobox(direita, textvariable=self.dono, state="readonly")
        self.combo.grid(row=4, column=1, sticky="ew", padx=8, pady=7)
        direita.columnconfigure(1, weight=1)
        botoes = ttk.Frame(direita)
        botoes.grid(row=5, column=0, columnspan=2, pady=20, sticky="w")
        ttk.Button(botoes, text="Novo", command=self.novo).pack(side="left", padx=3)
        ttk.Button(botoes, text="Guardar", command=self.guardar).pack(side="left", padx=3)
        ttk.Button(botoes, text="Editar", command=self.editar).pack(side="left", padx=3)
        self.botao_estado = ttk.Button(botoes, text="Arquivar", command=self.alterar_estado)
        self.botao_estado.pack(side="left", padx=3)

    def carregar(self):
        # Atualiza as opções de proprietários e a lista de animais.
        try:
            clientes = self.cliente_controller.listar()
            self.donos = {f"{c.nome} | {c.nif}": c.nif for c in clientes if c.ativo}
            self.combo["values"] = list(self.donos)
            self.animais = [a for a in self.controller.listar() if bool(a.ativo) != self.mostrar_arquivados.get()]
            self.lista.delete(0, tk.END)
            for animal in self.animais:
                self.lista.insert(tk.END, f"{animal.id} | {animal.nome} ({animal.especie})")
            self.novo()
        except Exception as erro:
            messagebox.showerror("Erro", str(erro), parent=self.janela)

    def selecionar(self, evento=None):
        # Mostra os dados do animal selecionado sem alterar o seu ID.
        indices = self.lista.curselection()
        if not indices:
            return
        self.selecionado = self.animais[indices[0]]
        self.campos["nome"].set(self.selecionado.nome)
        self.campos["especie"].set(self.selecionado.especie)
        self.campos["data_nasc"].set(self.selecionado.data_nasc.strftime("%d-%m-%Y"))
        self.campos["peso_animal"].set(str(self.selecionado.peso_animal))
        self.dono.set(next((op for op, nif in self.donos.items() if nif == self.selecionado.nif_cliente), ""))
        self.botao_estado.configure(text="Reativar" if not self.selecionado.ativo else "Arquivar")

    def novo(self):
        # Limpa os campos para registar um novo animal.
        self.selecionado = None
        self.lista.selection_clear(0, tk.END)
        for variavel in self.campos.values():
            variavel.set("")
        self.dono.set("")
        self.botao_estado.configure(text="Arquivar")

    def dados_formulario(self):
        # Converte nascimento e peso nos tipos esperados pelo service.
        try:
            texto = self.campos["data_nasc"].get().strip()
            nascimento = datetime.strptime(texto, "%d-%m-%Y").date()
            if nascimento.strftime("%d-%m-%Y") != texto:
                raise ValueError
        except ValueError:
            raise ValueError("A data deve ter o formato dd-mm-aaaa.") from None
        try:
            peso = float(self.campos["peso_animal"].get().replace(",", "."))
        except ValueError:
            raise ValueError("O peso deve ser numérico.") from None
        if self.dono.get() not in self.donos:
            raise ValueError("Seleciona um proprietário ativo.")
        return (self.campos["nome"].get(), self.campos["especie"].get(),
                nascimento, peso, self.donos[self.dono.get()])

    def guardar(self):
        # Regista o animal usando o controller existente.
        if self.selecionado is not None:
            messagebox.showwarning("Atenção", "Usa Editar para guardar alterações.", parent=self.janela)
            return
        try:
            self.controller.registar(*self.dados_formulario())
            self.carregar()
            messagebox.showinfo("Sucesso", "Animal registado.", parent=self.janela)
        except Exception as erro:
            messagebox.showerror("Erro", str(erro), parent=self.janela)

    def editar(self):
        # Atualiza o animal selecionado através do controller.
        if self.selecionado is None:
            messagebox.showwarning("Atenção", "Seleciona um animal.", parent=self.janela)
            return
        try:
            self.controller.atualizar(self.selecionado.id, *self.dados_formulario())
            self.carregar()
            messagebox.showinfo("Sucesso", "Animal atualizado.", parent=self.janela)
        except Exception as erro:
            messagebox.showerror("Erro", str(erro), parent=self.janela)

    def alterar_estado(self):
        # Arquiva ou reativa o animal preservando todas as consultas e vacinas.
        if self.selecionado is None:
            messagebox.showwarning("Atenção", "Seleciona um animal.", parent=self.janela)
            return
        ativo = not self.selecionado.ativo
        acao = "reativar" if ativo else "arquivar"
        if not messagebox.askyesno("Confirmar", f"Queres {acao} este animal?", parent=self.janela):
            return
        try:
            self.controller.definir_ativo(self.selecionado.id, ativo)
            self.carregar()
            messagebox.showinfo("Sucesso", f"Animal {'reativado' if ativo else 'arquivado'}.", parent=self.janela)
        except Exception as erro:
            messagebox.showerror("Erro", str(erro), parent=self.janela)


def abrir(animal_controller, cliente_controller, parent=None):
    # Abre a janela a partir do menu gráfico.
    vista = AnimalViewGUI(parent, animal_controller, cliente_controller)
    if parent is None:
        vista.janela.mainloop()
    return vista
