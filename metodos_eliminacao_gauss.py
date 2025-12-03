#Eliminação de gauss com pivoteamento parcial e completo (sem tambem)

import numpy as np
import time


def eliminacao_gauss_sem_pivoteamento(A, b, mostrar_passos=False):
    n = len(b)
    A = A.astype(float).copy()
    b = b.astype(float).copy()
    passos = []
    
    inicio = time.time()
    
    try:
        # Fase de eliminação
        for k in range(n-1):
            if abs(A[k, k]) < 1e-10:
                raise ValueError(f"Pivô nulo encontrado na posição ({k},{k}). Sistema pode ser singular ou necessitar pivoteamento.")
            
            if mostrar_passos:
                passos.append(f"\n--- Passo {k+1}: Eliminação da coluna {k+1} ---")
                passos.append(f"Pivô: A[{k+1},{k+1}] = {A[k,k]:.6f}")
            
            for i in range(k+1, n):
                multiplicador = A[i, k] / A[k, k]
                A[i, k:] = A[i, k:] - multiplicador * A[k, k:]
                b[i] = b[i] - multiplicador * b[k]
                
                if mostrar_passos:
                    passos.append(f"L[{i+1},{k+1}] = {multiplicador:.6f}")
        
        # Substituição reversa
        x = np.zeros(n)
        for i in range(n-1, -1, -1):
            if abs(A[i, i]) < 1e-10:
                raise ValueError(f"Sistema singular detectado na linha {i+1}")
            x[i] = (b[i] - np.dot(A[i, i+1:], x[i+1:])) / A[i, i]
        
        tempo = time.time() - inicio
        
        return {
            'sucesso': True,
            'solucao': x,
            'tempo': tempo,
            'passos': '\n'.join(passos) if mostrar_passos else '',
            'iteracoes': None
        }
        
    except Exception as e:
        tempo = time.time() - inicio
        return {
            'sucesso': False,
            'erro': str(e),
            'tempo': tempo
        }


def eliminacao_gauss_pivoteamento_parcial(A, b, mostrar_passos=False):
    n = len(b)
    A = A.astype(float).copy()
    b = b.astype(float).copy()
    passos = []
    
    inicio = time.time()
    
    try:
        # Fase de eliminação com pivoteamento parcial
        for k in range(n-1):
            # Encontrar o maior pivô na coluna k
            max_idx = k + np.argmax(np.abs(A[k:, k]))
            
            if abs(A[max_idx, k]) < 1e-10:
                raise ValueError(f"Matriz singular detectada na coluna {k+1}")
            
            # Trocar linhas se necessário
            if max_idx != k:
                A[[k, max_idx]] = A[[max_idx, k]]
                b[[k, max_idx]] = b[[max_idx, k]]
                if mostrar_passos:
                    passos.append(f"\n--- Troca de linhas {k+1} ↔ {max_idx+1} ---")
            
            if mostrar_passos:
                passos.append(f"\n--- Passo {k+1}: Eliminação da coluna {k+1} ---")
                passos.append(f"Pivô: A[{k+1},{k+1}] = {A[k,k]:.6f}")
            
            # Eliminação
            for i in range(k+1, n):
                multiplicador = A[i, k] / A[k, k]
                A[i, k:] = A[i, k:] - multiplicador * A[k, k:]
                b[i] = b[i] - multiplicador * b[k]
                
                if mostrar_passos:
                    passos.append(f"L[{i+1},{k+1}] = {multiplicador:.6f}")
        
        # Substituição reversa
        x = np.zeros(n)
        for i in range(n-1, -1, -1):
            x[i] = (b[i] - np.dot(A[i, i+1:], x[i+1:])) / A[i, i]
        
        tempo = time.time() - inicio
        
        return {
            'sucesso': True,
            'solucao': x,
            'tempo': tempo,
            'passos': '\n'.join(passos) if mostrar_passos else '',
            'iteracoes': None
        }
        
    except Exception as e:
        tempo = time.time() - inicio
        return {
            'sucesso': False,
            'erro': str(e),
            'tempo': tempo
        }


def eliminacao_gauss_pivoteamento_completo(A, b, mostrar_passos=False):

    n = len(b)
    A = A.astype(float).copy()
    b = b.astype(float).copy()
    ordem = np.arange(n)  # permutação das colunas
    passos = []
    
    inicio = time.time()
    
    try:
        # Fase de eliminação com pivoteamento completo
        for k in range(n-1):
            # Encontrar o maior pivô na submatriz A[k:, k:]
            submatriz = np.abs(A[k:, k:])
            i_max, j_max = np.unravel_index(np.argmax(submatriz), submatriz.shape)
            i_max += k
            j_max += k
            
            if abs(A[i_max, j_max]) < 1e-10:
                raise ValueError(f"Matriz singular detectada no passo {k+1}")
            
            # Trocar linhas se necessário
            if i_max != k:
                A[[k, i_max]] = A[[i_max, k]]
                b[[k, i_max]] = b[[i_max, k]]
                if mostrar_passos:
                    passos.append(f"\n--- Troca de linhas {k+1} ↔ {i_max+1} ---")
            
            # Trocar colunas se necessário
            if j_max != k:
                A[:, [k, j_max]] = A[:, [j_max, k]]
                ordem[[k, j_max]] = ordem[[j_max, k]]
                if mostrar_passos:
                    passos.append(f"--- Troca de colunas {k+1} ↔ {j_max+1} ---")
            
            if mostrar_passos:
                passos.append(f"\n--- Passo {k+1}: Eliminação da coluna {k+1} ---")
                passos.append(f"Pivô: A[{k+1},{k+1}] = {A[k,k]:.6f}")
            
            # Eliminação
            for i in range(k+1, n):
                multiplicador = A[i, k] / A[k, k]
                A[i, k:] = A[i, k:] - multiplicador * A[k, k:]
                b[i] = b[i] - multiplicador * b[k]
                
                if mostrar_passos:
                    passos.append(f"L[{i+1},{k+1}] = {multiplicador:.6f}")
        
        # Substituição reversa
        y = np.zeros(n)
        for i in range(n-1, -1, -1):
            y[i] = (b[i] - np.dot(A[i, i+1:], y[i+1:])) / A[i, i]
        
        # Reordenar solução de acordo com permutações de colunas
        x = np.zeros(n)
        for i in range(n):
            x[ordem[i]] = y[i]
        
        tempo = time.time() - inicio
        
        return {
            'sucesso': True,
            'solucao': x,
            'tempo': tempo,
            'passos': '\n'.join(passos) if mostrar_passos else '',
            'iteracoes': None
        }
        
    except Exception as e:
        tempo = time.time() - inicio
        return {
            'sucesso': False,
            'erro': str(e),
            'tempo': tempo
        }
