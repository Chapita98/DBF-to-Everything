# DBF-to-Everything

## Descripción
Convierte archivos .dbf a varios formatos y ofrece utilidades adicionales (Excel, CSV, JSON, extracción de schema, renombrado, fusión, estadísticas, validación, etc.).

## Uso rápido
1. Ejecuta el programa:
   - Si tienes el ejecutable: abre `dist/DbfToEverything.exe`.
   - Si usas Python: ejecuta `python menu.py`.

2. Selecciona la función deseada desde el menú principal:
   - **Dbf to Excel**: Convierte archivos DBF a Excel (.xlsx).
   - **Convertir Raíz a Excel**: Convierte todos los archivos DBF de una carpeta raíz (y subcarpetas) a Excel, replicando la estructura de carpetas. Si un archivo supera el máximo de filas de Excel, se omite y se notifica.
   - **Extraer Schema**: Extrae el esquema SQL de uno o varios DBF.
   - **Dbf to CSV**: Convierte DBF a CSV.
   - **Dbf a JSON**: Convierte DBF a JSON.
   - **Visualizar DBF**: Muestra una vista previa del DBF.
   - **Renombrar campos**: Cambia los nombres de los campos y exporta a CSV.
   - **Fusionar DBFs**: Une varios DBF en un solo archivo CSV.
   - **Estadísticas DBF**: Muestra información básica del archivo.
   - **Validar integridad**: Busca registros corruptos en el DBF.
   - **Extraer TODO el Schema**: Extrae recursivamente el schema SQL de todos los DBF en una carpeta y subcarpetas.

## Registro de acciones (logs)
Todas las acciones importantes del programa se registran automáticamente en `logs/registro_programa.txt`.
Puedes revisar este archivo para ver un historial de conversiones, errores y eventos relevantes.

## Requisitos
- Python 3.8+
- Paquetes: dbfread, pandas, openpyxl, tkinter

Instala dependencias con:
```
pip install dbfread pandas openpyxl
```

## Notas
- El programa crea automáticamente las carpetas de salida si no existen.
- Los nombres de archivos se limpian para evitar caracteres no válidos en Windows.
- Si un archivo de salida ya existe, se pregunta si deseas sobrescribirlo.

---
Autor: Chapita98
