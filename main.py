import customtkinter as ctk
import trab1
import trab2

ROXO_PRIMARIO = "#8A2BE2"
ROXO_HOVER = "#7B1FA2"
ROXO_ESCURO = "#4B0082"
ROXO_ESCURO_HOVER = "#3A0062"

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        
        self.title("Sistema Integrado de Cálculo Numérico")
        self.geometry("1000x750")
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.container = ctk.CTkFrame(self)
        self.container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        self.criar_menu_principal()
        self.mostrar_menu()

    def criar_menu_principal(self):
        frame_menu = ctk.CTkFrame(self.container)
        frame_menu.grid(row=0, column=0, sticky="nsew")
        self.frames["Menu"] = frame_menu
        
        frame_menu.grid_rowconfigure((0, 5), weight=1)
        frame_menu.grid_columnconfigure((0, 2), weight=1)
        
        ctk.CTkLabel(frame_menu, text="Trabalho de calculo numerico 2", 
                   font=ctk.CTkFont(size=32, weight="bold")).grid(row=1, column=1, pady=(0, 10))
        
        ctk.CTkLabel(frame_menu, text="Escolha os metodos", 
                   font=ctk.CTkFont(size=16)).grid(row=2, column=1, pady=(0, 30))
        
        ctk.CTkButton(frame_menu, 
                    text="Metodos do cap 2", 
                    font=ctk.CTkFont(size=18), height=80, corner_radius=15,
                    fg_color=ROXO_PRIMARIO, hover_color=ROXO_HOVER,
                    command=self.iniciar_trab1).grid(row=3, column=1, padx=50, pady=15, sticky="ew")
        
        ctk.CTkButton(frame_menu, 
                    text="Metodos do cap 3", 
                    font=ctk.CTkFont(size=18), height=80, corner_radius=15,
                    fg_color=ROXO_ESCURO, hover_color=ROXO_ESCURO_HOVER,
                    command=self.iniciar_trab2).grid(row=4, column=1, padx=50, pady=15, sticky="ew")
        
    def mostrar_menu(self):
        self.frames["Menu"].tkraise()

    def iniciar_trab1(self):
        if "Trab1" not in self.frames:
            self.frames["Trab1"] = trab1.InterfaceTrab1(self.container, self)
            self.frames["Trab1"].grid(row=0, column=0, sticky="nsew")
        self.frames["Trab1"].tkraise()

    def iniciar_trab2(self):
        if "Trab2" not in self.frames:
            self.frames["Trab2"] = trab2.InterfaceTrab2(self.container, self)
            self.frames["Trab2"].grid(row=0, column=0, sticky="nsew")
        self.frames["Trab2"].tkraise()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()