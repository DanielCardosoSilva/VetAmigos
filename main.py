
def main():
    print("=" * 40)
    print("           VETAMIGOS")
    print("  Sistema de Gestão Veterinária")
    print("=" * 40)

    # TODO: Iniciar o controller quando a estrutura de pastas for criada.

    while True:
        print("\n1. Gerir clientes")
        print("2. Gerir animais")
        print("3. Gerir consultas")
        print("4. Gerir vacinação")
        print("5. Gerir medicamentos")
        print("6. Gerir receitas")
        print("7. Gerir faturas e pagamentos")
        print("8. Consultar relatórios")
        print("0. Sair")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "0":
            print("\nAplicação encerrada. Até à próxima!")
            break
        elif opcao in ("1", "2", "3", "4", "5", "6", "7", "8"):
            # TODO: Implementar a funcionalidade correspondente à opção selecionada.
            continue
        else:
            print("\nOpção inválida. Tente novamente.")


if __name__ == "__main__":
    main()


