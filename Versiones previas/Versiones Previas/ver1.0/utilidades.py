import tkinter as tk
from interfaz import crear_interfaz

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Convertidor DBF a Excel v0.9")
    root.geometry("1000x600")
    crear_interfaz(root)
    root.mainloop()
