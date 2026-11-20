"""Serviço de autenticação multifator TOTP do VetAmigos."""

import hmac
import time

import pyotp

from db.connection import get_connection


def inicializar_mfa():
    """Acrescenta os campos necessários ao MFA sem apagar funcionários."""

    # Fazer uma migração incremental da tabela de funcionários.
    colunas_necessarias = {
        "mfa_secret": "TEXT",
        "mfa_pendente": "TEXT",
        "mfa_ultimo_passo": "INTEGER"
    }

    with get_connection() as conn:
        colunas_existentes = {
            linha["name"]
            for linha in conn.execute("PRAGMA table_info(funcionarios)")
        }

        for coluna, definicao in colunas_necessarias.items():
            if coluna not in colunas_existentes:
                conn.execute(
                    f"ALTER TABLE funcionarios ADD COLUMN {coluna} {definicao}"
                )


def _obter_proprietario(nome_utilizador):
    """Obtém uma conta ativa do tipo Proprietario."""

    # Impedir a configuração de MFA em contas inexistentes ou desativadas.
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT id, nome_utilizador, mfa_secret, mfa_pendente,
                   mfa_ultimo_passo
            FROM funcionarios
            WHERE nome_utilizador = ?
              AND tipo = 'Proprietario'
              AND ativo = 1
            """,
            (nome_utilizador,)
        ).fetchone()


def _passo_valido(segredo, codigo, ultimo_passo=None):
    """Identifica o intervalo TOTP válido e impede reutilizar códigos."""

    # Validar seis dígitos e permitir uma janela de 30 segundos de tolerância.
    if (
        not isinstance(codigo, str)
        or len(codigo) != 6
        or not codigo.isascii()
        or not codigo.isdecimal()
    ):
        return None

    totp = pyotp.TOTP(segredo)
    passo_atual = int(time.time() // totp.interval)

    for passo in (
        passo_atual - 1,
        passo_atual,
        passo_atual + 1
    ):
        if ultimo_passo is not None and passo <= ultimo_passo:
            continue

        esperado = totp.at(passo * totp.interval)

        if hmac.compare_digest(esperado, codigo):
            return passo

    return None


def iniciar_configuracao(nome_utilizador):
    """Gera um segredo temporário e a URI para configurar o autenticador."""

    # Criar um segredo apenas para uma conta de proprietário válida.
    funcionario = _obter_proprietario(nome_utilizador)

    if funcionario is None:
        raise ValueError("Conta de proprietário não encontrada ou inativa.")

    if funcionario["mfa_secret"]:
        raise ValueError("A autenticação multifator já está configurada.")

    segredo = pyotp.random_base32()

    with get_connection() as conn:
        conn.execute(
            """
            UPDATE funcionarios
            SET mfa_pendente = ?
            WHERE id = ?
            """,
            (segredo, funcionario["id"])
        )

    uri = pyotp.TOTP(segredo).provisioning_uri(
        name=nome_utilizador,
        issuer_name="VetAmigos"
    )

    return {
        "secret": segredo,
        "uri": uri
    }


def confirmar_configuracao(nome_utilizador, codigo):
    """Ativa o MFA depois de confirmar um código do autenticador."""

    # Impedir a ativação sem verificar o segredo provisório.
    funcionario = _obter_proprietario(nome_utilizador)

    if funcionario is None or not funcionario["mfa_pendente"]:
        raise ValueError("Não existe uma configuração MFA pendente.")

    passo = _passo_valido(
        funcionario["mfa_pendente"],
        codigo
    )

    if passo is None:
        return False

    with get_connection() as conn:
        resultado = conn.execute(
            """
            UPDATE funcionarios
            SET mfa_secret = mfa_pendente,
                mfa_pendente = NULL,
                mfa_ultimo_passo = ?
            WHERE id = ?
              AND mfa_pendente = ?
              AND mfa_secret IS NULL
            """,
            (
                passo,
                funcionario["id"],
                funcionario["mfa_pendente"]
            )
        )

    return resultado.rowcount == 1


def mfa_ativo(nome_utilizador):
    """Indica se o proprietário tem MFA configurado."""

    # Distinguir uma configuração confirmada de uma configuração pendente.
    funcionario = _obter_proprietario(nome_utilizador)

    return bool(funcionario and funcionario["mfa_secret"])


def verificar_codigo(nome_utilizador, codigo):
    """Verifica o código TOTP ativo, impedindo a sua reutilização."""

    # Recusar autenticação se não existir MFA configurado.
    funcionario = _obter_proprietario(nome_utilizador)

    if funcionario is None or not funcionario["mfa_secret"]:
        return False

    passo = _passo_valido(
        funcionario["mfa_secret"],
        codigo,
        funcionario["mfa_ultimo_passo"]
    )

    if passo is None:
        return False

    # Guardar o intervalo utilizado para impedir reutilização do mesmo código.
    with get_connection() as conn:
        resultado = conn.execute(
            """
            UPDATE funcionarios
            SET mfa_ultimo_passo = ?
            WHERE id = ?
              AND (mfa_ultimo_passo IS NULL OR mfa_ultimo_passo < ?)
            """,
            (passo, funcionario["id"], passo)
        )

    return resultado.rowcount == 1
