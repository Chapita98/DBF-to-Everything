import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from funciones_conversion import convertir_basico, convertir_avanzado, convertir_total

def seleccionar_archivos():
    archivos = filedialog.askopenfilenames(filetypes=[("Archivos DBF", "*.dbf")])
    for archivo in archivos:
        if archivo not in archivos_seleccionados:
            archivos_seleccionados.append(archivo)
            tabla.insert("", "end", values=(os.path.basename(archivo), archivo))

def seleccionar_todos():
    for fila in tabla.get_children():
        tabla.selection_add(fila)

def eliminar_seleccionados():
    for fila in tabla.selection():
        valores = tabla.item(fila, "values")
        archivos_seleccionados.remove(valores[1])
        tabla.delete(fila)

def limpiar_lista():
    archivos_seleccionados.clear()
    for fila in tabla.get_children():
        tabla.delete(fila)

def ejecutar_conversion(modo):
    if not archivos_seleccionados:
        messagebox.showwarning("Advertencia", "No se han seleccionado archivos.")
        return

    carpeta_salida = filedialog.askdirectory()
    if not carpeta_salida:
        return

    opciones = {
        "centrar": centrar_texto.get(),
        "colores": colores_alternados.get(),
        "negrita": encabezado_negrita.get(),
        "tamano_encabezado": tamano_encabezado.get(),
        "tamano_datos": tamano_datos.get(),
        "inmovilizar": inmovilizar_fila.get(),
        "ajustar": autoajustar_columnas.get()
    }

    try:
        if modo == "b":
            convertir_basico(archivos_seleccionados, carpeta_salida)
        elif modo == "a":
            convertir_avanzado(archivos_seleccionados, carpeta_salida, opciones)
        elif modo == "t":
            convertir_total(archivos_seleccionados, carpeta_salida, opciones)
        messagebox.showinfo("Éxito", "Conversión completada correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

ventana = tk.Tk()
ventana.title("Convertidor DBF a Excel")
ventana.geometry("1000x600")

archivos_seleccionados = []

frame_opciones = tk.Frame(ventana)
frame_opciones.pack(side="left", fill="y", padx=10, pady=10)

# Opciones de formato
centrar_texto = tk.BooleanVar()
colores_alternados = tk.BooleanVar()
encabezado_negrita = tk.BooleanVar()
inmovilizar_fila = tk.BooleanVar()
autoajustar_columnas = tk.BooleanVar()
tamano_encabezado = tk.IntVar(value=12)
tamano_datos = tk.IntVar(value=11)

tk.Checkbutton(frame_opciones, text="Centrar texto", variable=centrar_texto).pack(anchor="w")
tk.Checkbutton(frame_opciones, text="Colores alternados", variable=colores_alternados).pack(anchor="w")
tk.Checkbutton(frame_opciones, text="Encabezado en negrita", variable=encabezado_negrita).pack(anchor="w")
tk.Checkbutton(frame_opciones, text="Inmovilizar fila 1", variable=inmovilizar_fila).pack(anchor="w")
tk.Checkbutton(frame_opciones, text="Autoajustar columnas", variable=autoajustar_columnas).pack(anchor="w")

tk.Label(frame_opciones, text="Tamaño encabezado").pack(anchor="w")
tk.Spinbox(frame_opciones, from_=8, to=20, textvariable=tamano_encabezado).pack(anchor="w")

tk.Label(frame_opciones, text="Tamaño datos").pack(anchor="w")
tk.Spinbox(frame_opciones, from_=8, to=20, textvariable=tamano_datos).pack(anchor="w")

# Botones de acción
tk.Button(frame_opciones, text="Agregar archivos", command=seleccionar_archivos).pack(fill="x", pady=2)
tk.Button(frame_opciones, text="Seleccionar todos", command=seleccionar_todos).pack(fill="x", pady=2)
tk.Button(frame_opciones, text="Eliminar seleccionados", command=eliminar_seleccionados).pack(fill="x", pady=2)
tk.Button(frame_opciones, text="Limpiar lista", command=limpiar_lista).pack(fill="x", pady=2)

tk.Label(frame_opciones, text="Modo de conversión").pack(pady=5)
tk.Button(frame_opciones, text="Básico", command=lambda: ejecutar_conversion("b")).pack(fill="x", pady=2)
tk.Button(frame_opciones, text="Avanzado", command=lambda: ejecutar_conversion("a")).pack(fill="x", pady=2)
tk.Button(frame_opciones, text="Total", command=lambda: ejecutar_conversion("t")).pack(fill="x", pady=2)

# Tabla
frame_tabla = tk.Frame(ventana)
frame_tabla.pack(side="left", fill="both", expand=True, padx=10, pady=10)

tabla = ttk.Treeview(frame_tabla, columns=("Nombre", "Ruta"), show="headings")
tabla.heading("Nombre", text="Nombre del archivo")
tabla.heading("Ruta", text="Ruta completa")
tabla.pack(fill="both", expand=True)

ventana.mainloop()
