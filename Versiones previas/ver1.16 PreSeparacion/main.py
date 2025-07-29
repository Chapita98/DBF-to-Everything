"""
import tkinter as tk
from interfaz import Aplicacion

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Conversor DBF a Excel")
    root.geometry("700x600")
    Aplicacion(root)
    root.mainloop()
"""
from interfaz import Aplicacion

if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()