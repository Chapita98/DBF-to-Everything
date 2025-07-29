import os
from dbfread import DBF

def convertir_tipo_dbf_a_sql(tipo, longitud):
    """Convierte tipos de DBF a tipos SQL aproximados."""
    tipo = tipo.upper()
    if tipo == 'C':  # Character
        return f"VARCHAR({longitud})"
    elif tipo == 'N':  # Numeric
        return f"DECIMAL({longitud},0)"
    elif tipo == 'D':  # Date
        return "DATE"
    elif tipo == 'L':  # Logical
        return "BOOLEAN"
    else:  # Tipo no reconocido, usar VARCHAR como fallback
        return f"VARCHAR({longitud})"

def extraer_schema(ruta_dbf, ruta_salida):
    try:
        dbf = DBF(ruta_dbf, load=False)
        with open(ruta_salida, 'w', encoding='utf-8') as f:
            nombre_tabla = os.path.splitext(os.path.basename(ruta_dbf))[0]
            f.write(f"CREATE TABLE {nombre_tabla} (\n")
            campos = []
            for field in dbf.fields:
                tipo_sql = convertir_tipo_dbf_a_sql(field.type, field.length)
                campos.append(f"    {field.name} {tipo_sql}")
            f.write(",\n".join(campos))
            f.write("\n);")
        print(f"Esquema extraído como SQL: {ruta_salida}")
    except Exception as e:
        print(f"Error al extraer esquema de {ruta_dbf}: {e}")