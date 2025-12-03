#metodos de Gauss (Jacobi e seidel)

import numpy as np
import time


def gauss_jacobi(A, b, x0=None, tol=1e-6, max_iter=1000, mostrar_passos=False):

    n = len(b)
    A = A.astype(float)
    b = b.astype(float)
    
    if x0 is None:
        x = np.zeros(n)
    else:
        x = x0.copy()
    
    x_new = np.zeros(n)
    passos = []
    
    inicio = time.time()
    
    try:
        # Verificar se diagonal não tem zeros
        for i in range(n):
            if abs(A[i, i]) < 1e-10:
                raise ValueError(f"Elemento diagonal A[{i+1},{i+1}] é zero. Método de Jacobi não aplicável.")
        
        # Critério de convergência (critério das linhas)
        criterio_linhas = True
        for i in range(n):
            soma = np.sum(np.abs(A[i, :])) - np.abs(A[i, i])
            if soma >= np.abs(A[i, i]):
                criterio_linhas = False
                break
        
        if not criterio_linhas and mostrar_passos:
            passos.append("AVISO: Matriz não satisfaz critério das linhas. Convergência não garantida.\n")
        
        for k in range(max_iter):
            if mostrar_passos and k < 5:  # Mostrar apenas primeiras 5 iterações
                passos.append(f"\n--- Iteração {k+1} ---")
            
            for i in range(n):
                soma = np.dot(A[i, :], x) - A[i, i] * x[i]
                x_new[i] = (b[i] - soma) / A[i, i]
            
            if mostrar_passos and k < 5:
                passos.append(f"x^({k+1}) = {x_new}")
            
            # Verificar convergência
            erro = np.linalg.norm(x_new - x, np.inf)
            
            if mostrar_passos and k < 5:
                passos.append(f"Erro = {erro:.10f}")
            
            x = x_new.copy()
            
            if erro < tol:
                tempo = time.time() - inicio
                if mostrar_passos:
                    passos.append(f"\n--- Convergência atingida na iteração {k+1} ---")
                
                return {
                    'sucesso': True,
                    'solucao': x,
                    'tempo': tempo,
                    'passos': '\n'.join(passos) if mostrar_passos else '',
                    'iteracoes': k + 1,
                    'erro_final': erro
                }
        
        # Não convergiu
        tempo = time.time() - inicio
        return {
            'sucesso': False,
            'erro': f"Método não convergiu em {max_iter} iterações. Erro final: {erro:.10f}",
            'tempo': tempo,
            'iteracoes': max_iter,
            'solucao_parcial': x
        }
        
    except Exception as e:
        tempo = time.time() - inicio
        return {
            'sucesso': False,
            'erro': str(e),
            'tempo': tempo
        }


def gauss_seidel(A, b, x0=None, tol=1e-6, max_iter=1000, mostrar_passos=False):
   
    n = len(b)
    A = A.astype(float)
    b = b.astype(float)
    
    if x0 is None:
        x = np.zeros(n)
    else:
        x = x0.copy()
    
    x_old = x.copy()
    passos = []
    
    inicio = time.time()
    
    try:
        # Verificar se diagonal não tem zeros
        for i in range(n):
            if abs(A[i, i]) < 1e-10:
                raise ValueError(f"Elemento diagonal A[{i+1},{i+1}] é zero. Método de Gauss-Seidel não aplicável.")
        
        # Critério de convergência (critério das linhas)
        criterio_linhas = True
        for i in range(n):
            soma = np.sum(np.abs(A[i, :])) - np.abs(A[i, i])
            if soma >= np.abs(A[i, i]):
                criterio_linhas = False
                break
        
        if not criterio_linhas and mostrar_passos:
            passos.append("AVISO: Matriz não satisfaz critério das linhas. Convergência não garantida.\n")
        
        for k in range(max_iter):
            if mostrar_passos and k < 5:  # Mostrar apenas primeiras 5 iterações
                passos.append(f"\n--- Iteração {k+1} ---")
            
            x_old = x.copy()
            
            for i in range(n):
                soma1 = np.dot(A[i, :i], x[:i])
                soma2 = np.dot(A[i, i+1:], x_old[i+1:])
                x[i] = (b[i] - soma1 - soma2) / A[i, i]
            
            if mostrar_passos and k < 5:
                passos.append(f"x^({k+1}) = {x}")
            
            # Verificar convergência
            erro = np.linalg.norm(x - x_old, np.inf)
            
            if mostrar_passos and k < 5:
                passos.append(f"Erro = {erro:.10f}")
            
            if erro < tol:
                tempo = time.time() - inicio
                if mostrar_passos:
                    passos.append(f"\n--- Convergência atingida na iteração {k+1} ---")
                
                return {
                    'sucesso': True,
                    'solucao': x,
                    'tempo': tempo,
                    'passos': '\n'.join(passos) if mostrar_passos else '',
                    'iteracoes': k + 1,
                    'erro_final': erro
                }
        
        # Não convergiu
        tempo = time.time() - inicio
        return {
            'sucesso': False,
            'erro': f"Método não convergiu em {max_iter} iterações. Erro final: {erro:.10f}",
            'tempo': tempo,
            'iteracoes': max_iter,
            'solucao_parcial': x
        }
        
    except Exception as e:
        tempo = time.time() - inicio
        return {
            'sucesso': False,
            'erro': str(e),
            'tempo': tempo
        }
