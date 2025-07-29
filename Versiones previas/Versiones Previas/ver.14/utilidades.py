import os
import tkinter as tk
from tkinter import filedialog

def seleccionar_archivos():
    rutas = filedialog.askopenfilenames(
        title="Seleccionar archivos DBF",
        filetypes=[("Archivos DBF", "*.dbf")],
        initialdir=os.getcwd()
    )
    return list(rutas)

def seleccionar_carpeta_destino():
    return filedialog.askdirectory(title="Seleccionar carpeta de destino")

def obtener_nombre_archivo_sin_extension(ruta_archivo):
    return os.path.splitext(os.path.basename(ruta_archivo))[0]
