import tkinter as tk
from tkinter import messagebox
import sys
from interfaz import Aplicacion

class MenuPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Menú de Programas")
        self.resizable(False, False)
        self.centrar_ventana(400, 400)
        self.crear_widgets()

    def centrar_ventana(self, ancho, alto):
        self.update_idletasks()
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()
        x = (pantalla_ancho // 2) - (ancho // 2)
        y = (pantalla_alto // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def crear_widgets(self):
        frame = tk.Frame(self)
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

        btn1 = tk.Button(frame, text="Dbf to Excel", command=self.abrir_dfb_to_excel, **button_style)
        btn2 = tk.Button(frame, text="Extraer Schema", command=self.abrir_extraer_schema, **button_style)
        btn3 = tk.Button(frame, text="Dbf to CSV", command=self.abrir_dfb_to_csv, **button_style)
        btn4 = tk.Button(frame, text="Programa 4", state="disabled", **button_style)

        btn1.grid(row=0, column=0, padx=10, pady=10)
        btn2.grid(row=0, column=1, padx=10, pady=10)
        btn3.grid(row=1, column=0, padx=10, pady=10)
        btn4.grid(row=1, column=1, padx=10, pady=10)

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
    menu.mainloop()

if __name__ == "__main__":
    mostrar_menu()