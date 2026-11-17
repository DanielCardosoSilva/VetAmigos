"""Interface gráfica de gestão de clientes."""
import tkinter as tk
from tkinter import ttk, messagebox


class ClienteViewGUI:
    def __init__(self, parent, controller):
        # Prepara a janela e conserva o controller fornecido pelo menu.
        self.controller = controller
        self.clientes = []
        self.selecionado = None
        self.janela = tk.Toplevel(parent) if parent is not None else tk.Tk()
        self.janela.title("VetAmigos - Clientes")
        self.janela.geometry("850x480")
        self.campos = {nome: tk.StringVar(master=self.janela) for nome in ("nome", "nif", "telefone", "email")}
        self.mostrar_arquivados = tk.BooleanVar(master=self.janela)
        self.criar_interface()
        self.carregar()

    def criar_interface(self):
        # Organiza a lista e o formulário em dois painéis.
        painel = ttk.Frame(self.janela, padding=15)
        painel.pack(fill="both", expand=True)
        ttk.Label(painel, text="Gestão de Clientes", font=("Arial", 17, "bold")).pack(anchor="w", pady=(0, 12))
        conteudo = ttk.Frame(painel)
        conteudo.pack(fill="both", expand=True)
        esquerda = ttk.LabelFrame(conteudo, text="Lista de Clientes", padding=10)
        esquerda.pack(side="left", fill="both", expand=True, padx=(0, 10))
        direita = ttk.LabelFrame(conteudo, text="Dados do Cliente", padding=10)
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
        for linha, (campo, titulo) in enumerate((("nome", "Nome"), ("nif", "NIF"),
                                                 ("telefone", "Telefone"), ("email", "Email"))):
            ttk.Label(direita, text=titulo).grid(row=linha, column=0, sticky="w", pady=7)
            entrada = ttk.Entry(direita, textvariable=self.campos[campo], width=35)
            entrada.grid(row=linha, column=1, sticky="ew", padx=8, pady=7)
            if campo == "nif":
                self.entrada_nif = entrada
        direita.columnconfigure(1, weight=1)
        botoes = ttk.Frame(direita)
        botoes.grid(row=4, column=0, columnspan=2, pady=20, sticky="w")
        ttk.Button(botoes, text="Novo", command=self.novo).pack(side="left", padx=3)
        ttk.Button(botoes, text="Guardar", command=self.guardar).pack(side="left", padx=3)
        ttk.Button(botoes, text="Editar", command=self.editar).pack(side="left", padx=3)
        self.botao_estado = ttk.Button(botoes, text="Arquivar", command=self.alterar_estado)
        self.botao_estado.pack(side="left", padx=3)

    def carregar(self):
        # Recarrega os clientes e aplica o filtro de arquivo.
        try:
            todos = self.controller.listar()
            self.clientes = [c for c in todos if bool(c.ativo) != self.mostrar_arquivados.get()]
            self.lista.delete(0, tk.END)
            for cliente in self.clientes:
                self.lista.insert(tk.END, f"{cliente.nome} | {cliente.nif}")
            self.novo()
        except Exception as erro:
            messagebox.showerror("Erro", str(erro), parent=self.janela)

    def selecionar(self, evento=None):
        # Preenche os campos com o cliente selecionado.
        indices = self.lista.curselection()
        if not indices:
            return
        self.selecionado = self.clientes[indices[0]]
        for campo, variavel in self.campos.items():
            variavel.set(getattr(self.selecionado, campo))
        self.entrada_nif.configure(state="readonly")
        self.botao_estado.configure(text="Reativar" if not self.selecionado.ativo else "Arquivar")

    def novo(self):
        # Limpa a seleção para criar um cliente sem alterar o NIF de outro.
        self.selecionado = None
        self.lista.selection_clear(0, tk.END)
        self.entrada_nif.configure(state="normal")
        for variavel in self.campos.values():
            variavel.set("")
        self.botao_estado.configure(text="Arquivar")

    def guardar(self):
        # Regista um cliente novo recorrendo às validações do service.
        if self.selecionado is not None:
            messagebox.showwarning("Atenção", "Usa Editar para guardar alterações.", parent=self.janela)
            return
        try:
            self.controller.registar(*(self.campos[c].get().strip() for c in ("nome", "nif", "telefone", "email")))
            self.carregar()
            messagebox.showinfo("Sucesso", "Cliente registado.", parent=self.janela)
        except Exception as erro:
            messagebox.showerror("Erro", str(erro), parent=self.janela)

    def editar(self):
        # Guarda apenas os campos editáveis do cliente selecionado.
        if self.selecionado is None:
            messagebox.showwarning("Atenção", "Seleciona um cliente.", parent=self.janela)
            return
        try:
            self.controller.atualizar(self.selecionado.nif, self.campos["nome"].get(),
                                      self.campos["telefone"].get(), self.campos["email"].get())
            self.carregar()
            messagebox.showinfo("Sucesso", "Cliente atualizado.", parent=self.janela)
        except Exception as erro:
            messagebox.showerror("Erro", str(erro), parent=self.janela)

    def alterar_estado(self):
        # Arquiva ou reativa sem apagar as relações da base de dados.
        if self.selecionado is None:
            messagebox.showwarning("Atenção", "Seleciona um cliente.", parent=self.janela)
            return
        ativo = not self.selecionado.ativo
        acao = "reativar" if ativo else "arquivar"
        if not messagebox.askyesno("Confirmar", f"Queres {acao} este cliente?", parent=self.janela):
            return
        try:
            self.controller.definir_ativo(self.selecionado.nif, ativo)
            self.carregar()
            messagebox.showinfo("Sucesso", f"Cliente {'reativado' if ativo else 'arquivado'}.", parent=self.janela)
        except Exception as erro:
            messagebox.showerror("Erro", str(erro), parent=self.janela)


def abrir(controller, parent=None):
    # Permite abrir esta view a partir do menu principal.
    vista = ClienteViewGUI(parent, controller)
    if parent is None:
        vista.janela.mainloop()
    return vista
