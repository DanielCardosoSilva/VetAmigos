"""Controlo de acesso baseado em papéis (RBAC) do VetAmigos."""

from functools import wraps
import jwt


PERMISSOES = {
    "cliente": ("Proprietario", "Rececionista"),
    "animal": ("Proprietario", "Rececionista"),
    "consulta": ("Proprietario", "MedicoVeterinario", "Rececionista"),
    "vacina": ("Proprietario", "MedicoVeterinario"),
    "medicamento": ("Proprietario", "MedicoVeterinario"),
    "receita": ("Proprietario", "MedicoVeterinario"),
    "fatura": ("Proprietario", "Rececionista"),
    "relatorio": ("Proprietario",),
    "funcionario": ("Proprietario",),
}


def require_tipo(*tipos_permitidos):
    """Restringe a execução de uma função aos papéis autorizados."""

    # Validar a configuração do decorador antes da utilização.
    if not tipos_permitidos:
        raise ValueError("É necessário indicar pelo menos um papel permitido.")

    def decorator(funcao):
        # Preservar os metadados da função protegida.
        @wraps(funcao)
        def wrapper(token, *args, **kwargs):
            # Validar o JWT usando o módulo de sessões do David.
            from src.services.session import validar_token

            if not isinstance(token, str) or not token.strip():
                raise PermissionError(
                    "Não autenticado. É necessário iniciar sessão."
                )

            try:
                payload = validar_token(token)
            except jwt.ExpiredSignatureError as erro:
                raise PermissionError(
                    "Sessão expirada. Inicie sessão novamente."
                ) from erro
            except jwt.InvalidTokenError as erro:
                raise PermissionError(
                    "Sessão inválida. Inicie sessão novamente."
                ) from erro

            if not isinstance(payload, dict):
                raise PermissionError("Sessão inválida.")

            tipo = payload.get("tipo")

            if tipo not in tipos_permitidos:
                raise PermissionError(
                    "Acesso negado. Não tem permissões "
                    "para executar esta operação."
                )

            return funcao(token, *args, **kwargs)

        return wrapper

    return decorator


def require_modulo(modulo):
    """Protege uma operação segundo as permissões do módulo."""

    # Consultar a matriz de permissões da aplicação.
    if modulo not in PERMISSOES:
        raise ValueError(f"Módulo desconhecido: {modulo}")

    return require_tipo(*PERMISSOES[modulo])
