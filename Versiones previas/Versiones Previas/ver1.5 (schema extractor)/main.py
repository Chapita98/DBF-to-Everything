import tkinter as tk
from interfaz import crear_interfaz

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Conversor DBF a Excel")
    root.geometry("1100x600")
    crear_interfaz(root)
    root.mainloop()
