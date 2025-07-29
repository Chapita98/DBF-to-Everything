import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from funciones_conversion import convertir_basico, convertir_avanzado, convertir_total
from schema_extractor import extraer_schema

archivos_seleccionados = []
ruta_salida = ""

def seleccionar_archivos(entry, callback=None):
    rutas = filedialog.askopenfilenames(filetypes=[("Archivos DBF", "*.dbf")])
    if rutas:
        archivos_seleccionados.clear()
        archivos_seleccionados.extend(rutas)
        entry.config(state="normal")
        entry.delete(0, tk.END)
        entry.insert(0, "; ".join(rutas))
        entry.config(state="readonly")
        if callback:
            callback()

def seleccionar_directorio(entry, callback=None):
    global ruta_salida
    ruta = filedialog.askdirectory()
    if ruta:
        ruta_salida = ruta
        entry.config(state="normal")
        entry.delete(0, tk.END)
        entry.insert(0, ruta)
        entry.config(state="readonly")
        if callback:
            callback(ruta)

def crear_interfaz(root):
    tab_control = ttk.Notebook(root)

    tab_basico = ttk.Frame(tab_control)
    tab_avanzado = ttk.Frame(tab_control)
    tab_total = ttk.Frame(tab_control)
    tab_schema = ttk.Frame(tab_control)  # Nueva pestaña para extraer schema

    tab_control.add(tab_basico, text="Básico")
    tab_control.add(tab_avanzado, text="Avanzado")
    tab_control.add(tab_total, text="Total")
    tab_control.add(tab_schema, text="Extraer Schema")  # Añadida al final
    tab_control.pack(expand=1, fill="both")

    def construir_tab_con_tabla(tab, incluir_personalizacion=False, es_schema=False):
        frm_top = tk.Frame(tab)
        frm_top.pack(fill="x", pady=5)

        if es_schema:
            tk.Label(frm_top, text="Carpeta de entrada:").grid(row=0, column=0, sticky="e")
            entrada_entrada = tk.Entry(frm_top, state="readonly", width=80)
            entrada_entrada.grid(row=0, column=1, padx=5)
            def seleccionar_y_actualizar():
                seleccionar_directorio(entrada_entrada, lambda ruta: actualizar_tabla(ruta))
            tk.Button(frm_top, text="Seleccionar...", command=seleccionar_y_actualizar).grid(row=0, column=2)
        else:
            tk.Label(frm_top, text="Archivos DBF:").grid(row=0, column=0, sticky="e")
            entrada_archivos = tk.Entry(frm_top, state="readonly", width=80)
            entrada_archivos.grid(row=0, column=1, padx=5)
            tk.Button(frm_top, text="Seleccionar...", command=lambda: seleccionar_archivos(entrada_archivos, lambda: actualizar_tabla())).grid(row=0, column=2)

        tk.Label(frm_top, text="Carpeta de salida:").grid(row=1, column=0, sticky="e")
        entrada_salida = tk.Entry(frm_top, state="readonly", width=80)
        entrada_salida.grid(row=1, column=1, padx=5)
        tk.Button(frm_top, text="Seleccionar...", command=lambda: seleccionar_directorio(entrada_salida)).grid(row=1, column=2)

        frm_abajo = tk.Frame(tab)
        frm_abajo.pack(expand=1, fill="both", pady=5)

        frm_opciones = tk.Frame(frm_abajo)
        frm_opciones.pack(side="left", fill="y", padx=5)

        if incluir_personalizacion and not es_schema:
            opciones = {
                "centrar_texto": tk.BooleanVar(value=True),
                "color_alternado": tk.BooleanVar(value=True),
                "negrita": tk.BooleanVar(value=True),
                "inmovilizar": tk.BooleanVar(value=True),
                "autocolumnas": tk.BooleanVar(value=True),
                "tamano_encabezado": tk.IntVar(value=12),
                "tamano_datos": tk.IntVar(value=10)
            }
            tk.Checkbutton(frm_opciones, text="Centrar texto", variable=opciones["centrar_texto"]).pack(anchor="w")
            tk.Checkbutton(frm_opciones, text="Colores alternados", variable=opciones["color_alternado"]).pack(anchor="w")
            tk.Checkbutton(frm_opciones, text="Encabezado en negrita", variable=opciones["negrita"]).pack(anchor="w")
            tk.Checkbutton(frm_opciones, text="Inmovilizar fila 1", variable=opciones["inmovilizar"]).pack(anchor="w")
            tk.Checkbutton(frm_opciones, text="Autoajustar columnas", variable=opciones["autocolumnas"]).pack(anchor="w")
            tk.Label(frm_opciones, text="Tamaño encabezado").pack(anchor="w")
            tk.Spinbox(frm_opciones, from_=8, to=20, textvariable=opciones["tamano_encabezado"]).pack(fill="x")
            tk.Label(frm_opciones, text="Tamaño datos").pack(anchor="w")
            tk.Spinbox(frm_opciones, from_=8, to=20, textvariable=opciones["tamano_datos"]).pack(fill="x")

        frm_tabla = tk.Frame(frm_abajo)
        frm_tabla.pack(side="left", expand=1, fill="both")

        tabla = ttk.Treeview(frm_tabla, columns=("Nombre", "Ruta"), show="headings")
        tabla.heading("Nombre", text="Nombre del archivo")
        tabla.heading("Ruta", text="Ruta completa")
        tabla.pack(expand=1, fill="both")

        if es_schema:
            lbl_total = tk.Label(frm_abajo, text="0 archivos totales")
            lbl_total.pack(side="bottom", anchor="w", padx=5)
            lbl_seleccionados = tk.Label(frm_abajo, text="0 archivos seleccionados")
            lbl_seleccionados.pack(side="bottom", anchor="e", padx=5)

            def actualizar_seleccion(event):
                seleccionados = len(tabla.selection())
                lbl_seleccionados.config(text=f"{seleccionados} archivos seleccionados")
            tabla.bind("<<TreeviewSelect>>", actualizar_seleccion)

        frm_botones = tk.Frame(tab)
        frm_botones.pack(fill="x", pady=5)

        def actualizar_tabla(ruta_entrada=None):
            tabla.delete(*tabla.get_children())
            if es_schema and ruta_entrada:
                try:
                    archivos_dbf = [f for f in os.listdir(ruta_entrada) if f.lower().endswith('.dbf')]
                    for archivo in archivos_dbf:
                        ruta_completa = os.path.join(ruta_entrada, archivo)
                        tabla.insert("", "end", values=(archivo, ruta_completa))
                    if es_schema:
                        lbl_total.config(text=f"{len(archivos_dbf)} archivos totales")
                        lbl_seleccionados.config(text="0 archivos seleccionados")
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo listar archivos: {e}")
            elif not es_schema:
                for ruta in archivos_seleccionados:
                    nombre = os.path.basename(ruta)
                    tabla.insert("", "end", values=(nombre, ruta))

        def seleccionar_todo():
            for item in tabla.get_children():
                tabla.selection_add(item)
            if es_schema:
                actualizar_seleccion(None)

        def limpiar_lista():
            if es_schema:
                tabla.delete(*tabla.get_children())
                if 'lbl_total' in locals():
                    lbl_total.config(text="0 archivos totales")
                    lbl_seleccionados.config(text="0 archivos seleccionados")
            else:
                archivos_seleccionados.clear()
                entrada_archivos.config(state="normal")
                entrada_archivos.delete(0, tk.END)
                entrada_archivos.config(state="readonly")
                tabla.delete(*tabla.get_children())

        if es_schema:
            def extraer():
                if not entrada_entrada.get() or not entrada_salida.get():
                    messagebox.showerror("Error", "Debes seleccionar carpetas de entrada y salida.")
                    return
                seleccionados = [tabla.item(i)['values'][1] for i in tabla.selection()]
                if not seleccionados:
                    messagebox.showerror("Error", "Debes seleccionar al menos un archivo.")
                    return
                for ruta in seleccionados:
                    nombre = os.path.splitext(os.path.basename(ruta))[0] + "_schema.txt"
                    ruta_destino = os.path.join(entrada_salida.get(), nombre)
                    extraer_schema(ruta, ruta_destino)
                messagebox.showinfo("Éxito", "Esquemas extraídos correctamente.")
            action_text = "Extraer Schema"
            action = extraer
        else:
            if incluir_personalizacion:
                def convertir():
                    if not archivos_seleccionados or not ruta_salida:
                        messagebox.showerror("Error", "Debes seleccionar archivos y carpeta de salida.")
                        return
                    for ruta in archivos_seleccionados:
                        nombre = os.path.splitext(os.path.basename(ruta))[0] + ".xlsx"
                        ruta_destino = os.path.join(ruta_salida, nombre)
                        convertir_avanzado(ruta, ruta_destino, {
                            "centrar_texto": opciones["centrar_texto"].get(),
                            "color_alternado": opciones["color_alternado"].get(),
                            "negrita": opciones["negrita"].get(),
                            "inmovilizar_fila_1": opciones["inmovilizar"].get(),
                            "autocolumnas": opciones["autocolumnas"].get(),
                            "tamano_encabezado": opciones["tamano_encabezado"].get(),
                            "tamano_datos": opciones["tamano_datos"].get()
                        })
                    messagebox.showinfo("Éxito", "Conversión avanzada finalizada.")
            else:
                def convertir():
                    if not archivos_seleccionados or not ruta_salida:
                        messagebox.showerror("Error", "Debes seleccionar archivos y carpeta de salida.")
                        return
                    for ruta in archivos_seleccionados:
                        nombre = os.path.splitext(os.path.basename(ruta))[0] + ".xlsx"
                        ruta_destino = os.path.join(ruta_salida, nombre)
                        convertir_basico(ruta, ruta_destino)
                    messagebox.showinfo("Éxito", "Conversión básica finalizada.")
            action_text = "Convertir"
            action = convertir

        tk.Button(frm_botones, text="Seleccionar todo", command=seleccionar_todo).pack(side="left", padx=5)
        tk.Button(frm_botones, text="Limpiar lista", command=limpiar_lista).pack(side="left", padx=5)
        tk.Button(frm_botones, text=action_text, command=action).pack(side="right", padx=5)

    def construir_tab_total(tab):
        frm_top = tk.Frame(tab)
        frm_top.pack(fill="x", pady=5)

        tk.Label(frm_top, text="Archivos DBF: ").grid(row=0, column=0, sticky="e")
        entrada_archivos = tk.Entry(frm_top, state="readonly", width=80)
        entrada_archivos.grid(row=0, column=1, padx=5)
        tk.Button(frm_top, text="Seleccionar...", command=lambda: seleccionar_archivos(entrada_archivos)).grid(row=0, column=2)

        tk.Label(frm_top, text="Carpeta de salida: ").grid(row=1, column=0, sticky="e")
        entrada_salida = tk.Entry(frm_top, state="readonly", width=80)
        entrada_salida.grid(row=1, column=1, padx=5)
        tk.Button(frm_top, text="Seleccionar...", command=lambda: seleccionar_directorio(entrada_salida)).grid(row=1, column=2)

        opciones = {
            "centrar_texto": tk.BooleanVar(value=True),
            "color_alternado": tk.BooleanVar(value=True),
            "negrita": tk.BooleanVar(value=True),
            "inmovilizar": tk.BooleanVar(value=True),
            "autocolumnas": tk.BooleanVar(value=True),
            "tamano_encabezado": tk.IntVar(value=12),
            "tamano_datos": tk.IntVar(value=10)
        }

        frm_opciones = tk.Frame(tab)
        frm_opciones.pack(side="left", fill="y", padx=5, pady=5)

        tk.Checkbutton(frm_opciones, text="Centrar texto", variable=opciones["centrar_texto"]).pack(anchor="w")
        tk.Checkbutton(frm_opciones, text="Colores alternados", variable=opciones["color_alternado"]).pack(anchor="w")
        tk.Checkbutton(frm_opciones, text="Encabezado en negrita", variable=opciones["negrita"]).pack(anchor="w")
        tk.Checkbutton(frm_opciones, text="Inmovilizar fila 1", variable=opciones["inmovilizar"]).pack(anchor="w")
        tk.Checkbutton(frm_opciones, text="Autoajustar columnas", variable=opciones["autocolumnas"]).pack(anchor="w")

        tk.Label(frm_opciones, text="Tamaño encabezado").pack(anchor="w")
        tk.Spinbox(frm_opciones, from_=8, to=20, textvariable=opciones["tamano_encabezado"]).pack(fill="x")

        tk.Label(frm_opciones, text="Tamaño datos").pack(anchor="w")
        tk.Spinbox(frm_opciones, from_=8, to=20, textvariable=opciones["tamano_datos"]).pack(fill="x")

        def convertir():
            if not archivos_seleccionados or not ruta_salida:
                messagebox.showerror("Error", "Debes seleccionar archivos y carpeta de salida.")
                return
            convertir_total(archivos_seleccionados, ruta_salida, {
                "centrar_texto": opciones["centrar_texto"].get(),
                "color_alternado": opciones["color_alternado"].get(),
                "negrita": opciones["negrita"].get(),
                "inmovilizar_fila_1": opciones["inmovilizar"].get(),
                "autocolumnas": opciones["autocolumnas"].get(),
                "tamano_encabezado": opciones["tamano_encabezado"].get(),
                "tamano_datos": opciones["tamano_datos"].get()
            })
            messagebox.showinfo("Éxito", "Conversión total finalizada.")

        tk.Button(tab, text="Convertir todo", command=convertir).pack(side="right", padx=10, pady=10)

    construir_tab_con_tabla(tab_basico, incluir_personalizacion=False, es_schema=False)
    construir_tab_con_tabla(tab_avanzado, incluir_personalizacion=True, es_schema=False)
    construir_tab_total(tab_total)
    construir_tab_con_tabla(tab_schema, incluir_personalizacion=False, es_schema=True)