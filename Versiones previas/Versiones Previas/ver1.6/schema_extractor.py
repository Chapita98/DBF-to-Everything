import os
from dbfread import DBF

def mapear_tipo_dbf_a_dotnet(tipo, longitud):
    """Mapea tipos de DBF a tipos .NET basados en el tipo y longitud del campo."""
    tipo = tipo.upper()
    if tipo == 'C':  # Character
        return "System.String"
    elif tipo == 'N':  # Numeric
        if longitud <= 18:
            return "System.Decimal"
        else:
            return "System.String"  # Números muy grandes como strings
    elif tipo == 'D':  # Date
        return "System.DateTime"
    elif tipo == 'L':  # Logical
        return "System.Boolean"
    else:
        return "System.String"  # Por defecto

def extraer_schema(ruta_dbf, ruta_salida):
    try:
        dbf = DBF(ruta_dbf, load=False)
        with open(ruta_salida, 'w', encoding='utf-8') as f:
            # Escribir encabezado del informe de metadatos
            f.write("ColumnName\tColumnOrdinal\tColumnSize\tNumericPrecision\tNumericScale\tDataType\tProviderType\tIsLong\tAllowDBNull\tIsReadOnly\tIsRowVersion\tIsUnique\tIsKey\tIsAutoIncrement\n")
            for ordinal, field in enumerate(dbf.fields, start=0):
                nombre = field.name.lower()  # Normalizamos a minúsculas como en tu ejemplo
                tipo_dbf = field.type
                longitud = field.length
                # Precisión y escala para tipos numéricos, valores por defecto para otros
                precision = field.length if tipo_dbf == 'N' else 255
                scale = 0 if tipo_dbf == 'N' else 255
                data_type = mapear_tipo_dbf_a_dotnet(tipo_dbf, longitud)
                # Mapeo de ProviderType según tipos comunes
                provider_type = (
                    129 if data_type == "System.String" else
                    131 if data_type == "System.Decimal" else
                    133 if data_type == "System.DateTime" else
                    11 if data_type == "System.Boolean" else
                    130
                )
                is_long = "TRUE" if tipo_dbf == 'M' else "FALSE"  # Solo para campos Memo
                allow_db_null = "TRUE"  # Asumimos que todos pueden ser nulos
                is_read_only = "FALSE"
                is_row_version = "FALSE"
                # Asumimos valores por defecto para estas propiedades
                is_unique = "FALSE"  # No hay info en DBF
                is_key = "FALSE"  # Podríamos inferir que 'cod_sistem' es clave, pero no hay evidencia directa
                is_auto_increment = "FALSE"  # No hay info en DBF
                # Escribir línea de metadatos
                f.write(f"{nombre}\t{ordinal}\t{longitud}\t{precision}\t{scale}\t{data_type}\t{provider_type}\t{is_long}\t{allow_db_null}\t{is_read_only}\t{is_row_version}\t{is_unique}\t{is_key}\t{is_auto_increment}\n")
        print(f"Metadatos extraídos en: {ruta_salida}")
    except Exception as e:
        print(f"Error al extraer metadatos de {ruta_dbf}: {e}")

# Ejemplo de uso (descomentar para probar directamente)
# extraer_schema("ruta_a_tu_archivo.dbf", "salida_schema.txt")