"""Utilitários de apresentação para a CLI."""
from datetime import date, datetime
import sqlite3

def texto(mensagem):
    return input(mensagem).strip()

def inteiro(mensagem):
    return int(texto(mensagem))

def decimal(mensagem):
    return float(texto(mensagem).replace(",", "."))

def data(mensagem):
    return date.fromisoformat(texto(mensagem + " (AAAA-MM-DD): "))

def horario(mensagem):
    return datetime.strptime(texto(mensagem + " (AAAA-MM-DD HH:MM): "), "%Y-%m-%d %H:%M")

def mostrar(registos):
    if registos is None:
        print("Não encontrado.")
    elif isinstance(registos, (list, tuple)):
        if not registos:
            print("Não existem registos.")
        for registo in registos:
            print(registo)
    else:
        print(registos)

def menu(titulo, opcoes):
    while True:
        print(f"\n========== {titulo.upper()} ==========")
        for numero, (descricao, _) in opcoes.items():
            print(f"{numero}. {descricao}")
        print("0. Voltar")
        opcao = texto("\nEscolha uma opção: ")
        if opcao == "0":
            return
        if opcao not in opcoes:
            print("Opção inválida.")
            continue
        try:
            opcoes[opcao][1]()
        except (ValueError, sqlite3.IntegrityError) as erro:
            print(f"Erro: {erro}")
