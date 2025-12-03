import numpy as np
import customtkinter as ctk
from tkinter import messagebox
from fractions import Fraction
import re
from metodos_eliminacao_gauss import eliminacao_gauss_sem_pivoteamento, eliminacao_gauss_pivoteamento_parcial, eliminacao_gauss_pivoteamento_completo
from metodos_fatoracao import fatoracao_lu, fatoracao_cholesky
from metodos_iterativos import gauss_jacobi, gauss_seidel

ROXO_PRIMARIO = "#8A2BE2"
ROXO_HOVER = "#7B1FA2"

def converter_para_float(valor_str):
    valor_str = valor_str.strip()
    try:
        if '/' in valor_str:
            return float(Fraction(valor_str))
        return float(valor_str)
    except:
        return None

class InterfaceTrab2(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.A = None
        self.b = None
        
        self.mapa_metodos = {
            "Gauss Simples": "gauss_sem_piv",
            "Gauss Piv. Parcial": "gauss_piv_parcial",
            "Gauss Piv. Completo": "gauss_piv_completo",
            "Fatoração LU": "fatoracao_lu",
            "Cholesky": "fatoracao_cholesky",
            "Gauss-Jacobi": "gauss_jacobi",
            "Gauss-Seidel": "gauss_seidel"
        }
        
        self.grid_rowconfigure(3, weight=1) 
        self.grid_columnconfigure(0, weight=1)
        
        self.criar_interface()
    
    def criar_interface(self):        
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        btn_voltar = ctk.CTkButton(header_frame, text="<< Menu Principal", 
                                 command=lambda: self.controller.mostrar_menu(),
                                 fg_color="transparent", border_width=1, 
                                 text_color="white", hover_color="#444", width=120)
        btn_voltar.pack(side="left")
        
        lbl_titulo = ctk.CTkLabel(header_frame, text="Sistemas Lineares", 
                                font=ctk.CTkFont(size=20, weight="bold"))
        lbl_titulo.pack(side="left", padx=20)

        frame_input = ctk.CTkFrame(self)
        frame_input.grid(row=1, column=0, sticky="ew", padx=20, pady=5)
        
        ctk.CTkLabel(frame_input, text="Insira a Matriz Aumentada [A|b] ou A=... b=...", 
                   font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(10,0))
        
        self.texto_input = ctk.CTkTextbox(frame_input, height=120, font=("Courier New", 12))
        self.texto_input.pack(fill="x", padx=10, pady=10)
        self.texto_input.insert("1.0", "3 -2 5 20\n6 -9 12 51\n-5 0 2 1")

        toolbar_frame = ctk.CTkFrame(self)
        toolbar_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        
        ctk.CTkLabel(toolbar_frame, text="Método:").pack(side="left", padx=(10, 5))
        
        self.menu_metodos = ctk.CTkOptionMenu(toolbar_frame, 
                                            values=list(self.mapa_metodos.keys()),
                                            fg_color=ROXO_PRIMARIO, 
                                            button_color=ROXO_HOVER, 
                                            button_hover_color=ROXO_HOVER,
                                            width=180)
        self.menu_metodos.pack(side="left", padx=5, pady=10)
        self.menu_metodos.set("Gauss Simples")

        ctk.CTkFrame(toolbar_frame, width=2, height=30, fg_color="gray").pack(side="left", padx=10)

        ctk.CTkLabel(toolbar_frame, text="Tol:").pack(side="left", padx=2)
        self.tol_var = ctk.StringVar(value="1e-6")
        ctk.CTkEntry(toolbar_frame, textvariable=self.tol_var, width=60).pack(side="left", padx=2)
        
        ctk.CTkLabel(toolbar_frame, text="Iter:").pack(side="left", padx=(10, 2))
        self.max_iter_var = ctk.StringVar(value="1000")
        ctk.CTkEntry(toolbar_frame, textvariable=self.max_iter_var, width=50).pack(side="left", padx=2)
        
        self.mostrar_passos_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(toolbar_frame, text="Passos", variable=self.mostrar_passos_var, width=60).pack(side="left", padx=15)
        
        ctk.CTkButton(toolbar_frame, text="RESOLVER", command=self.resolver_sistema,
                    fg_color=ROXO_PRIMARIO, hover_color=ROXO_HOVER, width=120).pack(side="right", padx=10, pady=10)

        frame_res = ctk.CTkFrame(self)
        frame_res.grid(row=3, column=0, sticky="nsew", padx=20, pady=(0, 20))
        frame_res.grid_columnconfigure(0, weight=1)
        frame_res.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(frame_res, text="Resultados", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", padx=10, pady=5)
        
        self.texto_resultado = ctk.CTkTextbox(frame_res, font=("Courier New", 12))
        self.texto_resultado.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

    
    def parser_input(self):
        conteudo = self.texto_input.get("1.0", "end").strip()
        if not conteudo: return None, None

        def extrair_nums(txt):
            txt = txt.replace('[', ' ').replace(']', ' ').replace(',', ' ').replace(';', ' ')
            mat = []
            for linha in txt.split('\n'):
                vals = []
                for item in linha.split():
                    if any(c.isalpha() and c.lower() != 'e' for c in item): continue 
                    if item == '=': continue
                    val = converter_para_float(item)
                    if val is not None: vals.append(val)
                if vals: mat.append(vals)
            return np.array(mat, dtype=float) if mat else np.array([])

        if re.search(r'\bb\s*=', conteudo, re.IGNORECASE):
            match_b = re.search(r'\bb\s*=', conteudo, re.IGNORECASE)
            parte_a = extrair_nums(conteudo[:match_b.start()])
            parte_b = extrair_nums(conteudo[match_b.end():]).flatten()
            return parte_a, parte_b
        
        dados = extrair_nums(conteudo)
        if dados.size == 0: return None, None
        
        rows, cols = dados.shape
        if cols == rows + 1: return dados[:, :-1], dados[:, -1]
        if cols == rows: return dados, None
        return dados[:, :-1], dados[:, -1]

    def resolver_sistema(self):
        try:
            self.A, self.b = self.parser_input()
            if self.A is None: 
                messagebox.showwarning("Aviso", "Caixa de entrada vazia ou inválida.")
                return
            if self.b is None:
                messagebox.showerror("Erro", "Vetor 'b' não identificado ou matriz incompleta.")
                return
            if len(self.A) != len(self.b):
                messagebox.showerror("Erro", f"Dimensões incompatíveis: A{self.A.shape} e b({len(self.b)})")
                return

        except Exception as e:
            messagebox.showerror("Erro de Leitura", f"Erro ao ler matriz: {e}")
            return
            
        nome_metodo = self.menu_metodos.get()
        chave_metodo = self.mapa_metodos[nome_metodo]
        mostrar = self.mostrar_passos_var.get()
        
        self.texto_resultado.delete('1.0', "end")
        self.texto_resultado.insert("end", f"Calculando via {nome_metodo}...\n")
        
        try:
            if chave_metodo == "gauss_sem_piv": res = eliminacao_gauss_sem_pivoteamento(self.A, self.b, mostrar)
            elif chave_metodo == "gauss_piv_parcial": res = eliminacao_gauss_pivoteamento_parcial(self.A, self.b, mostrar)
            elif chave_metodo == "gauss_piv_completo": res = eliminacao_gauss_pivoteamento_completo(self.A, self.b, mostrar)
            elif chave_metodo == "fatoracao_lu": res = fatoracao_lu(self.A, self.b, mostrar)
            elif chave_metodo == "fatoracao_cholesky": res = fatoracao_cholesky(self.A, self.b, mostrar)
            elif chave_metodo == "gauss_jacobi": res = gauss_jacobi(self.A, self.b, tol=float(self.tol_var.get()), max_iter=int(self.max_iter_var.get()), mostrar_passos=mostrar)
            elif chave_metodo == "gauss_seidel": res = gauss_seidel(self.A, self.b, tol=float(self.tol_var.get()), max_iter=int(self.max_iter_var.get()), mostrar_passos=mostrar)
            
            self.exibir_resultado(res, nome_metodo)
        except Exception as e:
            self.texto_resultado.insert("end", f"\nERRO CRÍTICO: {e}")

    def exibir_resultado(self, resultado, metodo):
        sep = "="*60 + "\n"
        self.texto_resultado.insert("end", sep)
        
        if resultado['sucesso']:
            self.texto_resultado.insert("end", "SOLUÇÃO ENCONTRADA:\n")
            for i, v in enumerate(resultado['solucao']):
                self.texto_resultado.insert("end", f"  x[{i+1}] = {v:.8f}\n")
            
            self.texto_resultado.insert("end", f"\nTempo: {resultado['tempo']:.6f}s")
            if 'iteracoes' in resultado and resultado['iteracoes']:
                self.texto_resultado.insert("end", f" | Iterações: {resultado['iteracoes']}")
            self.texto_resultado.insert("end", "\n")

            try:
                residuo = np.linalg.norm(np.dot(self.A, resultado['solucao']) - self.b)
                self.texto_resultado.insert("end", f"Resíduo ||Ax - b||: {residuo:.6e}\n")
            except: pass
            
            if resultado.get('passos'):
                self.texto_resultado.insert("end", "\n" + "-"*30 + " PASSO A PASSO " + "-"*30 + "\n")
                self.texto_resultado.insert("end", resultado['passos'])
        else:
            self.texto_resultado.insert("end", "FALHA NA EXECUÇÃO:\n")
            self.texto_resultado.insert("end", f"Erro: {resultado['erro']}\n")
            if 'solucao_parcial' in resultado:
                 self.texto_resultado.insert("end", f"Solução Parcial: {resultado['solucao_parcial']}\n")