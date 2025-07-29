import os
from dbfread import DBF

def extraer_schema(ruta_dbf, ruta_salida):
    try:
        dbf = DBF(ruta_dbf, load=False)
        with open(ruta_salida, 'w', encoding='utf-8') as f:
            f.write(f"Schema de {os.path.basename(ruta_dbf)}:\n")
            for field in dbf.fields:
                f.write(f"{field.name}: {field.type} ({field.length})\n")
        print(f"Esquema extraído: {ruta_salida}")
    except Exception as e:
        print(f"Error al extraer esquema de {ruta_dbf}: {e}")