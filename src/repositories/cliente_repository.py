"""src/repositories/cliente_repository.py"""

from src.models.cliente import Cliente
from db.connection import get_connection

class ClienteRepository:
    def inserir(self, cliente: Cliente) -> Cliente:
        """Insere um novo cliente na base de dados."""
        with get_connection() as conn:
            cur = conn.execute(
                "INSERT INTO clientes (nome, nif, telefone, email) VALUES (?, ?, ?, ?)",
                (cliente.nome, cliente.nif, cliente.telefone, cliente.email)
            )
            cliente.id = cur.lastrowid
        return cliente

    def listar_todos(self) -> list[Cliente]:
        """Devolve uma lista de todos os clientes registados."""
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM clientes").fetchall()

        clientes = [
            Cliente(
                nome=r["nome"],
                nif=r["nif"],
                telefone=r["telefone"],
                email=r["email"]
            ) for r in rows
        ]

        for i in range(len(rows)):
            clientes[i].id = rows[i]["id"]

        return clientes

    def obter_por_id(self, id_cliente: int) -> Cliente | None:
        """Obtém um cliente através do seu ID primário."""
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM clientes WHERE id = ?", (id_cliente,)).fetchone()

        if row:
            cliente = Cliente(
                nome=row["nome"],
                nif=row["nif"],
                telefone=row["telefone"],
                email=row["email"]
            )
            cliente.id = row["id"]
            return cliente

        return None

    def obter_por_nif(self, nif: str) -> Cliente | None:
        """Procura um cliente pelo NIF para evitar duplicações."""
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM clientes WHERE nif = ?", (nif,)).fetchone()

        if row:
            cliente = Cliente(
                nome=row["nome"],
                nif=row["nif"],
                telefone=row["telefone"],
                email=row["email"]
            )
            cliente.id = row["id"]
            return cliente

        return None
