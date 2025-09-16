# Descargador de Archivos RETC (Emisiones al Aire de Fuentes Puntuales)

Este script en Python permite automatizar la descarga de los archivos **XLS/XLSX** y **CSV** publicados en el portal de datos del RETC del Ministerio del Medio Ambiente de Chile:

👉 [Emisiones al aire de fuentes puntuales](https://datosretc.mma.gob.cl/dataset/emisiones-al-aire-de-fuente-puntuales)

---

## 🎯 Objetivo

Facilitar la obtención de los archivos históricos de emisiones al aire, sin necesidad de descargarlos manualmente desde la página web.  
El script analiza el HTML del portal, identifica los enlaces disponibles a **.xls**, **.xlsx** y **.csv**, y los guarda en una carpeta local.

---

## ⚙️ Características

- Descarga automática de todos los archivos publicados en el dataset.
- Compatible con Linux (requiere Python 3).
- Guarda los archivos en una carpeta llamada `descargas_retc`.
- Reconstruye enlaces absolutos en caso de que estén definidos de forma relativa.
- Uso de librerías estándar: `requests` y `BeautifulSoup4`.

---

## 📦 Requisitos

Antes de ejecutar el script asegúrate de tener instaladas las librerías necesarias:

```bash
sudo apt update
sudo apt install python3-pip -y
pip3 install requests beautifulsoup4
```

---

## 🚀 Uso

1. Clona o descarga este repositorio (o simplemente guarda el script `descargar_retc.py` en tu carpeta de trabajo).

2. Dale permisos de ejecución:

   ```bash
   chmod +x descargar_retc.py
   ```

3. Ejecuta el script:

   ```bash
   ./descargar_retc.py
   ```

4. Una vez finalizado, los archivos descargados estarán en la carpeta:

   ```
   descargas_retc/
   ```

---

## 📂 Estructura de Archivos

```
.
├── descargar_retc.py   # Script principal
├── README.md           # Este archivo
└── descargas_retc/     # Carpeta donde se guardan los archivos descargados
```

---

## 📝 Notas

- Si el portal actualiza los enlaces o cambia la estructura, puede ser necesario ajustar el script.
- Recomendado revisar la integridad de los archivos descargados antes de procesarlos.
- El script está pensado para uso académico y técnico, respetando siempre las políticas de uso de datos abiertos del MMA Chile.

---
