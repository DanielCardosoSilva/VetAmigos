"""Controlador de auth."""


class AuthController:
    """Controlador responsável pela autenticação e MFA."""

    def __init__(self, auth_service):
        """Inicializa o controlador com o serviço de autenticação."""
        self.service = auth_service

    def iniciar_sessao(self, utilizador, palavra_passe):
        """Autentica o utilizador através do serviço."""
        return self.service.iniciar_sessao(utilizador, palavra_passe)

    def registar(self, nome, utilizador, senha, tipo, cedula=None):
        """Regista um funcionário com palavra-passe protegida por bcrypt."""
        return self.service.registar(nome, utilizador, senha, tipo, cedula)

    def configurar_mfa(self, nome_utilizador):
        """Gera e guarda o segredo TOTP para o utilizador."""
        return self.service.configurar_mfa(nome_utilizador)

    def verificar_mfa(self, nome_utilizador, codigo):
        """Verifica o código TOTP introduzido pelo utilizador."""
        return self.service.verificar_mfa(nome_utilizador, codigo)