from math import *

def bisseccao(a, b, delta, n, funcao):
    k = 0
    resultados = []
    
    fa = funcao(a)
    fb = funcao(b)
    
    if fa * fb > 0:
        raise ValueError("A função não muda de sinal no intervalo [a, b]")
    
    meio = (a + b) / 2
    fmeio = funcao(meio)
    resultados.append((k, a, b, meio, fmeio))
    
    if fabs(b - a) < delta:
        return meio, k, resultados
    
    while fabs(b - a) > delta and k < n:
        k += 1
        fa = funcao(a)
        meio = (a + b) / 2
        fmeio = funcao(meio)
        
        resultados.append((k, a, b, meio, fmeio))
        
        if fa * fmeio < 0:
            b = meio
        else:
            a = meio
            
        if fabs(b - a) < delta:
            break
    
    meio = (a + b) / 2

    return meio, k, resultados