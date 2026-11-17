"""
Ponto de entrada principal da aplicação em modo gráfico (Tkinter).
"""
import tkinter as tk
from db.connection import inicializar_bd
from main import construir_controllers
from src.views.login_view_gui import LoginViewGUI
from src.views.menu_view_gui import MenuViewGUI

def iniciar_aplicacao():
    """Inicializa a base de dados, constrói os controllers e inicia o ciclo gráfico."""
    inicializar_bd()
    controllers = construir_controllers()
    
    root = tk.Tk()
    
    def alternar_para_login():
        """Limpa a janela atual e apresenta o ecrã de login."""
        for widget in root.winfo_children():
            widget.destroy()
        LoginViewGUI(root, controllers["auth"], lambda funcionario: alternar_para_menu(funcionario))
        
    def alternar_para_menu(funcionario):
        """Limpa a janela de login e apresenta o menu principal correspondente ao perfil."""
        for widget in root.winfo_children():
            widget.destroy()
        MenuViewGUI(root, funcionario, controllers, on_logout=alternar_para_login)
        
    # Iniciar aplicação mostrando o login
    alternar_para_login()
    root.mainloop()

if __name__ == "__main__":
    iniciar_aplicacao()