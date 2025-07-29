import dbf
import pandas as pd

def convertir_archivo_grande(archivo_entrada, ruta_salida):
    try:
        with dbf.Table(archivo_entrada) as tabla:
            chunk_size = 10000
            writer = pd.ExcelWriter(ruta_salida, engine='openpyxl')
            df = pd.DataFrame()
            for i, record in enumerate(tabla):
                if i % chunk_size == 0 and i > 0:
                    df.to_excel(writer, sheet_name='Sheet1', startrow=i - len(df), index=False)
                    df = pd.DataFrame()
                df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
            if not df.empty:
                df.to_excel(writer, sheet_name='Sheet1', startrow=i - len(df) + 1, index=False)
            writer.close()
        print(f"Convertido: {ruta_salida}")
    except Exception as e:
        print(f"Error al procesar {archivo_entrada}: {e}")