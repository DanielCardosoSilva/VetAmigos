"""Vista CLI de relatorio."""
from src.views.common_view import menu, texto

def abrir(controller):
    def resumo():
        dados = controller.resumo()
        print(f"Clientes: {dados['clientes']} | Animais: {dados['animais']} | Consultas: {dados['consultas']} | Canceladas: {dados['canceladas']}")
    def mensal():
        periodo = texto("Mês (AAAA-MM): ")
        dados = controller.mensal(periodo)
        print(f"Consultas em {periodo}: {dados['consultas']} | Total faturado: {dados['faturado']:.2f} €")
        for cedula, total in sorted(dados['por_medico'].items()):
            print(f"Cédula {cedula}: {total} consulta(s)")
    menu("Consultar relatórios", {"1": ("Resumo geral", resumo), "2": ("Relatório mensal", mensal)})
