========================================
SOLVER DE SISTEMAS LINEARES
Cálculo Numérico - Capítulo 3
========================================

ESTRUTURA DO PROJETO:
====================

O projeto está organizado em 4 arquivos modulares:

1. Trab2.py - Interface gráfica principal
2. metodos_eliminacao_gauss.py - Métodos de Gauss
3. metodos_fatoracao.py - Métodos de fatoração
4. metodos_iterativos.py - Métodos iterativos

MÉTODOS IMPLEMENTADOS:
=====================

MÉTODOS DIRETOS:
1. Eliminação de Gauss (sem pivoteamento)
2. Eliminação de Gauss com Pivoteamento Parcial
3. Eliminação de Gauss com Pivoteamento Completo
4. Fatoração LU
5. Fatoração de Cholesky (para matrizes simétricas positivas definidas)

MÉTODOS ITERATIVOS:
6. Método de Gauss-Jacobi
7. Método de Gauss-Seidel

COMO USAR:
==========

1. Execute o programa:
   python Trab2.py

2. Carregue um sistema linear de uma das formas:
   - Arquivo com [A|b] juntos (matriz aumentada)
   - Arquivos separados para A e b
   - Inserir manualmente

3. Selecione o método desejado

4. Para métodos iterativos:
   - Configure tolerância (padrão: 1e-6)
   - Configure máximo de iterações (padrão: 1000)

5. Marque "Mostrar passos detalhados" se quiser ver o processo completo

6. Clique em "RESOLVER SISTEMA"

FORMATOS DE ARQUIVO:
====================

1. Sistema completo [A|b]:
   Cada linha representa uma equação
   Última coluna é o vetor b
   
   Exemplo (3x3):
   3 2 -1 5
   2 -2 4 -2
   -1 0.5 -1 0

2. Matriz A separada:
   Apenas os coeficientes da matriz
   
   Exemplo (3x3):
   3 2 -1
   2 -2 4
   -1 0.5 -1

3. Vetor b separado:
   Um valor por linha
   
   Exemplo:
   5
   -2
   0

SUPORTE A FRAÇÕES:
==================

✓ Agora aceita FRAÇÕES no formato a/b!

Exemplos com frações:
   1/2 1/3 5/6
   2 -1/4 7/4
   -1/3 2 0.5 4.166667

Formatos aceitos:
   • Inteiros: 2, -5, 10
   • Decimais: 1.5, -0.5, 3.14
   • Frações: 1/2, -3/4, 5/8
   • Misturado: pode combinar tudo na mesma matriz!

Arquivos de exemplo com frações:
   • exemplo_sistema_fracoes.txt
   • exemplo_matriz_fracoes.txt
   • exemplo_vetor_fracoes.txt

Para mais detalhes, veja: GUIA_FRACOES.txt

ARQUIVOS DE EXEMPLO:
===================

- exemplo_sistema1.txt: Sistema 3x3 geral
- exemplo_sistema2_cholesky.txt: Sistema 3x3 simétrico positivo definido (use Cholesky)
- exemplo_matriz_A.txt: Matriz 4x4 com diagonal dominante (bom para iterativos)
- exemplo_vetor_b.txt: Vetor b correspondente à matriz A

OBSERVAÇÕES IMPORTANTES:
========================

1. Cholesky: Só funciona para matrizes simétricas e positivas definidas

2. Métodos iterativos: Convergência é garantida para matrizes com diagonal dominante

3. Gauss sem pivoteamento: Pode falhar se encontrar pivô nulo

4. O programa detecta e informa casos especiais:
   - Matrizes singulares
   - Necessidade de pivoteamento
   - Cholesky não aplicável
   - Divergência de métodos iterativos

5. Todos os resultados incluem:
   - Solução do sistema
   - Tempo de execução
   - Resíduo ||Ax - b|| para verificação
   - Número de iterações (para métodos iterativos)

ESTRUTURA DE ARQUIVOS:
=====================

Trab2.py                        - Interface gráfica (arquivo principal)
metodos_eliminacao_gauss.py     - Eliminação de Gauss (sem, parcial, completo)
metodos_fatoracao.py            - Fatoração LU e Cholesky
metodos_iterativos.py           - Gauss-Jacobi e Gauss-Seidel
exemplo_sistema1.txt            - Sistema 3x3 exemplo
exemplo_sistema2_cholesky.txt   - Sistema simétrico positivo definido
exemplo_matriz_A.txt            - Matriz 4x4 diagonal dominante
exemplo_vetor_b.txt             - Vetor b correspondente
README.txt                      - Este arquivo

REQUISITOS:
===========

- Python 3.x
- NumPy
- Tkinter (geralmente já vem com Python)

Para instalar NumPy:
pip install numpy

EXECUÇÃO:
=========

1. Certifique-se de que todos os 4 arquivos .py estão na mesma pasta
2. Execute o arquivo principal:
   python Trab2.py

========================================
Desenvolvido para a disciplina de
Cálculo Numérico
========================================
