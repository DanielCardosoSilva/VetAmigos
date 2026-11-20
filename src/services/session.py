"""Gestão de sessões JWT do VetAmigos"""

import os
import uuid
from datetime import datetime, timedelta, timezone

import jwt


EMISSOR = "vetamigos"
DESTINATARIO = "vetamigos-desktop"
_REVOGADOS = {}


def _obter_chave():
    """Obtém a chave JWT configurada fora do código-fonte."""
    chave = os.environ.get("VETAMIGOS_SECRET", "")

    if len(chave.encode("utf-8")) < 32:
        raise RuntimeError(
            "Configure VETAMIGOS_SECRET com uma chave "
            "secreta de pelo menos 32 bytes."
        )

    return chave


def _limpar_revogados():
    """Remove da lista de revogação os tokens já expirados."""
    agora = datetime.now(timezone.utc).timestamp()

    for identificador, expiracao in list(_REVOGADOS.items()):
        if expiracao <= agora:
            del _REVOGADOS[identificador]


def criar_token(funcionario, mfa_confirmado=False):
    """Emite um JWT após a autenticação completa do funcionário."""
    if not getattr(funcionario, "ativo", False):
        raise PermissionError("Conta desativada.")

    if (
        funcionario.tipo == "Proprietario"
        and not mfa_confirmado
    ):
        raise PermissionError(
            "É necessário concluir a verificação MFA."
        )

    duracao = int(os.environ.get("VETAMIGOS_EXPIRY_HOURS", "1"))

    if duracao <= 0 or duracao > 24:
        raise ValueError("Duração de sessão inválida.")

    agora = datetime.now(timezone.utc)

    payload = {
        "sub": str(funcionario.nome_utilizador),
        "tipo": funcionario.tipo,
        "nome": funcionario.nome,
        "mfa": bool(mfa_confirmado),
        "jti": str(uuid.uuid4()),
        "iss": EMISSOR,
        "aud": DESTINATARIO,
        "iat": agora,
        "nbf": agora,
        "exp": agora + timedelta(hours=duracao)
    }

    return jwt.encode(
        payload,
        _obter_chave(),
        algorithm="HS256"
    )


def validar_token(token):
    """Valida assinatura, campos, expiração e revogação do JWT."""
    if not isinstance(token, str) or not token.strip():
        raise jwt.InvalidTokenError("Token em falta.")

    dados = jwt.decode(
        token,
        _obter_chave(),
        algorithms=["HS256"],
        issuer=EMISSOR,
        audience=DESTINATARIO,
        options={
            "require": [
                "sub", "tipo", "jti", "iss",
                "aud", "iat", "nbf", "exp", "mfa"
            ]
        }
    )

    _limpar_revogados()

    if dados["jti"] in _REVOGADOS:
        raise jwt.InvalidTokenError("Sessão terminada.")

    if dados["tipo"] == "Proprietario" and dados["mfa"] is not True:
        raise jwt.InvalidTokenError("MFA não confirmado.")

    return dados


def terminar_sessao(token):
    """Revoga um JWT válido, impedindo a sua reutilização."""
    try:
        dados = validar_token(token)
    except jwt.InvalidTokenError:
        return False

    _REVOGADOS[dados["jti"]] = dados["exp"]
    _limpar_revogados()
    return True