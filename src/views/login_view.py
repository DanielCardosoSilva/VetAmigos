"""Vista CLI de login."""
from getpass import getpass
from src.views.common_view import texto

def iniciar_sessao(controller):
    while True:
        print("\n========== INICIAR SESSÃO ==========")
        print("Introduza 0 no nome de utilizador para sair.")
        utilizador = texto("Nome de utilizador: ")
        if utilizador == "0":
            return None
        try:
            funcionario = controller.iniciar_sessao(utilizador, getpass("Palavra-passe: "))
            print(f"Bem-vindo(a), {funcionario.nome}!")
            return funcionario
        except ValueError as erro:
            print(f"Erro: {erro}")
