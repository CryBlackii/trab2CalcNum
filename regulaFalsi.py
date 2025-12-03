from math import *

def regulaFalsi(a, b, delta, n, funcao):
    k = 0
    resultados = []
    
    fa = funcao(a)
    fb = funcao(b)
    
    resultados.append((k, a, b, None, fa, fb, None))
    
    if fabs(b - a) < delta:
        raiz = (a + b) / 2
        return raiz, k, resultados
    
    if fabs(fa) < delta:
        return a, k, resultados
    if fabs(fb) < delta:
        return b, k, resultados
    
    k = 1
    while k <= n:
        x = (a * fb - b * fa) / (fb - fa)
        fx = funcao(x)
        
        resultados.append((k, a, b, x, fa, fb, fx))
        
        if fabs(fx) < delta:
            return x, k, resultados
        
        if fa * fx > 0:
            a = x
            fa = fx
        else:
            b = x
            fb = fx
        
        if fabs(b - a) < delta:
            raiz = (a + b) / 2
            return raiz, k, resultados
        
        k += 1
    
    return x, k-1, resultados