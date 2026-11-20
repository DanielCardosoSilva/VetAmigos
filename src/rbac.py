"""Controlo de acesso baseado em papéis"""

from functools import wraps

import jwt

from src.repositories.funcionario_repository import FuncionarioRepository
from src.services.session import validar_token


PERMISSOES = {
    "cliente": ("Proprietario", "Rececionista"),
    "animal": ("Proprietario", "Rececionista"),
    "consulta": (
        "Proprietario", "MedicoVeterinario", "Rececionista"
    ),
    "vacina": ("Proprietario", "MedicoVeterinario"),
    "medicamento": ("Proprietario", "MedicoVeterinario"),
    "receita": ("Proprietario", "MedicoVeterinario"),
    "fatura": ("Proprietario", "Rececionista"),
    "relatorio": ("Proprietario",),
    "funcionario": ("Proprietario",)
}


def autorizar_tipo(token, *tipos_permitidos):
    """Valida a sessão, o funcionário ativo e as permissões."""
    if not token:
        raise PermissionError(
            "Não autenticado. Inicie sessão."
        )

    try:
        dados = validar_token(token)
    except jwt.ExpiredSignatureError as erro:
        raise PermissionError(
            "Sessão expirada. Inicie sessão novamente."
        ) from erro
    except jwt.InvalidTokenError as erro:
        raise PermissionError(
            "Sessão inválida. Inicie sessão novamente."
        ) from erro

    funcionario = FuncionarioRepository().obter_por_nome_utilizador(
        dados["sub"]
    )

    if funcionario is None or not funcionario.ativo:
        raise PermissionError("Conta inexistente ou desativada.")

    if funcionario.tipo != dados["tipo"]:
        raise PermissionError("O perfil da sessão não é válido.")

    if funcionario.tipo not in tipos_permitidos:
        raise PermissionError(
            "Acesso negado. Não tem permissões para esta operação."
        )

    return dados


def autorizar_modulo(token, modulo):
    """Autoriza o acesso a um módulo segundo a matriz RBAC."""
    if modulo not in PERMISSOES:
        raise PermissionError("Módulo não autorizado.")

    return autorizar_tipo(token, *PERMISSOES[modulo])


def require_tipo(*tipos_permitidos):
    """Cria um decorador para proteger funções com JWT."""
    if not tipos_permitidos:
        raise ValueError("Indique pelo menos um perfil.")

    def decorator(funcao):
        # Preservar os metadados da função protegida.
        @wraps(funcao)
        def wrapper(token, *args, **kwargs):
            autorizar_tipo(token, *tipos_permitidos)
            return funcao(token, *args, **kwargs)

        return wrapper

    return decorator


def require_modulo(modulo):
    """Cria um decorador com as permissões de um módulo."""
    if modulo not in PERMISSOES:
        raise ValueError("Módulo desconhecido.")

    return require_tipo(*PERMISSOES[modulo])