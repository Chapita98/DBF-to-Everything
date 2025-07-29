import tkinter as tk
from tkinter import messagebox
import sys
from interfaz import Aplicacion

class MenuPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Menú de Programas")
        self.resizable(False, False)
        self.centrar_ventana(400, 520)
        self.crear_widgets()

    def centrar_ventana(self, ancho, alto):
        self.update_idletasks()
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()
        x = (pantalla_ancho // 2) - (ancho // 2)
        y = (pantalla_alto // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")
        self.minsize(ancho, alto)
        self.maxsize(ancho, alto)

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

        # Segunda columna
        btn5 = tk.Button(frame, text="Visualizar DBF", command=self.abrir_visualizador_dbf, **button_style)
        btn6 = tk.Button(frame, text="Renombrar campos", command=self.abrir_renombrar_campos, **button_style)
        btn7 = tk.Button(frame, text="Fusionar DBFs", command=self.abrir_fusionar_dbfs, **button_style)
        btn8 = tk.Button(frame, text="Estadísticas DBF", command=self.abrir_estadisticas_dbf, **button_style)
        btn9 = tk.Button(frame, text="Validar integridad", command=self.abrir_validar_integridad, **button_style)

        # Distribución en 2 columnas (5 filas)
        btn1.grid(row=0, column=0, padx=10, pady=7)
        btn2.grid(row=0, column=1, padx=10, pady=7)
        btn3.grid(row=1, column=0, padx=10, pady=7)
        btn4.grid(row=1, column=1, padx=10, pady=7)
        btn5.grid(row=2, column=0, padx=10, pady=7)
        btn6.grid(row=2, column=1, padx=10, pady=7)
        btn7.grid(row=3, column=0, padx=10, pady=7)
        btn8.grid(row=3, column=1, padx=10, pady=7)
        btn9.grid(row=4, column=0, columnspan=2, padx=10, pady=7, sticky="ew")

    # --- Nuevas funciones de botones ---
    def abrir_dbf_a_json(self):
        from funciones_extra import dbf_a_json
        import tkinter.filedialog as fd
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
        tk.Entry(win, textvariable=ruta_dbf, width=35).pack(pady=2)
        def sel_dbf():
            ruta = fd.askopenfilename(filetypes=[("DBF files", "*.dbf")])
            if ruta:
                ruta_dbf.set(ruta)
        tk.Button(win, text="Buscar", command=sel_dbf).pack(pady=2)
        tk.Label(win, text="Archivo de salida (.json):").pack(pady=10)
        ruta_json = tk.StringVar()
        tk.Entry(win, textvariable=ruta_json, width=35).pack(pady=2)
        def sel_json():
            ruta = fd.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
            if ruta:
                ruta_json.set(ruta)
        tk.Button(win, text="Guardar como...", command=sel_json).pack(pady=2)
        def ejecutar():
            if not ruta_dbf.get() or not ruta_json.get():
                messagebox.showerror("Error", "Selecciona ambos archivos.")
                return
            ok, msg = dbf_a_json(ruta_dbf.get(), ruta_json.get())
            if ok:
                messagebox.showinfo("Listo", msg)
            else:
                messagebox.showerror("Error", msg)
        tk.Button(win, text="Convertir a JSON", command=ejecutar).pack(pady=10)
        def cerrar():
            win.destroy()
            self.deiconify()
            self.geometry("")
            self.centrar_ventana(400, 520)
        win.protocol("WM_DELETE_WINDOW", cerrar)

    def abrir_visualizador_dbf(self):
        from funciones_extra import visualizar_dbf
        import tkinter.filedialog as fd
        import pandas as pd
        self.withdraw()
        win = tk.Toplevel(self)
        win.title("Visualizar DBF")
        win.resizable(False, False)
        self.update_idletasks()
        ancho_v = 600
        alto_v = 400
        x_v = self.winfo_screenwidth() // 2 - ancho_v // 2
        y_v = self.winfo_screenheight() // 2 - alto_v // 2
        win.geometry(f"{ancho_v}x{alto_v}+{x_v}+{y_v}")
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
            df = visualizar_dbf(ruta_dbf.get())
            if df is None:
                messagebox.showerror("Error", "No se pudo leer el archivo.")
                return
            # Mostrar en tabla simple
            top = tk.Toplevel(win)
            top.title("Vista previa DBF")
            top.geometry("800x400")
            from tkinter import ttk
            tree = ttk.Treeview(top, columns=list(df.columns), show="headings")
            for col in df.columns:
                tree.heading(col, text=col)
                tree.column(col, width=100)
            for _, row in df.head(100).iterrows():
                tree.insert("", tk.END, values=list(row))
            tree.pack(fill=tk.BOTH, expand=True)
        tk.Button(win, text="Visualizar", command=mostrar).pack(pady=10)
        def cerrar():
            win.destroy()
            self.deiconify()
            self.geometry("")
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

    def abrir_extraer_schema(self):
        from schema_extractor import extraer_schema
        import tkinter.filedialog as fd
        self.withdraw()
        win = tk.Toplevel(self)
        win.title("Extraer Schema")
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
        tk.Label(win, text="Archivo de salida (.sql):").pack(pady=10)
        ruta_sql = tk.StringVar()
        tk.Entry(win, textvariable=ruta_sql, width=35).pack(pady=2)
        def sel_sql():
            ruta = fd.asksaveasfilename(defaultextension=".sql", filetypes=[("SQL files", "*.sql")])
            if ruta:
                ruta_sql.set(ruta)
        tk.Button(win, text="Guardar como...", command=sel_sql).pack(pady=2)
        def ejecutar():
            if not ruta_dbf.get() or not ruta_sql.get():
                messagebox.showerror("Error", "Selecciona ambos archivos.")
                return
            extraer_schema(ruta_dbf.get(), ruta_sql.get(), constraints={})
            messagebox.showinfo("Listo", "Schema extraído correctamente.")
        tk.Button(win, text="Extraer Schema", command=ejecutar).pack(pady=10)
        def cerrar():
            win.destroy()
            # Restaurar tamaño y centrar menú
            self.deiconify()
            self.geometry("")
            self.centrar_ventana(400, 400)
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
            self.geometry("")
            self.centrar_ventana(400, 400)
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