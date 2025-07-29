import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys


# Ruta al programa principal
RUTA_DBF_TO_EXCEL = os.path.join(os.path.dirname(__file__), "main.py")


def lanzar_dfb_to_excel():
    try:
        root.destroy()  # Cierra el menú antes de abrir el programa
        exe = sys.executable
        subprocess.Popen([exe, RUTA_DBF_TO_EXCEL])
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el programa:\n{e}")

root = tk.Tk()
root.title("Menú de Programas")
root.geometry("400x400")
root.resizable(False, False)

# Centrar los botones en un grid 2x2
frame = tk.Frame(root)
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

# Botón funcional
btn1 = tk.Button(frame, text="Dbf to Excel", command=lanzar_dfb_to_excel, **button_style)

# Botones de ejemplo (deshabilitados)
btn2 = tk.Button(frame, text="Programa 2", state="disabled", **button_style)
btn3 = tk.Button(frame, text="Programa 3", state="disabled", **button_style)
btn4 = tk.Button(frame, text="Programa 4", state="disabled", **button_style)

# Distribución en cuadrado
btn1.grid(row=0, column=0, padx=10, pady=10)
btn2.grid(row=0, column=1, padx=10, pady=10)
btn3.grid(row=1, column=0, padx=10, pady=10)
btn4.grid(row=1, column=1, padx=10, pady=10)

root.mainloop()