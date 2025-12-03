# Cholenski e LU

import numpy as np
import time


def fatoracao_lu(A, b, mostrar_passos=False):
    n = len(b)
    A = A.astype(float).copy()
    b = b.astype(float).copy()
    L = np.eye(n)
    U = A.copy()
    passos = []
    
    inicio = time.time()
    
    try:
        # Fatoração LU
        for k in range(n-1):
            if abs(U[k, k]) < 1e-10:
                raise ValueError(f"Pivô nulo na posição ({k+1},{k+1}). Fatoração LU sem pivoteamento não é possível.")
            
            if mostrar_passos:
                passos.append(f"\n--- Passo {k+1} ---")
            
            for i in range(k+1, n):
                L[i, k] = U[i, k] / U[k, k]
                U[i, k:] = U[i, k:] - L[i, k] * U[k, k:]
                
                if mostrar_passos:
                    passos.append(f"L[{i+1},{k+1}] = {L[i,k]:.6f}")
        
        if mostrar_passos:
            passos.append("\n--- Matriz L ---")
            passos.append(str(L))
            passos.append("\n--- Matriz U ---")
            passos.append(str(U))
        
        # Resolver Ly = b (substituição direta)
        y = np.zeros(n)
        for i in range(n):
            y[i] = b[i] - np.dot(L[i, :i], y[:i])
        
        # Resolver Ux = y (substituição reversa)
        x = np.zeros(n)
        for i in range(n-1, -1, -1):
            if abs(U[i, i]) < 1e-10:
                raise ValueError(f"Sistema singular detectado")
            x[i] = (y[i] - np.dot(U[i, i+1:], x[i+1:])) / U[i, i]
        
        tempo = time.time() - inicio
        
        return {
            'sucesso': True,
            'solucao': x,
            'tempo': tempo,
            'passos': '\n'.join(passos) if mostrar_passos else '',
            'iteracoes': None,
            'L': L,
            'U': U
        }
        
    except Exception as e:
        tempo = time.time() - inicio
        return {
            'sucesso': False,
            'erro': str(e),
            'tempo': tempo
        }


def fatoracao_cholesky(A, b, mostrar_passos=False):

    n = len(b)
    A = A.astype(float).copy()
    b = b.astype(float).copy()
    passos = []
    
    inicio = time.time()
    
    try:
        # Verificar se a matriz é simétrica
        if not np.allclose(A, A.T):
            raise ValueError("Matriz nao é simétrica. ")
        
        # Fatoração de Cholesky: A = L * L^T
        L = np.zeros((n, n))
        
        for i in range(n):
            for j in range(i+1):
                if i == j:
                    soma = np.sum(L[i, :j]**2)
                    valor = A[i, i] - soma
                    if valor <= 0:
                        raise ValueError(f"Matriz não é positiva definida. Elemento diagonal {i+1} resultou em valor não positivo.")
                    L[i, j] = np.sqrt(valor)
                else:
                    soma = np.sum(L[i, :j] * L[j, :j])
                    L[i, j] = (A[i, j] - soma) / L[j, j]
            
            if mostrar_passos:
                passos.append(f"--- Linha {i+1} de L ---")
                passos.append(str(L[i, :i+1]))
        
        if mostrar_passos:
            passos.append("\n--- Matriz L (Cholesky) ---")
            passos.append(str(L))
        
        # Resolver Ly = b (substituição direta)
        y = np.zeros(n)
        for i in range(n):
            y[i] = (b[i] - np.dot(L[i, :i], y[:i])) / L[i, i]
        
        # Resolver L^T x = y (substituição reversa)
        x = np.zeros(n)
        for i in range(n-1, -1, -1):
            x[i] = (y[i] - np.dot(L[i+1:, i], x[i+1:])) / L[i, i]
        
        tempo = time.time() - inicio
        
        return {
            'sucesso': True,
            'solucao': x,
            'tempo': tempo,
            'passos': '\n'.join(passos) if mostrar_passos else '',
            'iteracoes': None,
            'L': L
        }
        
    except Exception as e:
        tempo = time.time() - inicio
        return {
            'sucesso': False,
            'erro': str(e),
            'tempo': tempo
        }
