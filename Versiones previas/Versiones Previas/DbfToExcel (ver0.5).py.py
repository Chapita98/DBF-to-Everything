import tkinter as tk
from tkinter import messagebox

def abrir_ventana_formato():
    ventana_formato = tk.Toplevel()
    ventana_formato.title("Opciones de formato")

    centrar_celdas = tk.BooleanVar(value=True)
    inmovilizar_fila = tk.BooleanVar(value=True)
    alternar_colores = tk.BooleanVar(value=True)
    ajustar_fila1 = tk.BooleanVar(value=True)

    tk.Checkbutton(ventana_formato, text="Centrar celdas", variable=centrar_celdas).pack()
    tk.Checkbutton(ventana_formato, text="Inmovilizar fila 1", variable=inmovilizar_fila).pack()
    tk.Checkbutton(ventana_formato, text="Alternar colores", variable=alternar_colores).pack()
    tk.Checkbutton(ventana_formato, text="Ajustar tamaño fila 1", variable=ajustar_fila1).pack()

    def guardar_formatos():
        global formatos_seleccionados
        formatos_seleccionados = {
            'centrar_celdas': centrar_celdas.get(),
            'inmovilizar_fila': inmovilizar_fila.get(),
            'alternar_colores': alternar_colores.get(),
            'ajustar_fila1': ajustar_fila1.get()
        }
        ventana_formato.destroy()
        messagebox.showinfo("Éxito", "Formatos guardados.")

    tk.Button(ventana_formato, text="Guardar", command=guardar_formatos).pack()

# Modificar aplicar_formato_excel para usar las opciones seleccionadas
def aplicar_formato_excel(ruta_salida, formatos):
    wb = load_workbook(ruta_salida)
    ws = wb.active

    if formatos.get('centrar_celdas', False):
        for row in ws.iter_rows():
            for cell in row:
                cell.alignment = Alignment(horizontal='center', vertical='center')

    if formatos.get('inmovilizar_fila', False):
        ws.freeze_panes = 'A2'

    if formatos.get('alternar_colores', False):
        for i, row in enumerate(ws.iter_rows(min_row=2), start=2):
            color = 'FFFFFF' if i % 2 == 0 else 'F0F0F0'
            for cell in row:
                cell.fill = PatternFill(start_color=color, end_color=color, fill_type='solid')

    if formatos.get('ajustar_fila1', False):
        ws.row_dimensions[1].height = 25

    for col in ws.columns:
        max_length = max(len(str(cell.value or '')) for cell in col)
        ws.column_dimensions[col[0].column_letter].width = max_length + 2

    wb.save(ruta_salida)