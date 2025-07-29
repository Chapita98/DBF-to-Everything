import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from schema_extractor import convertir_tipo_dbf_a_sql, extraer_schema
from funciones_conversion import convertir_basico, convertir_avanzado, convertir_total, guardar_dataframe_como_csv
from utilidades import obtener_archivos_dbf_en_carpeta

class Aplicacion(tk.Tk):
    def __init__(self, menu_callback=None):
        super().__init__()
        from utilidades import centrar_ventana
        self.menu_callback = menu_callback
        self.title("DBF a Excel")
        self.resizable(False, False)
        centrar_ventana(self, 700, 600)

        self.ruta_entrada = tk.StringVar()
        self.ruta_salida = tk.StringVar()

        self.opciones = {
            "centrar_texto": tk.BooleanVar(value=True),
            "color_alternado": tk.BooleanVar(value=True),
            "negrita": tk.BooleanVar(value=True),
            "inmovilizar_fila_1": tk.BooleanVar(value=True),
            "autocolumnas": tk.BooleanVar(value=True),
            "tamano_encabezado": tk.IntVar(value=12),
            "tamano_datos": tk.IntVar(value=10),
            "quitar_x": tk.BooleanVar(value=False)
        }

        self.archivos_seleccionados = []

        self.crear_widgets()

    def crear_widgets(self):
        # Botón Salir arriba a la derecha
        top_frame = tk.Frame(self)
        top_frame.pack(fill=tk.X)
        salir_btn = tk.Button(top_frame, text="Salir", command=self.volver_al_menu)
        salir_btn.pack(side=tk.RIGHT, padx=10, pady=5)

        # Ahora las pestañas
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill=tk.BOTH, expand=True)

        self.tab_basico = ttk.Frame(self.tabs)
        self.tab_avanzado = ttk.Frame(self.tabs)
        self.tab_total = ttk.Frame(self.tabs)
        self.tab_extraer_schema = ttk.Frame(self.tabs)
        self.tab_csv = ttk.Frame(self.tabs)

        self.tabs.add(self.tab_basico, text="Modo Básico")
        self.tabs.add(self.tab_avanzado, text="Modo Avanzado")
        self.tabs.add(self.tab_total, text="Convertir Todo")
        self.tabs.add(self.tab_total, text="Extraer Schema")
        self.tabs.add(self.tab_csv, text="Convertir a csv")

        for tab in (self.tab_basico, self.tab_avanzado, self.tab_total, self.tab_extraer_schema, self.tab_csv):
            self.crear_selector_rutas(tab)

        self.crear_tabla_archivos(self.tab_basico)
        self.crear_tabla_archivos(self.tab_avanzado)
        self.crear_tabla_archivos(self.tab_extraer_schema)
        self.crear_tabla_archivos(self.tab_csv)
        self.crear_personalizacion(self.tab_avanzado)
        self.crear_personalizacion(self.tab_total, incluir_tabla=False)

        self.crear_botones_conversion()

    def crear_selector_rutas(self, tab):
        frame = tk.Frame(tab)
        frame.pack(pady=10, fill=tk.X)

        # Selector de entrada
        frame_entrada = tk.Frame(frame)
        frame_entrada.pack(fill=tk.X, pady=2)
        tk.Label(frame_entrada, text="Carpeta de Entrada:").pack(side=tk.LEFT, padx=5)
        tk.Entry(frame_entrada, textvariable=self.ruta_entrada, width=40).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_entrada, text="Seleccionar Carpeta", command=self.seleccionar_entrada).pack(side=tk.LEFT)

        # Selector de salida
        frame_salida = tk.Frame(frame)
        frame_salida.pack(fill=tk.X, pady=2)
        tk.Label(frame_salida, text="Carpeta de Salida:").pack(side=tk.LEFT, padx=5)
        tk.Entry(frame_salida, textvariable=self.ruta_salida, width=40).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_salida, text="Seleccionar Carpeta", command=self.seleccionar_salida).pack(side=tk.LEFT)

    def crear_tabla_archivos(self, tab):
        frame = tk.Frame(tab)
        frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        self.tree = ttk.Treeview(frame, columns=("Archivo",), show="headings", selectmode="extended")
        self.tree.heading("Archivo", text="Archivo DBF")
        self.tree.pack(fill=tk.BOTH, expand=True)

        botones = tk.Frame(tab)
        botones.pack(side=tk.LEFT, padx=20, pady=10)

        tk.Button(botones, text="Cargar Archivos", command=self.cargar_archivos).pack(pady=5)
        tk.Button(botones, text="Seleccionar Todo", command=self.seleccionar_todo).pack(pady=5)
        tk.Button(botones, text="Limpiar Lista", command=self.limpiar_lista).pack(pady=5)

    def crear_personalizacion(self, tab, incluir_tabla=True):
        frame = tk.LabelFrame(tab, text="Opciones de Personalización")
        frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

        tk.Checkbutton(frame, text="Centrar Texto", variable=self.opciones["centrar_texto"]).pack(anchor="w")
        tk.Checkbutton(frame, text="Color Alternado en Encabezado", variable=self.opciones["color_alternado"]).pack(anchor="w")
        tk.Checkbutton(frame, text="Inmovilizar Fila 1", variable=self.opciones["inmovilizar_fila_1"]).pack(anchor="w")
        tk.Checkbutton(frame, text="Ajustar Ancho de Columnas", variable=self.opciones["autocolumnas"]).pack(anchor="w")
        tk.Checkbutton(frame, text="Quitar letra 'x' inicial en nombres", variable=self.opciones["quitar_x"]).pack(anchor="w")

        tk.Label(frame, text="Tamaño de encabezado:").pack()
        tk.Spinbox(frame, from_=8, to=24, textvariable=self.opciones["tamano_encabezado"]).pack()

        tk.Label(frame, text="Tamaño de datos:").pack()
        tk.Spinbox(frame, from_=8, to=24, textvariable=self.opciones["tamano_datos"]).pack()

    def crear_botones_conversion(self):
        frame = tk.Frame(self)
        frame.pack(pady=10)

        tk.Button(frame, text="Convertir", command=self.convertir_basico).pack(side=tk.RIGHT, padx=10)
        tk.Button(frame, text="Seleccionar Todo", command=self.seleccionar_todo).pack(side=tk.LEFT, padx=10)
        tk.Button(frame, text="Limpiar Lista", command=self.limpiar_lista).pack(side=tk.LEFT, padx=15)

    def seleccionar_entrada(self):
        carpeta = filedialog.askdirectory()
        if carpeta:
            self.ruta_entrada.set(carpeta)
            self.cargar_archivos()

    def seleccionar_salida(self):
        carpeta = filedialog.askdirectory()
        if carpeta:
            self.ruta_salida.set(carpeta)

    def cargar_archivos(self):
        self.tree.delete(*self.tree.get_children())
        self.archivos_seleccionados = []

        carpeta = self.ruta_entrada.get()
        if not carpeta or not os.path.isdir(carpeta):
            return

        archivos = obtener_archivos_dbf_en_carpeta(carpeta)
        for archivo in archivos:
            self.tree.insert("", tk.END, values=(archivo,))
        self.archivos_seleccionados = archivos

    def seleccionar_todo(self):
        for item in self.tree.get_children():
            self.tree.selection_add(item)

    def limpiar_lista(self):
        self.tree.delete(*self.tree.get_children())
        self.archivos_seleccionados = []

    def convertir_basico(self):
        salida = self.ruta_salida.get()
        for item in self.tree.selection():
            archivo = self.tree.item(item)["values"][0]
            convertir_basico(os.path.join(self.ruta_entrada.get(), archivo), salida, self.opciones["quitar_x"].get())
        messagebox.showinfo("Completado", "Conversión básica finalizada.")

    def convertir_avanzado(self):
        salida = self.ruta_salida.get()
        for item in self.tree.selection():
            archivo = self.tree.item(item)["values"][0]
            convertir_avanzado(os.path.join(self.ruta_entrada.get(), archivo), salida, self.obtener_opciones())
        messagebox.showinfo("Completado", "Conversión avanzada finalizada.")

    def convertir_total(self):
        ruta = self.ruta_entrada.get()
        archivos = obtener_archivos_dbf_en_carpeta(ruta)
        if not archivos:
            messagebox.showwarning("Sin archivos", "No hay archivos DBF en la carpeta.")
            return
        lista_completa = [os.path.join(ruta, archivo) for archivo in archivos]
        convertir_total(lista_completa, self.ruta_salida.get(), self.obtener_opciones())
        messagebox.showinfo("Completado", "Conversión total de la carpeta finalizada.")

    def obtener_opciones(self):
        return {clave: var.get() for clave, var in self.opciones.items()}
    
    def volver_al_menu(self):
        self.destroy()
        if self.menu_callback:
            self.menu_callback()
