import os
from dbfread import DBF

def convertir_tipo_dbf_a_sql(tipo, longitud):
    """Convierte tipos de DBF a tipos SQL aproximados."""
    tipo = tipo.upper()
    if tipo == 'C':
        return f"VARCHAR({longitud})"
    elif tipo == 'N':
        return f"DECIMAL({longitud},0)"
    elif tipo == 'D':
        return "DATE"
    elif tipo == 'L':
        return "BOOLEAN"
    else:
        return f"VARCHAR({longitud})"

def extraer_schema(ruta_dbf, ruta_salida, constraints):
    try:
        dbf = DBF(ruta_dbf, load=False)
        with open(ruta_salida, 'w', encoding='utf-8') as f:
            nombre_tabla = os.path.splitext(os.path.basename(ruta_dbf))[0]
            f.write(f"CREATE TABLE {nombre_tabla} (\n")
            campos_sql = []
            for field in dbf.fields:
                nombre = field.name
                tipo_sql = convertir_tipo_dbf_a_sql(field.type, field.length)
                if constraints.get(nombre, {}).get("Autoincrement", False):
                    tipo_sql += " AUTO_INCREMENT"
                campos_sql.append(f"    {nombre} {tipo_sql}")

            # Agregar PK
            pks = [nombre for nombre, config in constraints.items() if config.get("PK", False)]
            if pks:
                campos_sql.append(f"    PRIMARY KEY ({', '.join(pks)})")

            # Agregar FK
            for nombre, config in constraints.items():
                if config.get("FK", False) and config.get("FK_Table") and config.get("FK_Column"):
                    campos_sql.append(f"    FOREIGN KEY ({nombre}) REFERENCES {config['FK_Table']} ({config['FK_Column']})")

            # Agregar UNIQUE
            for nombre, config in constraints.items():
                if config.get("Unique", False):
                    campos_sql.append(f"    UNIQUE ({nombre})")

            f.write(",\n".join(campos_sql))
            f.write("\n);")
        print(f"Esquema extraído como SQL: {ruta_salida}")
    except Exception as e:
        print(f"Error al extraer esquema de {ruta_dbf}: {e}")