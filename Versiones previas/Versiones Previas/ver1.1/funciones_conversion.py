import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from funciones_conversion import convertir_basico, convertir_avanzado, convertir_total

class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Convertidor DBF a Excel")
        self.root.geometry("1024x600")

        self.archivos_seleccionados = []
        self.ruta_salida = tk.StringVar()

        self.crear_interfaz()

    def crear_interfaz(self):
        frame_rutas = ttk.Frame(self.root)
        frame_rutas.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_rutas, text="Ruta de salida:").pack(side="left")
        self.entry_salida = ttk.Entry(frame_rutas, textvariable=self.ruta_salida, width=80)
        self.entry_salida.pack(side="left", padx=5)
        ttk.Button(frame_rutas, text="Seleccionar carpeta", command=self.seleccionar_directorio_salida).pack(side="left")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        self.tab_basico = ttk.Frame(self.notebook)
        self.tab_avanzado = ttk.Frame(self.notebook)
        self.tab_total = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_basico, text="Básico")
        self.notebook.add(self.tab_avanzado, text="Avanzado")
        self.notebook.add(self.tab_total, text="Total")

        self.crear_tab_basico()
        self.crear_tab_avanzado()
        self.crear_tab_total()

    def crear_tab_basico(self):
        self.configurar_tabla(self.tab_basico)
        self.agregar_panel_izquierdo(self.tab_basico, self.convertir_basico)

    def crear_tab_avanzado(self):
        self.configurar_tabla(self.tab_avanzado)
        self.agregar_panel_izquierdo(self.tab_avanzado, self.convertir_avanzado, incluir_opciones=True)

    def crear_tab_total(self):
        frame = ttk.Frame(self.tab_total)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Label(frame, text="Conversión de todos los archivos DBF en una carpeta:").pack(pady=5)

        ttk.Button(frame, text="Seleccionar carpeta con archivos DBF", command=self.seleccionar_directorio_total).pack(pady=5)

        ttk.Button(frame, text="Convertir todo", command=self.convertir_total).pack(pady=20)

    def configurar_tabla(self, parent):
        frame_tabla = ttk.Frame(parent)
        frame_tabla.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.tabla = ttk.Treeview(frame_tabla, columns=("archivo"), show="headings")
        self.tabla.heading("archivo", text="Archivo DBF seleccionado")
        self.tabla.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def agregar_panel_izquierdo(self, parent, funcion_convertir, incluir_opciones=False):
        frame_opciones = ttk.Frame(parent)
        frame_opciones.pack(side="left", fill="y", padx=10, pady=10)

        ttk.Button(frame_opciones, text="Seleccionar archivos DBF", command=self.seleccionar_archivos).pack(pady=5)
        ttk.Button(frame_opciones, text="Seleccionar todos", command=self.seleccionar_todos_archivos).pack(pady=5)
        ttk.Button(frame_opciones, text="Convertir", command=funcion_convertir).pack(pady=20)

        if incluir_opciones:
            self.configuracion = {
                "centrar_texto": tk.BooleanVar(value=True),
                "inmovilizar_fila": tk.BooleanVar(value=True),
                "colores_alternados": tk.BooleanVar(value=True),
                "ajustar_columnas": tk.BooleanVar(value=True),
                "negrita_encabezado": tk.BooleanVar(value=True),
                "tamano_encabezado": tk.IntVar(value=12),
                "tamano_datos": tk.IntVar(value=10)
            }

            for key, var in self.configuracion.items():
                if isinstance(var, tk.BooleanVar):
                    ttk.Checkbutton(frame_opciones, text=key.replace("_", " ").capitalize(), variable=var).pack(anchor="w")

            ttk.Label(frame_opciones, text="Tamaño encabezado:").pack(anchor="w")
            ttk.Spinbox(frame_opciones, from_=8, to=20, textvariable=self.configuracion["tamano_encabezado"]).pack(anchor="w")

            ttk.Label(frame_opciones, text="Tamaño datos:").pack(anchor="w")
            ttk.Spinbox(frame_opciones, from_=8, to=20, textvariable=self.configuracion["tamano_datos"]).pack(anchor="w")

    def seleccionar_archivos(self):
        archivos = filedialog.askopenfilenames(filetypes=[("Archivos DBF", "*.dbf")])
        if archivos:
            self.archivos_seleccionados = archivos
            self.actualizar_tabla()

    def seleccionar_todos_archivos(self):
        directorio = filedialog.askdirectory()
        if directorio:
            archivos = [os.path.join(directorio, f) for f in os.listdir(directorio) if f.lower().endswith(".dbf")]
            self.archivos_seleccionados = archivos
            self.actualizar_tabla()

    def seleccionar_directorio_salida(self):
        carpeta = filedialog.askdirectory()
        if carpeta:
            self.ruta_salida.set(carpeta)

    def seleccionar_directorio_total(self):
        carpeta = filedialog.askdirectory()
        if carpeta:
            self.ruta_salida.set(carpeta)

    def actualizar_tabla(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        for archivo in self.archivos_seleccionados:
            self.tabla.insert("", "end", values=(archivo,))

    def convertir_basico(self):
        if not self.archivos_seleccionados:
            messagebox.showwarning("Advertencia", "No se seleccionaron archivos.")
            return
        convertir_basico(self.archivos_seleccionados, self.ruta_salida.get())

    def convertir_avanzado(self):
        if not self.archivos_seleccionados:
            messagebox.showwarning("Advertencia", "No se seleccionaron archivos.")
            return
        convertir_avanzado(self.archivos_seleccionados, self.ruta_salida.get(), self.configuracion)

    def convertir_total(self):
        if not self.ruta_salida.get():
            messagebox.showwarning("Advertencia", "Seleccione una carpeta de salida.")
            return
        convertir_total(self.ruta_salida.get())

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()
