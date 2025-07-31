import os
import pandas as pd
from dbfread import DBF
from tkinter import messagebox

def dbf_a_json(ruta_dbf, ruta_json):
    try:
        dbf = DBF(ruta_dbf, load=True)
        df = pd.DataFrame(iter(dbf))
        df.to_json(ruta_json, orient="records", force_ascii=False)
        return True, "Archivo JSON generado correctamente."
    except Exception as e:
        return False, f"Error: {e}"

def visualizar_dbf(ruta_dbf):
    try:
        dbf = DBF(ruta_dbf, load=True)
        df = pd.DataFrame(iter(dbf))
        return df
    except Exception as e:
        return None

def renombrar_campos_dbf(ruta_dbf, nuevos_nombres, ruta_salida):
    try:
        dbf = DBF(ruta_dbf, load=True)
        df = pd.DataFrame(iter(dbf))
        if len(nuevos_nombres) != len(df.columns):
            return False, "Cantidad de nombres no coincide con los campos."
        df.columns = nuevos_nombres
        df.to_csv(ruta_salida, index=False)
        return True, "Campos renombrados y exportados a CSV."
    except Exception as e:
        return False, f"Error: {e}"

def fusionar_dbfs(lista_rutas, ruta_salida):
    try:
        dfs = [pd.DataFrame(iter(DBF(r, load=True))) for r in lista_rutas]
        df_final = pd.concat(dfs, ignore_index=True)
        df_final.to_csv(ruta_salida, index=False)
        return True, "Archivos fusionados correctamente."
    except Exception as e:
        return False, f"Error: {e}"

def estadisticas_dbf(ruta_dbf):
    try:
        dbf = DBF(ruta_dbf, load=True)
        df = pd.DataFrame(iter(dbf))
        stats = {
            "registros": len(df),
            "campos": list(df.columns),
            "tipos": df.dtypes.apply(lambda x: str(x)).to_dict()
        }
        return stats
    except Exception as e:
        return {"error": str(e)}

def validar_integridad_dbf(ruta_dbf):
    try:
        dbf = DBF(ruta_dbf, load=True)
        errores = []
        for i, record in enumerate(dbf):
            if record is None:
                errores.append(i)
        if errores:
            return False, f"Registros corruptos en posiciones: {errores}"
        return True, "No se detectaron registros corruptos."
    except Exception as e:
        return False, f"Error: {e}"
