import os
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from funciones_conversion import convertir_basico, convertir_avanzado, convertir_total

def seleccionar_archivos():
    archivos = filedialog.askopenfilenames(filetypes=[("Archivos DBF", "*.dbf")])
    for archivo in archivos:
        if archivo not in archivos_seleccionados:
            archivos_seleccionados.append(archivo)
    actualizar_lista_archivos()

def seleccionar_todos():
    for child in lista_archivos.get_children():
        lista_archivos.selection_add(child)

def quitar_archivos():
    archivos_seleccionados.clear()
    lista_archivos.delete(*lista_archivos.get_children())

def actualizar_lista_archivos():
    lista_archivos.delete(*lista_archivos.get_children())
    for archivo in archivos_seleccionados:
        lista_archivos.insert("", "end", values=(archivo,))

def ejecutar_conversion(modo):
    if not archivos_seleccionados:
        messagebox.showwarning("Advertencia", "No se han seleccionado archivos.")
        return

    try:
        for archivo in archivos_seleccionados:
            if modo == "basico":
                convertir_basico(archivo)
            elif modo == "avanzado":
                convertir_avanzado(archivo, formato_opciones())
            elif modo == "total":
                convertir_total(archivo, formato_opciones())
        messagebox.showinfo("Éxito", "Conversión completada.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

def formato_opciones():
    return {
        "centrar": var_centrar.get(),
        "autoajustar": var_autoajustar.get(),
        "negrita": var_negrita.get(),
        "congelar": var_congelar.get(),
        "colores": var_colores.get(),
        "tamano_encabezado": int(var_tamano_encabezado.get()),
        "tamano_datos": int(var_tamano_datos.get())
    }

app = tk.Tk()
app.title("Convertidor DBF a Excel")
app.geometry("1000x600")

frame_opciones = tk.Frame(app)
frame_opciones.pack(side="left", fill="y", padx=10, pady=10)

var_centrar = tk.BooleanVar()
var_autoajustar = tk.BooleanVar()
var_negrita = tk.BooleanVar()
var_congelar = tk.BooleanVar()
var_colores = tk.BooleanVar()
var_tamano_encabezado = tk.StringVar(value="12")
var_tamano_datos = tk.StringVar(value="10")

tk.Checkbutton(frame_opciones, text="Centrar texto", variable=var_centrar).pack(anchor="w")
tk.Checkbutton(frame_opciones, text="Autoajustar columnas", variable=var_autoajustar).pack(anchor="w")
tk.Checkbutton(frame_opciones, text="Encabezado en negrita", variable=var_negrita).pack(anchor="w")
tk.Checkbutton(frame_opciones, text="Congelar fila 1", variable=var_congelar).pack(anchor="w")
tk.Checkbutton(frame_opciones, text="Colores alternados", variable=var_colores).pack(anchor="w")

tk.Label(frame_opciones, text="Tamaño encabezado:").pack(anchor="w")
tk.Entry(frame_opciones, textvariable=var_tamano_encabezado, width=5).pack(anchor="w")

tk.Label(frame_opciones, text="Tamaño datos:").pack(anchor="w")
tk.Entry(frame_opciones, textvariable=var_tamano_datos, width=5).pack(anchor="w")

tk.Button(frame_opciones, text="Seleccionar archivos", command=seleccionar_archivos).pack(fill="x", pady=5)
tk.Button(frame_opciones, text="Seleccionar todos", command=seleccionar_todos).pack(fill="x", pady=5)
tk.Button(frame_opciones, text="Quitar archivos", command=quitar_archivos).pack(fill="x", pady=5)

tk.Button(frame_opciones, text="Convertir Básico", command=lambda: ejecutar_conversion("basico")).pack(fill="x", pady=5)
tk.Button(frame_opciones, text="Convertir Avanzado", command=lambda: ejecutar_conversion("avanzado")).pack(fill="x", pady=5)
tk.Button(frame_opciones, text="Convertir Total", command=lambda: ejecutar_conversion("total")).pack(fill="x", pady=5)

frame_tabla = tk.Frame(app)
frame_tabla.pack(side="right", fill="both", expand=True, padx=10, pady=10)

columnas = ("Archivo",)
lista_archivos = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
lista_archivos.heading("Archivo", text="Archivo DBF")
lista_archivos.pack(fill="both", expand=True)

archivos_seleccionados = []

app.mainloop()
