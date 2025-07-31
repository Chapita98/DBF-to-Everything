import os
import tkinter as tk
from tkinter import messagebox
import sys
from interfaz import Aplicacion

class MenuPrincipal(tk.Tk):
    def abrir_dbf_a_json(self):
        from funciones_extra import dbf_a_json
        from tkinter import filedialog, messagebox
        self.withdraw()
        win = tk.Toplevel(self)
        win.title("Dbf a JSON")
        win.resizable(False, False)
        self.update_idletasks()
        ancho, alto = 400, 180
        x = self.winfo_screenwidth() // 2 - ancho // 2
        y = self.winfo_screenheight() // 2 - alto // 2
        win.geometry(f"{ancho}x{alto}+{x}+{y}")
        tk.Label(win, text="Selecciona un archivo DBF:").pack(pady=10)
        ruta_dbf = tk.StringVar()
        tk.Entry(win, textvariable=ruta_dbf, width=40).pack(pady=2)
        def sel_dbf():
            ruta = filedialog.askopenfilename(filetypes=[("DBF files", "*.dbf")])
            if ruta:
                ruta_dbf.set(ruta)
        tk.Button(win, text="Buscar", command=sel_dbf).pack(pady=2)
        tk.Label(win, text="Archivo de salida (.json):").pack(pady=10)
        ruta_json = tk.StringVar()
        tk.Entry(win, textvariable=ruta_json, width=40).pack(pady=2)
        def sel_json():
            ruta = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
            if ruta:
                ruta_json.set(ruta)
        tk.Button(win, text="Guardar como...", command=sel_json).pack(pady=2)
        def ejecutar():
            from utilidades import registrar_evento
            if not ruta_dbf.get() or not ruta_json.get():
                messagebox.showerror("Error", "Selecciona ambos archivos.")
                registrar_evento("Dbf a JSON - 0 - FALLO - No se seleccionaron ambos archivos")
                return
            ok, msg = dbf_a_json(ruta_dbf.get(), ruta_json.get())
            if ok:
                messagebox.showinfo("Listo", msg)
                registrar_evento(f"Dbf a JSON - 1 - EXITO")
            else:
                messagebox.showerror("Error", msg)
                registrar_evento(f"Dbf a JSON - 1 - FALLO - {msg}")
        tk.Button(win, text="Convertir a JSON", command=ejecutar).pack(pady=10)
        def cerrar():
            win.destroy()
            self.deiconify()

        # btn10 = tk.Button(frame, text="Extraer TODO el Schema", command=self.abrir_extraer_todo_schema, **button_style)
        win.protocol("WM_DELETE_WINDOW", cerrar)
    def abrir_visualizador_dbf(self):
        from tkinter import messagebox
        messagebox.showinfo("Visualizador DBF", "Función aún no implementada.")

    def __init__(self):
        super().__init__()
        from utilidades import centrar_ventana
        self.title("Menú de Programas")
        self.resizable(False, False)
        centrar_ventana(self, 400, 520)
        self.minsize(400, 520)
        self.maxsize(400, 520)
        self.crear_widgets()

        # btn10.grid(row=2, column=0, columnspan=2, padx=10, pady=7, sticky="ew")
    def centrar_ventana(self, ancho, alto):
        self.update_idletasks()
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()
        x = (pantalla_ancho // 2) - (ancho // 2)
    def abrir_extraer_todo_schema(self):
        from tkinter import filedialog, messagebox
        from schema_extractor import extraer_schema
        import os
        self.withdraw()
        win = tk.Toplevel(self)
        win.title("Extraer TODO el Schema de DBF")
        win.resizable(False, False)
        ancho, alto = 520, 300
        # Centrar la ventana
        win.update_idletasks()
        pantalla_ancho = win.winfo_screenwidth()
        pantalla_alto = win.winfo_screenheight()
        x = (pantalla_ancho // 2) - (ancho // 2)
        y = (pantalla_alto // 2) - (alto // 2)
        win.geometry(f"{ancho}x{alto}+{x}+{y}")
        win.minsize(ancho, alto)
        win.maxsize(ancho, alto)


        tk.Label(win, text="Selecciona la carpeta RAÍZ con subcarpetas de DBF:").pack(pady=(10,2))
        carpeta_origen = tk.StringVar()
        entry_origen = tk.Entry(win, textvariable=carpeta_origen, width=60)
        entry_origen.pack(pady=2)
        def sel_origen():
            carpeta = filedialog.askdirectory(title="Seleccionar carpeta raíz de DBF")
            if carpeta:
                carpeta_origen.set(carpeta)
        btn_origen = tk.Button(win, text="Seleccionar carpeta de entrada", command=sel_origen)
        btn_origen.pack(pady=2)

        tk.Label(win, text="Carpeta de destino para los schemas:").pack(pady=(10,2))
        carpeta_destino = tk.StringVar()
        entry_dest = tk.Entry(win, textvariable=carpeta_destino, width=60)
        entry_dest.pack(pady=2)
        def sel_dest():
            carpeta = filedialog.askdirectory(title="Seleccionar carpeta de destino")
            if carpeta:
                carpeta_destino.set(carpeta)
        btn_dest = tk.Button(win, text="Seleccionar carpeta de salida", command=sel_dest)
        btn_dest.pack(pady=2)


        # Botón para iniciar conversión (debajo de los objetos actuales)
        btn_iniciar = tk.Button(win, text="Iniciar Conversión", command=lambda: ejecutar(), bg="#4A90E2", fg="white", font=("Arial", 12, "bold"))
        btn_iniciar.pack(pady=(30, 10))

        # Botón para iniciar el proceso
        def ejecutar():
            from utilidades import registrar_evento
            origen = carpeta_origen.get()
            destino = carpeta_destino.get()
            if not origen or not destino:
                messagebox.showerror("Error", "Selecciona ambas carpetas.")
                registrar_evento("Extraer TODO el Schema - 0 - FALLO - No se seleccionaron ambas carpetas")
                return
            errores = []
            total = 0
            for root, dirs, files in os.walk(origen):
                rel_path = os.path.relpath(root, origen)
                dest_dir = os.path.join(destino, rel_path) if rel_path != '.' else destino
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                for file in files:
                    if file.lower().endswith('.dbf'):
                        ruta_dbf = os.path.join(root, file)
                        nombre = os.path.splitext(file)[0]
                        ruta_sql = os.path.join(dest_dir, f"{nombre}.sql")
                        try:
                            extraer_schema(ruta_dbf, ruta_sql, constraints={})
                            total += 1
                        except Exception as e:
                            errores.append(f"{ruta_dbf}: {e}")
            if errores:
                messagebox.showwarning("Completado con errores", f"Se procesaron {total} archivos. Algunos archivos no se procesaron:\n" + "\n".join(errores))
                nota = f"Errores: {' | '.join(errores[:3])}{' ...' if len(errores)>3 else ''}"
                registrar_evento(f"Extraer TODO el Schema - {total} - FALLO - {nota}")
            else:
                messagebox.showinfo("Completado", f"Schemas extraídos correctamente. Total: {total}")
                registrar_evento(f"Extraer TODO el Schema - {total} - EXITO")
            win.destroy()
            self.deiconify()


        def cerrar():
            win.destroy()
            self.deiconify()
            self.centrar_ventana(400, 520)
        win.protocol("WM_DELETE_WINDOW", cerrar)

    def crear_widgets(self):
        # Título centrado arriba de los botones
        titulo = tk.Label(self, text=".dbf To Everything", font=("Arial", 20, "bold"), fg="#333")
        titulo.pack(pady=(18, 8))

        frame = tk.Frame(self)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        self.frame_botones = frame

        button_style = {
            "width": 16,
            "height": 2,
            "font": ("Arial", 13, "bold"),
            "bg": "#4A90E2",
            "fg": "white",
            "activebackground": "#357ABD",
            "activeforeground": "white",
            "bd": 2,
            "relief": "raised"
        }

        # Primera columna
        btn1 = tk.Button(frame, text="Dbf to Excel", command=self.abrir_dfb_to_excel, **button_style)
        btn2 = tk.Button(frame, text="Extraer Schema", command=self.abrir_extraer_schema, **button_style)
        btn3 = tk.Button(frame, text="Dbf to CSV", command=self.abrir_dfb_to_csv, **button_style)
        btn4 = tk.Button(frame, text="Dbf a JSON", command=self.abrir_dbf_a_json, **button_style)
        btn5 = tk.Button(frame, text="Visualizar DBF", command=self.abrir_visualizador_dbf, **button_style)
        btn6 = tk.Button(frame, text="Renombrar campos", command=self.abrir_renombrar_campos, **button_style)
        btn7 = tk.Button(frame, text="Fusionar DBFs", command=self.abrir_fusionar_dbfs, **button_style)
        btn8 = tk.Button(frame, text="Estadísticas DBF", command=self.abrir_estadisticas_dbf, **button_style)
        btn9 = tk.Button(frame, text="Validar integridad", command=self.abrir_validar_integridad, **button_style)
        btn10 = tk.Button(frame, text="Extraer TODO el Schema", command=self.abrir_extraer_todo_schema, **button_style)

        # Distribución en 2 columnas (6 filas)
        btn1.grid(row=0, column=0, padx=10, pady=7)
        btn2.grid(row=0, column=1, padx=10, pady=7)
        btn3.grid(row=1, column=0, padx=10, pady=7)
        btn4.grid(row=1, column=1, padx=10, pady=7)
        btn5.grid(row=2, column=0, padx=10, pady=7)
        btn6.grid(row=2, column=1, padx=10, pady=7)
        btn7.grid(row=3, column=0, padx=10, pady=7)
        btn8.grid(row=3, column=1, padx=10, pady=7)
        btn9.grid(row=4, column=0, columnspan=2, padx=10, pady=7, sticky="ew")
        btn10.grid(row=5, column=0, columnspan=2, padx=10, pady=7, sticky="ew")

    # --- Nuevas funciones de botones ---
    def abrir_extraer_schema(self):
        from tkinter import filedialog, messagebox
        from schema_extractor import extraer_schema
        import os
        self.withdraw()
        win = tk.Toplevel(self)
        win.title("Extraer Schema de DBF")
        win.resizable(False, False)
        self.update_idletasks()
        ancho, alto = 480, 260
        x = self.winfo_screenwidth() // 2 - ancho // 2
        y = self.winfo_screenheight() // 2 - alto // 2
        win.geometry(f"{ancho}x{alto}+{x}+{y}")

        tk.Label(win, text="Selecciona archivos DBF (Ctrl+Click):").pack(pady=10)
        rutas_dbf = tk.StringVar()
        entry_dbf = tk.Entry(win, textvariable=rutas_dbf, width=55)
        entry_dbf.pack(pady=2)
        def sel_dbfs():
            archivos = filedialog.askopenfilenames(title="Seleccionar archivos DBF", filetypes=[("Archivos DBF", "*.dbf")])
            if archivos:
                rutas_dbf.set(";".join(archivos))
        tk.Button(win, text="Buscar", command=sel_dbfs).pack(pady=2)

        tk.Label(win, text="Carpeta de destino para los schemas:").pack(pady=10)
        carpeta_destino = tk.StringVar()
        entry_dest = tk.Entry(win, textvariable=carpeta_destino, width=55)
        entry_dest.pack(pady=2)
        def sel_dest():
            carpeta = filedialog.askdirectory(title="Seleccionar carpeta de destino")
            if carpeta:
                carpeta_destino.set(carpeta)
        tk.Button(win, text="Seleccionar carpeta", command=sel_dest).pack(pady=2)

        def ejecutar():
            from utilidades import registrar_evento
            archivos = rutas_dbf.get().split(";")
            carpeta = carpeta_destino.get()
            if not archivos or not archivos[0]:
                messagebox.showerror("Error", "Debes seleccionar al menos un archivo DBF.")
                registrar_evento("Extraer Schema - 0 - FALLO - No se seleccionaron archivos")
                return
            if not carpeta:
                messagebox.showerror("Error", "Debes seleccionar la carpeta de destino.")
                registrar_evento("Extraer Schema - 0 - FALLO - No se seleccionó carpeta de destino")
                return
            errores = []
            total = 0
            for ruta_dbf in archivos:
                if not ruta_dbf.strip():
                    continue
                nombre = os.path.splitext(os.path.basename(ruta_dbf))[0]
                ruta_sql = os.path.join(carpeta, f"{nombre}.sql")
                try:
                    extraer_schema(ruta_dbf, ruta_sql, constraints={})
                    total += 1
                except Exception as e:
                    errores.append(f"{nombre}: {e}")
            if errores:
                messagebox.showwarning("Completado con errores", "Algunos archivos no se procesaron:\n" + "\n".join(errores))
                nota = f"Errores: {' | '.join(errores[:3])}{' ...' if len(errores)>3 else ''}"
                registrar_evento(f"Extraer Schema - {total} - FALLO - {nota}")
            else:
                messagebox.showinfo("Completado", "Schemas extraídos correctamente.")
                registrar_evento(f"Extraer Schema - {total} - EXITO")
            win.destroy()
            self.deiconify()

        tk.Button(win, text="Extraer Schema(s)", command=ejecutar).pack(pady=10)
        def cerrar():
            win.destroy()
            self.deiconify()
            self.centrar_ventana(400, 520)
        win.protocol("WM_DELETE_WINDOW", cerrar)

    def abrir_visualizador_dbf(self):
        from funciones_extra import visualizar_dbf
        from tkinter import filedialog, messagebox
        import pandas as pd
        ruta = filedialog.askopenfilename(title="Seleccionar archivo DBF", filetypes=[("Archivos DBF", "*.dbf")])
        if not ruta:
            return
        df = visualizar_dbf(ruta)
        if df is None:
            messagebox.showerror("Error", "No se pudo visualizar el archivo DBF.")
            return
        # Mostrar una vista simple del DataFrame (primeras filas)
        vista = df.head(20).to_string(index=False)
        messagebox.showinfo("Vista previa DBF", vista)

    def abrir_renombrar_campos(self):
        from funciones_extra import renombrar_campos_dbf
        from tkinter import filedialog, simpledialog, messagebox
        self.withdraw()
        win = tk.Toplevel(self)
        win.title("Renombrar campos DBF")
        win.resizable(False, False)
        self.update_idletasks()
        ancho, alto = 500, 220
        x = self.winfo_screenwidth() // 2 - ancho // 2
        y = self.winfo_screenheight() // 2 - alto // 2
        win.geometry(f"{ancho}x{alto}+{x}+{y}")
        tk.Label(win, text="Selecciona un archivo DBF:").pack(pady=10)
        ruta_dbf = tk.StringVar()
        tk.Entry(win, textvariable=ruta_dbf, width=40).pack(pady=2)
        def sel_dbf():
            ruta = filedialog.askopenfilename(filetypes=[("DBF files", "*.dbf")])
            if ruta:
                ruta_dbf.set(ruta)
        tk.Button(win, text="Buscar", command=sel_dbf).pack(pady=2)
        tk.Label(win, text="Nuevos nombres (separados por coma):").pack(pady=10)
        nombres = tk.StringVar()
        tk.Entry(win, textvariable=nombres, width=50).pack(pady=2)
        tk.Label(win, text="Archivo de salida (.csv):").pack(pady=10)
        ruta_csv = tk.StringVar()
        tk.Entry(win, textvariable=ruta_csv, width=40).pack(pady=2)
        def sel_csv():
            ruta = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if ruta:
                ruta_csv.set(ruta)
        tk.Button(win, text="Guardar como...", command=sel_csv).pack(pady=2)
        def ejecutar():
            from utilidades import registrar_evento
            if not ruta_dbf.get() or not ruta_csv.get() or not nombres.get():
                messagebox.showerror("Error", "Completa todos los campos.")
                registrar_evento("Renombrar campos - 0 - FALLO - Faltan campos")
                return
            nuevos = [n.strip() for n in nombres.get().split(",")]
            ok, msg = renombrar_campos_dbf(ruta_dbf.get(), nuevos, ruta_csv.get())
            if ok:
                messagebox.showinfo("Listo", msg)
                registrar_evento(f"Renombrar campos - 1 - EXITO")
            else:
                messagebox.showerror("Error", msg)
                registrar_evento(f"Renombrar campos - 1 - FALLO - {msg}")
        tk.Button(win, text="Renombrar y exportar", command=ejecutar).pack(pady=10)
        def cerrar():
            win.destroy()
            self.deiconify()
            self.centrar_ventana(400, 520)
        win.protocol("WM_DELETE_WINDOW", cerrar)

    def abrir_fusionar_dbfs(self):
        from funciones_extra import fusionar_dbfs
        from tkinter import filedialog, messagebox
        self.withdraw()
        win = tk.Toplevel(self)
        win.title("Fusionar DBFs")
        win.resizable(False, False)
        self.update_idletasks()
        ancho, alto = 500, 180
        x = self.winfo_screenwidth() // 2 - ancho // 2
        y = self.winfo_screenheight() // 2 - alto // 2
        win.geometry(f"{ancho}x{alto}+{x}+{y}")
        tk.Label(win, text="Selecciona archivos DBF (Ctrl+Click):").pack(pady=10)
        rutas_dbf = tk.StringVar()
        tk.Entry(win, textvariable=rutas_dbf, width=50).pack(pady=2)
        def sel_dbfs():
            rutas = filedialog.askopenfilenames(filetypes=[("DBF files", "*.dbf")])
            if rutas:
                rutas_dbf.set(", ".join(rutas))
        tk.Button(win, text="Buscar", command=sel_dbfs).pack(pady=2)
        tk.Label(win, text="Archivo de salida (.csv):").pack(pady=10)
        ruta_csv = tk.StringVar()
        tk.Entry(win, textvariable=ruta_csv, width=40).pack(pady=2)
        def sel_csv():
            ruta = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if ruta:
                ruta_csv.set(ruta)
        tk.Button(win, text="Guardar como...", command=sel_csv).pack(pady=2)
        def ejecutar():
            from utilidades import registrar_evento
            if not rutas_dbf.get() or not ruta_csv.get():
                messagebox.showerror("Error", "Selecciona archivos y salida.")
                registrar_evento("Fusionar DBFs - 0 - FALLO - Faltan archivos o salida")
                return
            lista = [r.strip() for r in rutas_dbf.get().split(",") if r.strip()]
            ok, msg = fusionar_dbfs(lista, ruta_csv.get())
            if ok:
                messagebox.showinfo("Listo", msg)
                registrar_evento(f"Fusionar DBFs - {len(lista)} - EXITO")
            else:
                messagebox.showerror("Error", msg)
                registrar_evento(f"Fusionar DBFs - {len(lista)} - FALLO - {msg}")
        tk.Button(win, text="Fusionar", command=ejecutar).pack(pady=10)
        def cerrar():
            win.destroy()
            self.deiconify()
            self.centrar_ventana(400, 520)
        win.protocol("WM_DELETE_WINDOW", cerrar)

    def abrir_estadisticas_dbf(self):
        from funciones_extra import estadisticas_dbf
        from tkinter import filedialog, messagebox
        self.withdraw()
        win = tk.Toplevel(self)
        win.title("Estadísticas DBF")
        win.resizable(False, False)
        self.update_idletasks()
        ancho, alto = 400, 200
        x = self.winfo_screenwidth() // 2 - ancho // 2
        y = self.winfo_screenheight() // 2 - alto // 2
        win.geometry(f"{ancho}x{alto}+{x}+{y}")
        tk.Label(win, text="Selecciona un archivo DBF:").pack(pady=10)
        ruta_dbf = tk.StringVar()
        tk.Entry(win, textvariable=ruta_dbf, width=40).pack(pady=2)
        def sel_dbf():
            ruta = filedialog.askopenfilename(filetypes=[("DBF files", "*.dbf")])
            if ruta:
                ruta_dbf.set(ruta)
        tk.Button(win, text="Buscar", command=sel_dbf).pack(pady=2)
        def mostrar():
            from utilidades import registrar_evento
            if not ruta_dbf.get():
                messagebox.showerror("Error", "Selecciona un archivo DBF.")
                registrar_evento("Estadísticas DBF - 0 - FALLO - No se seleccionó archivo")
                return
            stats = estadisticas_dbf(ruta_dbf.get())
            if "error" in stats:
                messagebox.showerror("Error", stats["error"])
                registrar_evento(f"Estadísticas DBF - 0 - FALLO - {stats['error']}")
                return
            info = f"Registros: {stats['registros']}\nCampos: {', '.join(stats['campos'])}\nTipos: {stats['tipos']}"
            messagebox.showinfo("Estadísticas", info)
            registrar_evento(f"Estadísticas DBF - 1 - EXITO")
        tk.Button(win, text="Mostrar estadísticas", command=mostrar).pack(pady=10)
        def cerrar():
            win.destroy()
            self.deiconify()
            self.centrar_ventana(400, 520)
        win.protocol("WM_DELETE_WINDOW", cerrar)

    def abrir_validar_integridad(self):
        from funciones_extra import validar_integridad_dbf
        from tkinter import filedialog, messagebox
        self.withdraw()
        win = tk.Toplevel(self)
        win.title("Validar integridad DBF")
        win.resizable(False, False)
        self.update_idletasks()
        ancho, alto = 400, 180
        x = self.winfo_screenwidth() // 2 - ancho // 2
        y = self.winfo_screenheight() // 2 - alto // 2
        win.geometry(f"{ancho}x{alto}+{x}+{y}")
        tk.Label(win, text="Selecciona un archivo DBF:").pack(pady=10)
        ruta_dbf = tk.StringVar()
        tk.Entry(win, textvariable=ruta_dbf, width=35).pack(pady=2)
        def sel_dbf():
            ruta = filedialog.askopenfilename(filetypes=[("DBF files", "*.dbf")])
            if ruta:
                ruta_dbf.set(ruta)
        tk.Button(win, text="Buscar", command=sel_dbf).pack(pady=2)
        def ejecutar():
            from utilidades import registrar_evento
            if not ruta_dbf.get():
                messagebox.showerror("Error", "Selecciona un archivo DBF.")
                registrar_evento("Validar integridad - 0 - FALLO - No se seleccionó archivo")
                return
            ok, msg = validar_integridad_dbf(ruta_dbf.get())
            if ok:
                messagebox.showinfo("Integridad", msg)
                registrar_evento(f"Validar integridad - 1 - EXITO")
            else:
                messagebox.showerror("Integridad", msg)
                registrar_evento(f"Validar integridad - 1 - FALLO - {msg}")
        tk.Button(win, text="Validar", command=ejecutar).pack(pady=10)
        def cerrar():
            win.destroy()
            self.deiconify()
            self.centrar_ventana(400, 520)
        win.protocol("WM_DELETE_WINDOW", cerrar)
    def abrir_extraer_schema(self):
        import os
        from tkinter import filedialog, messagebox
        from schema_extractor import extraer_schema
        self.withdraw()
        win = tk.Toplevel(self)
        win.title("Extraer Schema de DBF")
        win.resizable(False, False)
        self.update_idletasks()
        ancho, alto = 480, 260
        x = self.winfo_screenwidth() // 2 - ancho // 2
        y = self.winfo_screenheight() // 2 - alto // 2
        win.geometry(f"{ancho}x{alto}+{x}+{y}")

        tk.Label(win, text="Selecciona archivos DBF (Ctrl+Click):").pack(pady=10)
        rutas_dbf = tk.StringVar()
        entry_dbf = tk.Entry(win, textvariable=rutas_dbf, width=55)
        entry_dbf.pack(pady=2)
        def sel_dbfs():
            archivos = filedialog.askopenfilenames(title="Seleccionar archivos DBF", filetypes=[("Archivos DBF", "*.dbf")])
            if archivos:
                rutas_dbf.set(";".join(archivos))
        tk.Button(win, text="Buscar", command=sel_dbfs).pack(pady=2)

        tk.Label(win, text="Carpeta de destino para los schemas:").pack(pady=10)
        carpeta_destino = tk.StringVar()
        entry_dest = tk.Entry(win, textvariable=carpeta_destino, width=55)
        entry_dest.pack(pady=2)
        def sel_dest():
            carpeta = filedialog.askdirectory(title="Seleccionar carpeta de destino")
            if carpeta:
                carpeta_destino.set(carpeta)
        tk.Button(win, text="Seleccionar carpeta", command=sel_dest).pack(pady=2)

        def ejecutar():
            archivos = rutas_dbf.get().split(";")
            carpeta = carpeta_destino.get()
            if not archivos or not archivos[0]:
                messagebox.showerror("Error", "Debes seleccionar al menos un archivo DBF.")
                return
            if not carpeta:
                messagebox.showerror("Error", "Debes seleccionar la carpeta de destino.")
                return
            errores = []
            for ruta_dbf in archivos:
                nombre = os.path.splitext(os.path.basename(ruta_dbf))[0]
                ruta_sql = os.path.join(carpeta, f"{nombre}.sql")
                try:
                    extraer_schema(ruta_dbf, ruta_sql, constraints={})
                except Exception as e:
                    errores.append(f"{nombre}: {e}")
            if errores:
                messagebox.showwarning("Completado con errores", "Algunos archivos no se procesaron:\n" + "\n".join(errores))
            else:
                messagebox.showinfo("Completado", "Schemas extraídos correctamente.")
            win.destroy()
            self.deiconify()

        tk.Button(win, text="Extraer Schema(s)", command=ejecutar).pack(pady=10)
        def cerrar():
            win.destroy()
            self.deiconify()
            self.centrar_ventana(400, 520)
        win.protocol("WM_DELETE_WINDOW", cerrar)

    def abrir_renombrar_campos(self):
        from funciones_extra import renombrar_campos_dbf, visualizar_dbf
        import tkinter.filedialog as fd
        self.withdraw()
        win = tk.Toplevel(self)
        win.title("Renombrar campos DBF")
        win.resizable(False, False)
        self.update_idletasks()
        ancho, alto = 500, 300
        x = self.winfo_screenwidth() // 2 - ancho // 2
        y = self.winfo_screenheight() // 2 - alto // 2
        win.geometry(f"{ancho}x{alto}+{x}+{y}")
        tk.Label(win, text="Selecciona un archivo DBF:").pack(pady=10)
        ruta_dbf = tk.StringVar()
        tk.Entry(win, textvariable=ruta_dbf, width=40).pack(pady=2)
        def sel_dbf():
            ruta = fd.askopenfilename(filetypes=[("DBF files", "*.dbf")])
            if ruta:
                ruta_dbf.set(ruta)
        tk.Button(win, text="Buscar", command=sel_dbf).pack(pady=2)
        tk.Label(win, text="Nuevos nombres (separados por coma):").pack(pady=10)
        nombres = tk.StringVar()
        tk.Entry(win, textvariable=nombres, width=50).pack(pady=2)
        tk.Label(win, text="Archivo de salida (.csv):").pack(pady=10)
        ruta_csv = tk.StringVar()
        tk.Entry(win, textvariable=ruta_csv, width=40).pack(pady=2)
        def sel_csv():
            ruta = fd.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if ruta:
                ruta_csv.set(ruta)
        tk.Button(win, text="Guardar como...", command=sel_csv).pack(pady=2)
        def ejecutar():
            if not ruta_dbf.get() or not ruta_csv.get() or not nombres.get():
                messagebox.showerror("Error", "Completa todos los campos.")
                return
            nuevos = [n.strip() for n in nombres.get().split(",")]
            ok, msg = renombrar_campos_dbf(ruta_dbf.get(), nuevos, ruta_csv.get())
            if ok:
                messagebox.showinfo("Listo", msg)
            else:
                messagebox.showerror("Error", msg)
        tk.Button(win, text="Renombrar y exportar", command=ejecutar).pack(pady=10)
        def cerrar():
            win.destroy()
            self.deiconify()
            self.geometry("")
            self.centrar_ventana(400, 520)
        win.protocol("WM_DELETE_WINDOW", cerrar)

    def abrir_fusionar_dbfs(self):
        from funciones_extra import fusionar_dbfs
        import tkinter.filedialog as fd
        self.withdraw()
        win = tk.Toplevel(self)
        win.title("Fusionar DBFs")
        win.resizable(False, False)
        self.update_idletasks()
        ancho, alto = 500, 220
        x = self.winfo_screenwidth() // 2 - ancho // 2
        y = self.winfo_screenheight() // 2 - alto // 2
        win.geometry(f"{ancho}x{alto}+{x}+{y}")
        tk.Label(win, text="Selecciona archivos DBF (Ctrl+Click):").pack(pady=10)
        rutas_dbf = tk.StringVar()
        tk.Entry(win, textvariable=rutas_dbf, width=50).pack(pady=2)
        def sel_dbfs():
            rutas = fd.askopenfilenames(filetypes=[("DBF files", "*.dbf")])
            if rutas:
                rutas_dbf.set(", ".join(rutas))
        tk.Button(win, text="Buscar", command=sel_dbfs).pack(pady=2)
        tk.Label(win, text="Archivo de salida (.csv):").pack(pady=10)
        ruta_csv = tk.StringVar()
        tk.Entry(win, textvariable=ruta_csv, width=40).pack(pady=2)
        def sel_csv():
            ruta = fd.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if ruta:
                ruta_csv.set(ruta)
        tk.Button(win, text="Guardar como...", command=sel_csv).pack(pady=2)
        def ejecutar():
            if not rutas_dbf.get() or not ruta_csv.get():
                messagebox.showerror("Error", "Selecciona archivos y salida.")
                return
            lista = [r.strip() for r in rutas_dbf.get().split(",")]
            ok, msg = fusionar_dbfs(lista, ruta_csv.get())
            if ok:
                messagebox.showinfo("Listo", msg)
            else:
                messagebox.showerror("Error", msg)
        tk.Button(win, text="Fusionar", command=ejecutar).pack(pady=10)
        def cerrar():
            win.destroy()
            self.deiconify()
            self.geometry("")
            self.centrar_ventana(400, 520)
        win.protocol("WM_DELETE_WINDOW", cerrar)

    def abrir_estadisticas_dbf(self):
        from funciones_extra import estadisticas_dbf
        import tkinter.filedialog as fd
        self.withdraw()
        win = tk.Toplevel(self)
        win.title("Estadísticas DBF")
        win.resizable(False, False)
        self.update_idletasks()
        ancho, alto = 400, 250
        x = self.winfo_screenwidth() // 2 - ancho // 2
        y = self.winfo_screenheight() // 2 - alto // 2
        win.geometry(f"{ancho}x{alto}+{x}+{y}")
        tk.Label(win, text="Selecciona un archivo DBF:").pack(pady=10)
        ruta_dbf = tk.StringVar()
        tk.Entry(win, textvariable=ruta_dbf, width=40).pack(pady=2)
        def sel_dbf():
            ruta = fd.askopenfilename(filetypes=[("DBF files", "*.dbf")])
            if ruta:
                ruta_dbf.set(ruta)
        tk.Button(win, text="Buscar", command=sel_dbf).pack(pady=2)
        def mostrar():
            if not ruta_dbf.get():
                messagebox.showerror("Error", "Selecciona un archivo DBF.")
                return
            stats = estadisticas_dbf(ruta_dbf.get())
            if "error" in stats:
                messagebox.showerror("Error", stats["error"])
                return
            info = f"Registros: {stats['registros']}\nCampos: {', '.join(stats['campos'])}\nTipos: {stats['tipos']}"
            messagebox.showinfo("Estadísticas", info)
        tk.Button(win, text="Mostrar estadísticas", command=mostrar).pack(pady=10)
        def cerrar():
            win.destroy()
            self.deiconify()
            self.geometry("")
            self.centrar_ventana(400, 520)
        win.protocol("WM_DELETE_WINDOW", cerrar)

    def abrir_validar_integridad(self):
        from funciones_extra import validar_integridad_dbf
        import tkinter.filedialog as fd
        self.withdraw()
        win = tk.Toplevel(self)
        win.title("Validar integridad DBF")
        win.resizable(False, False)
        self.update_idletasks()
        ancho, alto = 400, 180
        x = self.winfo_screenwidth() // 2 - ancho // 2
        y = self.winfo_screenheight() // 2 - alto // 2
        win.geometry(f"{ancho}x{alto}+{x}+{y}")
        tk.Label(win, text="Selecciona un archivo DBF:").pack(pady=10)
        ruta_dbf = tk.StringVar()
        tk.Entry(win, textvariable=ruta_dbf, width=35).pack(pady=2)
        def sel_dbf():
            ruta = fd.askopenfilename(filetypes=[("DBF files", "*.dbf")])
            if ruta:
                ruta_dbf.set(ruta)
        tk.Button(win, text="Buscar", command=sel_dbf).pack(pady=2)
        def ejecutar():
            if not ruta_dbf.get():
                messagebox.showerror("Error", "Selecciona un archivo DBF.")
                return
            ok, msg = validar_integridad_dbf(ruta_dbf.get())
            if ok:
                messagebox.showinfo("Integridad", msg)
            else:
                messagebox.showerror("Integridad", msg)
        tk.Button(win, text="Validar", command=ejecutar).pack(pady=10)
        def cerrar():
            win.destroy()
            self.deiconify()
            self.geometry("")
            self.centrar_ventana(400, 520)
        win.protocol("WM_DELETE_WINDOW", cerrar)


    def abrir_dfb_to_csv(self):
        from funciones_conversion import convertir_dbf_a_dataframe, guardar_dataframe_como_csv
        import tkinter.filedialog as fd
        self.withdraw()
        win = tk.Toplevel(self)
        win.title("Dbf to CSV")
        win.resizable(False, False)
        # Centrar ventana hija
        self.update_idletasks()
        ancho, alto = 400, 200
        x = self.winfo_screenwidth() // 2 - ancho // 2
        y = self.winfo_screenheight() // 2 - alto // 2
        win.geometry(f"{ancho}x{alto}+{x}+{y}")
        tk.Label(win, text="Selecciona un archivo DBF:").pack(pady=10)
        ruta_dbf = tk.StringVar()
        tk.Entry(win, textvariable=ruta_dbf, width=35).pack(pady=2)

        def sel_dbf():
            ruta = fd.askopenfilename(filetypes=[("DBF files", "*.dbf")])
            if ruta:
                ruta_dbf.set(ruta)

        tk.Button(win, text="Buscar", command=sel_dbf).pack(pady=2)
        tk.Label(win, text="Archivo de salida (.csv):").pack(pady=10)
        ruta_csv = tk.StringVar()
        tk.Entry(win, textvariable=ruta_csv, width=35).pack(pady=2)

        def sel_csv():
            ruta = fd.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if ruta:
                ruta_csv.set(ruta)

        tk.Button(win, text="Guardar como...", command=sel_csv).pack(pady=2)
        def ejecutar():
            if not ruta_dbf.get() or not ruta_csv.get():
                messagebox.showerror("Error", "Selecciona ambos archivos.")
                return
            df = convertir_dbf_a_dataframe(ruta_dbf.get())
            guardar_dataframe_como_csv(df, ruta_csv.get())
            messagebox.showinfo("Listo", "Archivo CSV generado correctamente.")
        tk.Button(win, text="Convertir a CSV", command=ejecutar).pack(pady=10)
        def cerrar():
            win.destroy()
            # Restaurar tamaño y centrar menú
            self.deiconify()
            self.centrar_ventana(400, 520)
        win.protocol("WM_DELETE_WINDOW", cerrar)

    def abrir_dfb_to_excel(self):
        self.destroy()
        app = Aplicacion(menu_callback=mostrar_menu)
        app.mainloop()

def mostrar_menu():
    menu = MenuPrincipal()
    menu.centrar_ventana(400, 520)
    menu.mainloop()

if __name__ == "__main__":
    mostrar_menu()