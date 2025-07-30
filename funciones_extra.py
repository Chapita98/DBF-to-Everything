import os
import pandas as pd
from dbfread import DBF
from tkinter import messagebox

def dbf_a_json(ruta_dbf, ruta_json):
    from utilidades import registrar_evento
    try:
        dbf = DBF(ruta_dbf, load=True)
        df = pd.DataFrame(iter(dbf))
        df.to_json(ruta_json, orient="records", force_ascii=False)
        registrar_evento(f"Dbf a JSON - 1 - EXITO")
        return True, "Archivo JSON generado correctamente."
    except Exception as e:
        registrar_evento(f"Dbf a JSON - 1 - FALLO - {e}")
        return False, f"Error: {e}"

def visualizar_dbf(ruta_dbf):
    try:
        dbf = DBF(ruta_dbf, load=True)
        df = pd.DataFrame(iter(dbf))
        return df
    except Exception as e:
        return None

def renombrar_campos_dbf(ruta_dbf, nuevos_nombres, ruta_salida):
    from utilidades import registrar_evento
    try:
        dbf = DBF(ruta_dbf, load=True)
        df = pd.DataFrame(iter(dbf))
        if len(nuevos_nombres) != len(df.columns):
            registrar_evento(f"Renombrar campos - 0 - FALLO - Cantidad de nombres no coincide")
            return False, "Cantidad de nombres no coincide con los campos."
        df.columns = nuevos_nombres
        df.to_csv(ruta_salida, index=False)
        registrar_evento(f"Renombrar campos - 1 - EXITO")
        return True, "Campos renombrados y exportados a CSV."
    except Exception as e:
        registrar_evento(f"Renombrar campos - 1 - FALLO - {e}")
        return False, f"Error: {e}"

def fusionar_dbfs(lista_rutas, ruta_salida):
    from utilidades import registrar_evento
    try:
        dfs = [pd.DataFrame(iter(DBF(r, load=True))) for r in lista_rutas]
        df_final = pd.concat(dfs, ignore_index=True)
        df_final.to_csv(ruta_salida, index=False)
        registrar_evento(f"Fusionar DBFs - {len(lista_rutas)} - EXITO")
        return True, "Archivos fusionados correctamente."
    except Exception as e:
        registrar_evento(f"Fusionar DBFs - {len(lista_rutas)} - FALLO - {e}")
        return False, f"Error: {e}"

def estadisticas_dbf(ruta_dbf):
    from utilidades import registrar_evento
    try:
        dbf = DBF(ruta_dbf, load=True)
        df = pd.DataFrame(iter(dbf))
        stats = {
            "registros": len(df),
            "campos": list(df.columns),
            "tipos": df.dtypes.apply(lambda x: str(x)).to_dict()
        }
        registrar_evento(f"Estadísticas DBF - 1 - EXITO")
        return stats
    except Exception as e:
        registrar_evento(f"Estadísticas DBF - 0 - FALLO - {e}")
        return {"error": str(e)}

def validar_integridad_dbf(ruta_dbf):
    from utilidades import registrar_evento
    try:
        dbf = DBF(ruta_dbf, load=True)
        errores = []
        for i, record in enumerate(dbf):
            if record is None:
                errores.append(i)
        if errores:
            registrar_evento(f"Validar integridad - 1 - FALLO - Registros corruptos: {errores}")
            return False, f"Registros corruptos en posiciones: {errores}"
        registrar_evento(f"Validar integridad - 1 - EXITO")
        return True, "No se detectaron registros corruptos."
    except Exception as e:
        registrar_evento(f"Validar integridad - 0 - FALLO - {e}")
        return False, f"Error: {e}"
