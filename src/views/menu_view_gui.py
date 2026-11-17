"""
Módulo de Menu Principal GUI (Tkinter) VetAmigos.
"""
import tkinter as tk
from tkinter import messagebox

class MenuViewGUI:
    """Janela do menu principal adaptada ao perfil do funcionário autenticado."""
    
    def __init__(self, root, funcionario, controllers, on_logout):
        self.root = root
        self.funcionario = funcionario
        self.controllers = controllers
        self.on_logout = on_logout
        
        self.root.title(f"VetAmigos - Menu Principal ({funcionario.nome})")
        self.root.geometry("650x520")
        self.root.resizable(False, False)
        
        self._criar_widgets()

    def _criar_widgets(self):
        """Cria a interface do menu principal com controlo de acesso visual por perfil."""
        # Barra superior com informações e botão de Terminar Sessão (T1.5)
        frame_topo = tk.Frame(self.root, bg="#1976D2", height=60)
        frame_topo.pack(fill="x", side="top")
        
        lbl_info = tk.Label(
            frame_topo, text=f"Utilizador: {getattr(self.funcionario, 'nome', 'Funcionário')}", 
            bg="#1976D2", fg="white", font=("Arial", 11, "bold")
        )
        lbl_info.pack(side="left", padx=20, pady=15)
        
        # Botão Terminar Sessão (T1.5)
        btn_logout = tk.Button(
            frame_topo, text="Terminar Sessão", bg="#D32F2F", fg="white", 
            font=("Arial", 10, "bold"), command=self.terminar_sessao
        )
        btn_logout.pack(side="right", padx=20, pady=12)
        
        # Frame central para os módulos (T1.3)
        frame_centro = tk.LabelFrame(
            self.root, text=" Módulos Disponíveis ", font=("Arial", 12, "bold"), padx=20, pady=20
        )
        frame_centro.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Obter permissões baseadas no perfil do utilizador logado
        permissoes = self._obter_permissoes_por_perfil()
        
        # Lista de módulos do sistema: (Texto do Botão, Função de Abertura, Chave de Permissão)
        modulos = [
            ("Gerir Clientes", self.abrir_clientes, "cliente"),
            ("Gerir Animais", self.abrir_animais, "animal"),
            ("Gerir Consultas", self.abrir_consultas, "consulta"),
            ("Gerir Vacinação", self.abrir_vacinacao, "vacina"),
            ("Gerir Medicamentos", self.abrir_medicamentos, "medicamento"),
            ("Gerir Receitas", self.abrir_receitas, "receita"),
            ("Gerir Faturas", self.abrir_faturas, "fatura"),
            ("Consultar Relatórios", self.abrir_relatorios, "relatorio"),
            ("Gerir Funcionários", self.abrir_funcionarios, "funcionario")
        ]
        
        # Posicionar botões em grelha (Grid) com controlo de acesso visual (T1.4)
        row, col = 0, 0
        for texto, comando, chave in modulos:
            permitido = permissoes.get(chave, False)
            
            # Controlo de acesso visual (T1.4): desativar botões não permitidos (state=DISABLED)
            estado = "normal" if permitido else "disabled"
            cor_bg = "#4CAF50" if permitido else "#E0E0E0"
            cor_fg = "white" if permitido else "#9E9E9E"
            
            btn = tk.Button(
                frame_centro, text=texto, command=comando, 
                font=("Arial", 10, "bold"), width=20, height=2,
                bg=cor_bg, fg=cor_fg, state=estado
            )
            btn.grid(row=row, column=col, padx=12, pady=12)
            
            col += 1
            if col > 2:
                col = 0
                row += 1

    def _obter_permissoes_por_perfil(self):
        """Define quais módulos estão ativos para o perfil atual com base na matriz de regras do projeto."""
        tipo_func = type(self.funcionario).__name__
        
        if "Rececionista" in tipo_func:
            return {
                "cliente": True, "animal": True, "consulta": True, 
                "vacina": False, "medicamento": False, "receita": False, 
                "fatura": True, "relatorio": False, "funcionario": False
            }
        elif "MedicoVeterinario" in tipo_func:
            return {
                "cliente": False, "animal": True, "consulta": True, 
                "vacina": True, "medicamento": True, "receita": True, 
                "fatura": False, "relatorio": False, "funcionario": False
            }
        elif "Proprietario" in tipo_func:
            return {
                "cliente": False, "animal": True, "consulta": True, 
                "vacina": True, "medicamento": False, "receita": True, 
                "fatura": True, "relatorio": True, "funcionario": False
            }
        else:
            # Administrador / Acesso Total por predefinição
            return {
                "cliente": True, "animal": True, "consulta": True, 
                "vacina": True, "medicamento": True, "receita": True, 
                "fatura": True, "relatorio": True, "funcionario": True
            }

    def terminar_sessao(self):
        """Fecha a janela do menu principal e reabre a janela de login (T1.5)."""
        if messagebox.askyesno("Terminar Sessão", "Tem certeza que deseja terminar a sessão?"):
            self.root.destroy()
            self.on_logout()

    def abrir_clientes(self):
        messagebox.showinfo("Navegação", "A abrir Módulo de Clientes (Daniel)")

    def abrir_animais(self):
        messagebox.showinfo("Navegação", "A abrir Módulo de Animais (Daniel)")

    def abrir_consultas(self):
        messagebox.showinfo("Navegação", "A abrir Módulo de Consultas (David)")

    def abrir_vacinacao(self):
        messagebox.showinfo("Navegação", "A abrir Módulo de Vacinação (David)")

    def abrir_medicamentos(self):
        messagebox.showinfo("Navegação", "A abrir Módulo de Medicamentos")

    def abrir_receitas(self):
        messagebox.showinfo("Navegação", "A abrir Módulo de Receitas")

    def abrir_faturas(self):
        messagebox.showinfo("Navegação", "A abrir Módulo de Faturas (Regina)")

    def abrir_relatorios(self):
        messagebox.showinfo("Navegação", "A abrir Painel de Relatórios (Regina)")

    def abrir_funcionarios(self):
        messagebox.showinfo("Navegação", "A abrir Gestão de Funcionários")