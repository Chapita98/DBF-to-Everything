import tkinter as tk
from tkinter import messagebox
import sys
from interfaz import Aplicacion

class MenuPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Menú de Programas")
        self.resizable(False, False)
        self.centrar_ventana(400, 400)
        self.crear_widgets()

    def centrar_ventana(self, ancho, alto):
        self.update_idletasks()
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()
        x = (pantalla_ancho // 2) - (ancho // 2)
        y = (pantalla_alto // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def crear_widgets(self):
        frame = tk.Frame(self)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        button_style = {
            "width": 12,
            "height": 4,
            "font": ("Arial", 14, "bold"),
            "bg": "#4A90E2",
            "fg": "white",
            "activebackground": "#357ABD",
            "activeforeground": "white",
            "bd": 2,
            "relief": "raised"
        }

        btn1 = tk.Button(frame, text="Dbf to Excel", command=self.abrir_dfb_to_excel, **button_style)
        btn2 = tk.Button(frame, text="Programa 2", state="disabled", **button_style)
        btn3 = tk.Button(frame, text="Programa 3", state="disabled", **button_style)
        btn4 = tk.Button(frame, text="Programa 4", state="disabled", **button_style)

        btn1.grid(row=0, column=0, padx=10, pady=10)
        btn2.grid(row=0, column=1, padx=10, pady=10)
        btn3.grid(row=1, column=0, padx=10, pady=10)
        btn4.grid(row=1, column=1, padx=10, pady=10)

    def abrir_dfb_to_excel(self):
        self.destroy()
        app = Aplicacion(menu_callback=mostrar_menu)
        app.mainloop()

def mostrar_menu():
    menu = MenuPrincipal()
    menu.mainloop()

if __name__ == "__main__":
    mostrar_menu()