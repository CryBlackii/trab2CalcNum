from math import *

def mil(x0, delta, n, funcao, phi):
    k = 0
    resultados = []
    
    fx0 = funcao(x0)
    resultados.append((k, x0, fx0, None))
    
    if fabs(fx0) < delta:
        return x0, k, resultados
    
    k = 1
    while k <= n:
        x1 = phi(x0)
        fx1 = funcao(x1)
        
        resultados.append((k, x1, fx1, fabs(x1 - x0)))
        
        if fabs(fx1) < delta or fabs(x1 - x0) < delta:
            return x1, k, resultados
        
        x0 = x1
        k += 1
    
    return x1, k-1, resultados