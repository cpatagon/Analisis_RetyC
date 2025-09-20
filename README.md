# Descargador RETC — Emisiones al Aire (Fuentes Puntuales)

Este proyecto incluye un script para **descargar automáticamente** los archivos publicados (CSV/XLS/XLSX) del dataset **“Emisiones al aire de fuentes puntuales”** del RETC (MMA Chile).

Dataset: *Emisiones al aire de fuente puntuales* – RETC

---

## 🎯 Objetivo

Evitar descargas manuales: el script recorre la página del dataset, detecta los enlaces a archivos históricos y los guarda localmente en `datos/descargas_retc/`.

---

## 🧰 Requisitos

* **Python 3.8+**
* Paquetes:

  ```bash
  pip install requests beautifulsoup4
  ```
* (Opcional para Excel):

  ```bash
  pip install openpyxl
  ```

> Si usas Conda:
> `conda install -c conda-forge requests beautifulsoup4 openpyxl`

---

## 📂 Estructura recomendada

```
RetC/
├── datos/
│   └── descargas_retc/           # ← aquí se guardan las descargas
├── src/
│   └── descarga_retc.py          # ← script de descarga
└── README.md
```

---

## 🚀 Uso

Desde la **raíz del repositorio**:

```bash
# 1) Crear carpeta de salida (si no existe)
mkdir -p datos/descargas_retc

# 2) Ejecutar el descargador
python src/descarga_retc.py \
  --url "https://datosretc.mma.gob.cl/dataset/emisiones-al-aire-de-fuente-puntuales" \
  --out "datos/descargas_retc"
```

El script buscará enlaces a `.csv`, `.xls`, `.xlsx` y descargará todo en `datos/descargas_retc/`.

---

## ⚙️ Opciones útiles

* **Vista previa (sin descargar):**

  ```bash
  python src/descarga_retc.py --dry-run
  ```

* **Filtrar por nombre (regex):**
  (ej.: solo EFP históricos y 2023)

  ```bash
  python src/descarga_retc.py --pattern "ruea-efp|ckan_ruea_2023"
  ```

* **Sobrescribir si ya existe + reintentos:**

  ```bash
  python src/descarga_retc.py --overwrite --retries 5
  ```

* **Cambiar carpeta de salida:**

  ```bash
  python src/descarga_retc.py --out "/ruta/a/otra/carpeta"
  ```

---

## ✅ Verificación rápida

Listar los primeros archivos descargados:

```bash
ls -lh datos/descargas_retc | head
```

Contar por tipo:

```bash
find datos/descargas_retc -type f -iname "*.csv"  | wc -l
find datos/descargas_retc -type f -iname "*.xls"  | wc -l
find datos/descargas_retc -type f -iname "*.xlsx" | wc -l
```

Revisar un CSV:

```bash
wc -l datos/descargas_retc/ruea-efp-2019-ckan.csv
head -n 5 datos/descargas_retc/ruea-efp-2019-ckan.csv
```

---

## 🧪 Notas y problemas comunes

* **Cambios en la página del dataset:**
  Si el HTML cambia, ajusta el parser en `src/descarga_retc.py` (el script ya intenta buscar también dentro de iframes).

* **Errores de codificación al abrir CSV antiguos:**
  Algunos no están en UTF-8. Con pandas:

  ```python
  pd.read_csv("archivo.csv", encoding="latin-1")
  ```

* **Conexión inestable:**
  Usa `--retries` y vuelve a ejecutar. El script retoma archivo por archivo.

---

## ➡️ Pasos siguientes (opcional)

Una vez descargados, puedes filtrar por región y consolidar:

```bash
# Filtrar por Región Metropolitana (ejemplo):
python src/filtrado_region_todo.py --region "Metropolitana de Santiago"

# Consolidar EFP 2005–2022:
python src/consolidar_efp.py --indir datos/filtrados_region/CSV

# Consolidar 2005–2023 (EFP + RUEA 2023):
python src/consolidar_global_2005_2023.py \
  --indir "datos/filtrados_region/CONSOLIDADOS" \
  --efp-name EFP_RM_2005_2022_consolidado.csv \
  --r23-name ruea-efp-2023-ckan_RM.csv \
  --out CONSOLIDADO_RETC_2005-2023.csv
```

---

## 📜 Licencia y fuente de datos

* Los datos pertenecen al **RETC / Ministerio del Medio Ambiente (Chile)** y se rigen por su política de datos abiertos.
* Este script se provee para fines técnicos/ académicos; por favor, cita la fuente y revisa siempre la vigencia del dataset.
