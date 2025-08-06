# DBF-to-Everything

## Descripción
Convierte archivos .dbf a varios formatos y ofrece utilidades adicionales (Excel, CSV, JSON, extracción de schema, renombrado, fusión, estadísticas, validación, etc.).

## Uso rápido
1. Ejecuta el programa:
   - Si tienes el ejecutable: abre `dist/DbfToEverything.exe`.
   - Si usas Python: ejecuta `python menu.py`.


2. Selecciona la función deseada desde el menú principal:
   - **Dbf to Excel**: Convierte archivos DBF a Excel (.xlsx) con opciones de personalización de formato, nombres y columnas.
   - **Convertir Raíz a Excel**: Convierte todos los archivos DBF de una carpeta raíz (y subcarpetas) a Excel, replicando la estructura de carpetas. Incluye:
     - Progreso visual con contador y porcentaje (por archivo grande).
     - Indicación del archivo actual en proceso.
     - Intervención manual para archivos con tipos no reconocidos, permitiendo elegir el nombre y ruta del Excel de salida.
     - Opción de fragmentar archivos grandes en varias hojas o archivos.
     - Registro detallado de errores y omisión de archivos demasiado grandes.
   - **Extraer Schema**: Extrae el esquema SQL de uno o varios DBF.
   - **Extraer TODO el Schema**: Extrae recursivamente el schema SQL de todos los DBF en una carpeta y subcarpetas, con intervención manual para tipos no reconocidos.
   - **Dbf to CSV**: Convierte DBF a CSV.
   - **Dbf a JSON**: Convierte DBF a JSON.
   - **Visualizar DBF**: Muestra una vista previa del DBF en formato tabla.
   - **Renombrar campos**: Cambia los nombres de los campos y exporta a CSV.
   - **Fusionar DBFs**: Une varios DBF en un solo archivo CSV.
   - **Estadísticas DBF**: Muestra información básica del archivo (campos, tipos, cantidad de registros).
   - **Validar integridad**: Busca registros corruptos en el DBF.

## Funciones avanzadas y mejoras recientes
- Progreso visual y porcentaje de avance por archivo en conversiones masivas.
- Intervención manual para archivos problemáticos (tipos no reconocidos), permitiendo elegir el archivo de salida.
- Registro de todas las acciones y errores (con traceback) en la carpeta `logs`.
- Personalización de formato de salida Excel (fuente, ancho, encabezado, etc.).
- Ventanas centradas y diseño vertical para mejor usabilidad.
- Opción de sobrescribir o renombrar archivos de salida existentes.
- Fragmentación automática de archivos grandes.



## Registro de acciones (logs)
Todas las acciones importantes del programa se registran automáticamente en `logs/registro_programa.txt`.
Errores de conversión y detalles técnicos se guardan en archivos como `logs/errores_excel_raiz.txt` y `logs/errores_schema.txt`.
Puedes revisar estos archivos para ver un historial de conversiones, errores y eventos relevantes.

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
