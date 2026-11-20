"""Proteção dos controllers com JWT e RBAC."""

from functools import wraps

from src.rbac import autorizar_modulo


class ControladorProtegido:
    """Intermediário que autoriza operações de um módulo."""

    def __init__(self, controller, modulo, token):
        # Guardar o controller original e os dados de autorização.
        self._controller = controller
        self._modulo = modulo
        self._token = token

    def __getattr__(self, nome):
        # Validar o acesso antes de disponibilizar uma operação.
        atributo = getattr(self._controller, nome)

        if not callable(atributo):
            autorizar_modulo(self._token, self._modulo)
            return atributo

        @wraps(atributo)
        def executar(*args, **kwargs):
            # Revalidar o JWT antes de cada operação.
            autorizar_modulo(self._token, self._modulo)
            return atributo(*args, **kwargs)

        return executar


def proteger_controllers(controllers, token):
    """Cria versões protegidas dos controllers de negócio."""
    protegidos = {}

    for modulo, controller in controllers.items():
        # Manter o controller de autenticação separado do acesso de negócio.
        if modulo == "auth":
            protegidos[modulo] = controller
        else:
            protegidos[modulo] = ControladorProtegido(
                controller, modulo, token
            )

    return protegidos