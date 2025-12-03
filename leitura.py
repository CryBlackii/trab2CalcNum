import math

def leitura(caminho):
    with open(caminho, 'r') as f:
        linhas = f.readlines()
    
    exercicios = []
    exercicio_atual = {}
    
    for linha in linhas:
        linha = linha.strip()
        
        if linha.startswith('# ex'):
            if exercicio_atual:
                exercicios.append(exercicio_atual)
                exercicio_atual = {}
            exercicio_atual['nome'] = linha[2:].strip()
        elif '=' in linha:
            chave, valor = linha.split('=', 1)
            chave = chave.strip()
            valor = valor.strip()
            exercicio_atual[chave] = valor
    
    if exercicio_atual:
        exercicios.append(exercicio_atual)
    
    for exercicio in exercicios:
        expressao = exercicio['funcao']
        # Usar math.e em vez de e solto
        exercicio['funcao'] = lambda x, expr=expressao: eval(expr, {
            "x": x, "log": math.log, "log10": math.log10, "sqrt": math.sqrt, 
            "sin": math.sin, "cos": math.cos, "tan": math.tan, "exp": math.exp, 
            "pi": math.pi, "e": math.e
        })
        
        expressao_phi = exercicio['phi']
        exercicio['phi'] = lambda x, expr=expressao_phi: eval(expr, {
            "x": x, "log": math.log, "log10": math.log10, "sqrt": math.sqrt, 
            "sin": math.sin, "cos": math.cos, "tan": math.tan, "exp": math.exp, 
            "pi": math.pi, "e": math.e
        })
        
        exercicio['a'] = float(exercicio.get('a', 0))
        exercicio['b'] = float(exercicio.get('b', 0))
        exercicio['x0'] = float(exercicio.get('x0', 0))
        exercicio['x1'] = float(exercicio.get('x1', 0))
        exercicio['delta'] = float(exercicio.get('delta', 0.001))
        exercicio['n'] = int(exercicio.get('n', 50))
        exercicio['expressao'] = expressao
    
    return exercicios