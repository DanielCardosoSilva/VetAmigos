"""Controlador de auth."""
class AuthController:
    def __init__(self, funcionario_service):
        self.service = funcionario_service
    def iniciar_sessao(self, utilizador, palavra_passe):
        return self.service.iniciar_sessao(utilizador, palavra_passe)
