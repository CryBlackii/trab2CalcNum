from leitura import leitura
from bisseccao import bisseccao
from mil import mil
from newton import newton
from secante import secante
from regulaFalsi import regulaFalsi

def executar_metodos(a, b, x0, x1, delta, n, funcao, phi):
    resultados = {}
    
    try:
        raiz_bisseccao, k_bisseccao, _ = bisseccao(a, b, delta, n, funcao)
        resultados["Bisseção"] = f"{raiz_bisseccao:.6f} ({k_bisseccao} it.)"
    except Exception:
        resultados["Bisseção"] = "Erro: Sem raiz"
    
    try:
        raiz_mil, k_mil, _ = mil(x0, delta, n, funcao, phi)
        resultados["MIL"] = f"{raiz_mil:.6f} ({k_mil} it.)"
    except Exception:
        resultados["MIL"] = "Erro: Sem raiz"
    
    try:
        raiz_regula, k_regula, _ = regulaFalsi(a, b, delta, n, funcao)
        resultados["Regula Falsi"] = f"{raiz_regula:.6f} ({k_regula} it.)"
    except Exception:
        resultados["Regula Falsi"] = "Erro"
    
    try:
        raiz_newton, k_newton, _ = newton(x0, delta, n, funcao)
        resultados["Newton"] = f"{raiz_newton:.6f} ({k_newton} it.)"
    except Exception:
        resultados["Newton"] = "Erro"
    
    try:
        raiz_secante, k_secante, _ = secante(x0, x1, delta, n, funcao)
        resultados["Secante"] = f"{raiz_secante:.6f} ({k_secante} it.)"
    except Exception:
        resultados["Secante"] = "Erro"
    
    return resultados

def imprimir_tabela_completa(todos_resultados):
    print("\n" + "="*120)
    print("RESULTADOS")
    print("="*120)
    
    cabecalho = "| {:<10} | {:<18} | {:<18} | {:<18} | {:<18} | {:<18} |".format(
        "Exercício", "Bisseção", "Regula Falsi", "Newton", "Secante", "MIL"
    )
    print(cabecalho)
    print("="*120)
    
    for exercicio, resultados in todos_resultados.items():
        linha = "| {:<10} | {:<18} | {:<18} | {:<18} | {:<18} | {:<18} |".format(
            exercicio,
            resultados.get("Bisseção", "-"),
            resultados.get("Regula Falsi", "-"),
            resultados.get("Newton", "-"),
            resultados.get("Secante", "-"),
            resultados.get("MIL", "-")
        )
        print(linha)
    
    print("="*120)

if __name__ == "__main__":
    try:
        exercicios = leitura("exer.txt")
        
        if not exercicios:
            print("Nenhum exercício encontrado no arquivo!")
            exit()
        
        todos_resultados = {}
        
        for exercicio in exercicios:
            resultados = executar_metodos(
                exercicio['a'], exercicio['b'], exercicio['x0'], exercicio['x1'],
                exercicio['delta'], exercicio['n'], exercicio['funcao'], exercicio['phi']
            )
            
            todos_resultados[exercicio['nome']] = resultados
        
        imprimir_tabela_completa(todos_resultados)
        
    except Exception as e:
        print(f"Erro geral: {e}")
        import traceback
        traceback.print_exc()