# src/repositories/cliente_repository.py
import sqlite3
from src.models.cliente import Cliente
from db.connection import get_connection

class ClienteRepository:
    def inserir(self, cliente: Cliente) -> Cliente:
        """Insere um novo cliente na base de dados SQL Server / SQLite."""
        with get_connection() as conn:
            cur = conn.execute(
                "INSERT INTO clientes (nome, nif, telefone, email, morada) VALUES (?, ?, ?, ?, ?)",
                (cliente.nome, cliente.nif, cliente.telefone, cliente.email, cliente.morada)
            )
            cliente.id = cur.lastrowid
        return cliente

    def listar_todos(self) -> list[Cliente]:
        """Devolve uma lista de todos os clientes registados."""
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM clientes").fetchall()
        return [
            Cliente(
                id=r["id"],
                nome=r["nome"],
                nif=r["nif"],
                telefone=r["telefone"],
                email=r["email"]
                morada=r["morada"]
            ) for r in rows
        ]

    def obter_por_id(self, id_cliente: int) -> Cliente | None:
        """Obtém um cliente através do seu ID primário."""
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM clientes WHERE id = ?", (id_cliente,)).fetchone()
            if row:
                return Cliente(
                    id=row["id"],
                    nome=row["nome"],
                    nif=row["nif"],
                    telefone=row["telefone"],
                    email=row["email"],
                    morada=row["morada"]
                )
        return None

    def obter_por_nif(self, nif: str) -> Cliente | None:
        """Procura um cliente pelo NIF para evitar duplicações."""
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM clientes WHERE nif = ?", (nif,)).fetchone()
            if row:
                return Cliente(
                    id=row["id"],
                    nome=row["nome"],
                    nif=row["nif"],
                    telefone=row["telefone"],
                    email=row["email"],
                    morada=row["morada"]
                )
        return None