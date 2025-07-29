import os
from dbfread import DBF

def convertir_tipo_dbf_a_sql(tipo, longitud, config, nombre_campo):
    tipo = tipo.upper()
    if tipo == 'C':
        tam = config.get("Tamaño", "Original")
        if tam == "Personalizado":
            tam = config.get("Tamaño_Personalizado", longitud)
        elif tam in ["20", "50", "150"]:
            tam = int(tam)
        else:
            tam = longitud
        return f"VARCHAR({tam})"
    elif tipo == 'N':
        tam = config.get("Tamaño", "Original")
        if tam == "Personalizado":
            tam = config.get("Tamaño_Personalizado", longitud)
        elif tam in ["20", "50", "150"]:
            tam = int(tam)
        else:
            tam = longitud
        return f"DECIMAL({tam},0)"
    elif tipo == 'D' or 'FECHA' in nombre_campo.upper():
        return "DATE"
    elif tipo == 'T' or 'HORA' in nombre_campo.upper():
        return "TIME"
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
                config = constraints.get(nombre, {})
                tipo_sql = convertir_tipo_dbf_a_sql(field.type, field.length, config, nombre)
                if config.get("Autoincrement", False):
                    tipo_sql += " AUTO_INCREMENT"
                campos_sql.append(f"    {nombre} {tipo_sql}")

            pks = [nombre for nombre, config in constraints.items() if config.get("PK", False)]
            if pks:
                campos_sql.append(f"    PRIMARY KEY ({', '.join(pks)})")

            f.write(",\n".join(campos_sql))
            f.write("\n);")
    except Exception as e:
        print(f"Error al extraer esquema: {e}")