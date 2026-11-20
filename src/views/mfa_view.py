"""src/views/mfa_view.py - Verificação e configuração MFA (TOTP) em consola."""

from src.models.proprietario import Proprietario


def validar_mfa_proprietario(funcionario, auth_controller) -> bool:
    """Garante a verificação MFA TOTP quando o utilizador autenticado é Proprietário."""
    if not isinstance(funcionario, Proprietario):
        return True

    utilizador = funcionario.nome_utilizador
    segredo_existente = getattr(funcionario, "mfa_secret", None)

    if not segredo_existente:
        print("\n========== CONFIGURAÇÃO MFA (PROPRIETÁRIO) ==========")
        dados_mfa = auth_controller.configurar_mfa(utilizador)
        funcionario.mfa_secret = dados_mfa["secret"]
        print(f"Chave secreta TOTP (Base32): {dados_mfa['secret']}")
        print(f"URI de autenticação: {dados_mfa['uri']}")
        print("Adicione esta chave ou URI na sua app autenticadora (ex.: Google Authenticator / Authy).")

    while True:
        codigo = input("Introduza o código MFA de 6 dígitos (ou 0 para cancelar): ").strip()
        if codigo == "0":
            print("Verificação MFA cancelada.")
            return False

        if auth_controller.verificar_mfa(utilizador, codigo):
            print("Verificação MFA concluída com sucesso.")
            return True

        print("Código MFA inválido ou expirado. Tente novamente.")