from math import *

def secante(x0, x1, delta, n, funcao):
    k = 0
    resultados = []
    
    fx0 = funcao(x0)
    fx1 = funcao(x1)
    
    resultados.append((k, x0, fx0, None, None))
    k += 1
    resultados.append((k, x1, fx1, fabs(x1 - x0), fabs(fx1)))
    
    if fabs(fx0) < delta:
        return x0, k, resultados
    if fabs(fx1) < delta or fabs(x1 - x0) < delta:
        return x1, k, resultados
    
    k = 2
    while k <= n:
        if fabs(fx1 - fx0) < 1e-15:
            break
            
        x2 = x1 - (fx1 * (x1 - x0)) / (fx1 - fx0)
        fx2 = funcao(x2)
        
        resultados.append((k, x2, fx2, fabs(x2 - x1), fabs(fx2)))
        
        if fabs(fx2) < delta or fabs(x2 - x1) < delta:
            return x2, k, resultados
        
        x0, x1 = x1, x2
        fx0, fx1 = fx1, fx2
        k += 1
    
    return x2, k-1, resultados