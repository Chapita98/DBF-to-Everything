import os
from tkinter import filedialog

def seleccionar_entrada():
    """Abre un diálogo para seleccionar una carpeta de entrada. Retorna la ruta o None si se cancela."""
    return filedialog.askdirectory(title="Seleccionar carpeta de entrada") or None

def seleccionar_carpeta_destino():
    """Abre un diálogo para seleccionar una carpeta de destino. Retorna la ruta o None si se cancela."""
    return filedialog.askdirectory(title="Seleccionar carpeta de destino") or None

def obtener_nombre_archivo_sin_extension(ruta_archivo):
    """Devuelve el nombre del archivo sin extensión a partir de una ruta."""
    return os.path.splitext(os.path.basename(ruta_archivo))[0]

def obtener_archivos_dbf_en_carpeta(ruta_carpeta):
    """Devuelve una lista de rutas de archivos .dbf en la carpeta dada. Si la carpeta no existe, retorna lista vacía."""
    try:
        return [
            os.path.join(ruta_carpeta, f)
            for f in os.listdir(ruta_carpeta)
            if f.lower().endswith('.dbf')
        ]
    except Exception:
        return []

def crear_carpeta_si_no_existe(ruta):
    """Crea la carpeta si no existe."""
    if not os.path.exists(ruta):
        os.makedirs(ruta)

def limpiar_nombre_archivo(nombre):
    """Limpia el nombre de archivo quitando caracteres no válidos para Windows."""
    import re
    return re.sub(r'[<>:"/\\|?*]', '_', nombre)