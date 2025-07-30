import datetime
def registrar_evento(mensaje):
    """Agrega un mensaje con timestamp al registro de logs/registro_programa.txt"""
    ruta_log = os.path.join(os.path.dirname(__file__), 'logs', 'registro_programa.txt')
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        with open(ruta_log, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {mensaje}\n")
    except Exception as e:
        print(f"No se pudo escribir en el log: {e}")
def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = (pantalla_ancho // 2) - (ancho // 2)
    y = (pantalla_alto // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
    
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