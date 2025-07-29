import tkinter as tk
from tkinter import ttk, filedialog
from funciones_conversion import convertir_basico, convertir_avanzado, convertir_total
from utilidades import personalizar_excel, actualizar_tabla_archivos, obtener_archivos_dbf
import os

def crear_interfaz(root):
    # Marco principal
    marco = tk.Frame(root)
    marco.pack(fill="both", expand=True)

    # Tabla de archivos
    columnas = ("Archivo", "Ruta")
    tabla = ttk.Treeview(marco, columns=columnas, show="headings")
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="w")
    tabla.pack(side="right", fill="both", expand=True)

    # Panel lateral con opciones
    panel_opciones = tk.Frame(marco)
    panel_opciones.pack(side="left", fill="y")

    # Botones
    def seleccionar_carpeta():
        carpeta = filedialog.askdirectory()
        if carpeta:
            archivos = obtener_archivos_dbf(carpeta)
            actualizar_tabla_archivos(tabla, archivos)

    def seleccionar_todos():
        for item in tabla.get_children():
            tabla.selection_add(item)

    def ejecutar_conversion(funcion_conversion):
        seleccionados = tabla.selection()
        archivos = [tabla.item(i)["values"][1] for i in seleccionados]
        for archivo in archivos:
            funcion_conversion(archivo)

    # Botones y opciones
    btn_carpeta = tk.Button(panel_opciones, text="Seleccionar Carpeta", command=seleccionar_carpeta)
    btn_todos = tk.Button(panel_opciones, text="Seleccionar Todos", command=seleccionar_todos)
    btn_basico = tk.Button(panel_opciones, text="Convertir Básico", command=lambda: ejecutar_conversion(convertir_basico))
    btn_avanzado = tk.Button(panel_opciones, text="Convertir Avanzado", command=lambda: ejecutar_conversion(convertir_avanzado))
    btn_total = tk.Button(panel_opciones, text="Convertir Total", command=lambda: ejecutar_conversion(convertir_total))

    # Empaquetar botones
    for btn in [btn_carpeta, btn_todos, btn_basico, btn_avanzado, btn_total]:
        btn.pack(padx=10, pady=5, fill="x")
