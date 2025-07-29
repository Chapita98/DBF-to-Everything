import os
import tkinter as tk
from tkinter import messagebox
import pandas as pd
import dbfread

def convertir_archivos():
    directorio_entrada = entrada_var.get()
    directorio_salida = salida_var.get()
    if not directorio_entrada or not directorio_salida:
        messagebox.showerror("Error", "Por favor, selecciona ambos directorios.")
        return

    seleccionados = lista_archivos.curselection()
    if not seleccionados:
        messagebox.showerror("Error", "Por favor, selecciona al menos un archivo.")
        return

    carpeta_salidas = os.path.join(directorio_salida, "salidas")
    if not os.path.exists(carpeta_salidas):
        os.makedirs(carpeta_salidas)

    archivos_a_convertir = [lista_archivos.get(index) for index in seleccionados]
    archivos_existentes = []

    # Verificar archivos existentes
    for archivo in archivos_a_convertir:
        nombre_salida = os.path.splitext(archivo)[0] + '.xlsx'
        ruta_salida = os.path.join(carpeta_salidas, nombre_salida)
        if os.path.exists(ruta_salida):
            archivos_existentes.append(nombre_salida)

    if archivos_existentes:
        mensaje = "Los siguientes archivos ya existen:\n" + "\n".join(archivos_existentes) + "\n\n¿Desea sobrescribirlos?"
        respuesta = messagebox.askyesno("Advertencia", mensaje)
        if not respuesta:
            # Renombrar archivos
            for i, archivo in enumerate(archivos_a_convertir):
                nombre_base = os.path.splitext(archivo)[0]
                ruta_salida = os.path.join(carpeta_salidas, nombre_base + '.xlsx')
                contador = 1
                while os.path.exists(ruta_salida):
                    ruta_salida = os.path.join(carpeta_salidas, f"{nombre_base} ({contador}).xlsx")
                    contador += 1
                archivos_a_convertir[i] = (archivo, ruta_salida)
        else:
            archivos_a_convertir = [(archivo, os.path.join(carpeta_salidas, os.path.splitext(archivo)[0] + '.xlsx')) for archivo in archivos_a_convertir]
    else:
        archivos_a_convertir = [(archivo, os.path.join(carpeta_salidas, os.path.splitext(archivo)[0] + '.xlsx')) for archivo in archivos_a_convertir]

    # Realizar la conversión
    for archivo, ruta_salida in archivos_a_convertir:
        try:
            tabla = dbfread.DBF(os.path.join(directorio_entrada, archivo), encoding='latin1')
            df = pd.DataFrame(iter(tabla))
            df.to_excel(ruta_salida, index=False)
            print(f"Convertido: {ruta_salida}")
        except Exception as e:
            print(f"Error al procesar {archivo}: {e}")

    messagebox.showinfo("Éxito", "Archivos convertidos correctamente.")