from math import *

def newton(x0, delta, n, funcao):
    def derivada(x):
        h = 1e-7
        return (funcao(x + h) - funcao(x)) / h
    
    k = 0
    resultados = []
    
    fx0 = funcao(x0)
    resultados.append((k, x0, fx0, None, None))
    
    if fabs(fx0) < delta:
        return x0, k, resultados
    
    k = 1
    while k <= n:
        fxlinha = derivada(x0)
        
        if fabs(fxlinha) < 1e-10:
            break
            
        x1 = x0 - (fx0 / fxlinha)
        fx1 = funcao(x1)
        
        resultados.append((k, x1, fx1, fabs(x1 - x0), fabs(fx1)))
        
        if fabs(fx1) < delta or fabs(x1 - x0) < delta:
            return x1, k, resultados
        
        x0 = x1
        fx0 = fx1
        k += 1
    
    return x1, k-1, resultados