import jwt
import datetime
from datetime import timezone
import os


#Lab 2

SECRET_KEY = os.environ.get("VETAMIGOS_SECRET", "dev-only-chave-longa-32chars")

def criar_token(func) -> str:
    agora = datetime.datetime.now(timezone.utc)
    payload = {
        "sub":  func.nome_utilizador,
        "tipo": func.tipo,
        "nome": func.nome,
        "iat":  agora,
        "exp":  agora + datetime.timedelta(hours=1),
        "iss":  "vetamigos",
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def validar_token(token: str):
    """Valida JWT. Devolve o payload, ou None se inválido/expirado."""
    try:
        return jwt.decode(
            token, SECRET_KEY, algorithms=["HS256"], issuer="vetamigos"
        )
    except jwt.ExpiredSignatureError:
        print("Sessão expirada — faça login novamente.")
    except jwt.InvalidTokenError as e:
        print(f"Token inválido: {e}")
    return None
    


# login_view.py
funcionario = controller.iniciar_sessao(utilizador, senha)
token = criar_token(funcionario)
menu_view.abrir(token, controllers)      # token, not the object

# menu_view.py  (or wherever the token arrives)
def abrir(self, token, controllers):
    dados = validar_token(token)
    if not dados:
        self.voltar_ao_login()
        return
    self.utilizador_actual = dados           # sub / tipo / nome
    # ... render menu by dados["tipo"]


#Lab 4

EXPIRY_HOURS = int(os.environ.get("VETAMIGOS_EXPIRY_HOURS", "1"))
...
"exp": agora + datetime.timedelta(hours=EXPIRY_HOURS),

import uuid

_REVOGADOS = set()          # jti values logged out (module-level, in-memory)

def criar_token(func) -> str:
    agora = datetime.datetime.now(timezone.utc)
    payload = {
        "sub":  func.nome_utilizador,
        "tipo": func.tipo,
        "nome": func.nome,
        "jti":  str(uuid.uuid4()),            # <-- new: unique id
        "iat":  agora,
        "exp":  agora + datetime.timedelta(hours=EXPIRY_HOURS),
        "iss":  "vetamigos",
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def validar_token(token: str):
    try:
        dados = jwt.decode(
            token, SECRET_KEY, algorithms=["HS256"], issuer="vetamigos"
        )
    except jwt.ExpiredSignatureError:
        print("Sessão expirada.")
        return None
    except jwt.InvalidTokenError as e:
        print(f"Token inválido: {e}")
        return None

    if dados["jti"] in _REVOGADOS:            # <-- new: logout check
        print("Sessão terminada (logout).")
        return None
    return dados


def terminar_sessao(token: str) -> bool:      # <-- new: logout function
    """Invalida o token imediatamente (logout)."""
    dados = validar_token(token)
    if dados:
        _REVOGADOS.add(dados["jti"])
        return True
    return False

# logout_view.py
def logout(self, token):
    terminar_sessao(token)
    self.voltar_ao_login()