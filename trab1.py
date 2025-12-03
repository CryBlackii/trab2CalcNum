import customtkinter as ctk
from tkinter import messagebox
import math
from bisseccao import bisseccao
from mil import mil
from newton import newton
from secante import secante
from regulaFalsi import regulaFalsi

ROXO_PRIMARIO = "#8A2BE2"
ROXO_HOVER = "#7B1FA2"

def executar_metodos(a, b, x0, x1, delta, n, funcao, phi):
    resultados = {}
    
    try:
        raiz, k, _ = bisseccao(a, b, delta, n, funcao)
        resultados["Bisseção"] = f"{raiz:.8f} ({k} iterações)"
    except Exception as e: resultados["Bisseção"] = f"Erro: {e}"
    
    try:
        raiz, k, _ = mil(x0, delta, n, funcao, phi)
        resultados["MIL"] = f"{raiz:.8f} ({k} iterações)"
    except Exception: resultados["MIL"] = "Erro (Divergiu ou falha no Phi)"
    
    try:
        raiz, k, _ = regulaFalsi(a, b, delta, n, funcao)
        resultados["Regula Falsi"] = f"{raiz:.8f} ({k} iterações)"
    except Exception: resultados["Regula Falsi"] = "Erro"
    
    try:
        raiz, k, _ = newton(x0, delta, n, funcao)
        resultados["Newton"] = f"{raiz:.8f} ({k} iterações)"
    except Exception: resultados["Newton"] = "Erro"
    
    try:
        raiz, k, _ = secante(x0, x1, delta, n, funcao)
        resultados["Secante"] = f"{raiz:.8f} ({k} iterações)"
    except Exception: resultados["Secante"] = "Erro"
    
    return resultados

class InterfaceTrab1(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.criar_interface()

    def criar_interface(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        btn_voltar = ctk.CTkButton(header, text="<< Menu Principal", 
                                 command=lambda: self.controller.mostrar_menu(),
                                 fg_color="transparent", border_width=1, 
                                 text_color="white", hover_color="#444", width=120)
        btn_voltar.pack(side="left")
        
        ctk.CTkLabel(header, text="Zeros de Funções", 
                   font=ctk.CTkFont(size=20, weight="bold")).pack(side="left", padx=20)

        form_frame = ctk.CTkScrollableFrame(self, height=250, fg_color="transparent")
        form_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=5)
        
        self.entradas = {}
        campos = [
            ("Função f(x):", "funcao", "x**3 - 9*x + 3"),
            ("Phi φ(x) (opcional):", "phi", "(x**3 + 3)/9"),
            ("Intervalo a:", "a", "0"),
            ("Intervalo b:", "b", "1"),
            ("Chute Inicial x0:", "x0", "0.5"),
            ("Chute Secundário x1:", "x1", "0.6"),
            ("Erro (delta):", "delta", "0.0001"),
            ("Máx Iterações (n):", "n", "100")
        ]
        
        for i, (label_txt, chave, valor_padrao) in enumerate(campos):
            row = i // 2
            col = (i % 2) * 2
            
            ctk.CTkLabel(form_frame, text=label_txt, font=ctk.CTkFont(weight="bold")).grid(row=row, column=col, padx=10, pady=5, sticky="w")
            
            entry = ctk.CTkEntry(form_frame, width=200)
            entry.insert(0, valor_padrao)
            entry.grid(row=row, column=col+1, padx=10, pady=5, sticky="ew")
            
            self.entradas[chave] = entry

        action_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        
        ctk.CTkLabel(action_frame, text="Executar Método:").pack(side="left", padx=10)
        
        self.var_metodo = ctk.StringVar(value="Todos")
        combo_metodos = ctk.CTkOptionMenu(action_frame, 
                                        values=["Todos", "Bisseção", "Regula Falsi", "Newton", "Secante", "MIL"],
                                        variable=self.var_metodo,
                                        fg_color=ROXO_PRIMARIO, button_color=ROXO_HOVER, button_hover_color=ROXO_HOVER)
        combo_metodos.pack(side="left", padx=10)
        
        ctk.CTkButton(action_frame, text="CALCULAR RAÍZES", command=self.calcular, 
                    fg_color=ROXO_PRIMARIO, hover_color=ROXO_HOVER, width=200).pack(side="right", padx=10)

        res_frame = ctk.CTkFrame(self)
        res_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=(0, 20))
        res_frame.grid_columnconfigure(0, weight=1)
        res_frame.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(res_frame, text="Resultados", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", padx=10, pady=5)
        
        self.texto_resultado = ctk.CTkTextbox(res_frame, font=("Courier New", 12))
        self.texto_resultado.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

    def calcular(self):
        try:
            func_str = self.entradas["funcao"].get()
            phi_str = self.entradas["phi"].get()
            
            try:
                params = {k: float(self.entradas[k].get()) for k in ["a", "b", "x0", "x1", "delta"]}
                params["n"] = int(self.entradas["n"].get())
            except ValueError:
                messagebox.showwarning("Erro", "Verifique se os campos numéricos (a, b, x0...) contêm apenas números válidos (use ponto para decimais).")
                return

            env = {"x": 0, "log": math.log, "log10": math.log10, "sqrt": math.sqrt, 
                   "sin": math.sin, "cos": math.cos, "tan": math.tan, "exp": math.exp, 
                   "pi": math.pi, "e": math.e}

            funcao_lambda = lambda x, expr=func_str: eval(expr, {**env, "x": x})
            phi_lambda = (lambda x, expr=phi_str: eval(expr, {**env, "x": x})) if phi_str else None

            escolha = self.var_metodo.get()
            
            self.texto_resultado.delete("1.0", "end")
            self.texto_resultado.insert("end", f"Calculando {escolha} para f(x) = {func_str}...\n")
            self.texto_resultado.insert("end", "-"*60 + "\n")

            resultados = executar_metodos(params['a'], params['b'], params['x0'], params['x1'], 
                                        params['delta'], params['n'], funcao_lambda, phi_lambda)
            
            for met, res in resultados.items():
                if escolha == "Todos" or escolha == met:
                    self.texto_resultado.insert("end", f"{met:<15} | {res}\n")
            
            self.texto_resultado.insert("end", "-"*60 + "\n")

        except Exception as e:
            messagebox.showerror("Erro Crítico", f"Ocorreu um erro no cálculo:\n{e}\n\nVerifique a sintaxe da função.")