#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import os

# URL del dataset
URL = "https://datosretc.mma.gob.cl/dataset/emisiones-al-aire-de-fuente-puntuales"

# Carpeta de destino
DEST_DIR = "descargas_retc"
os.makedirs(DEST_DIR, exist_ok=True)

# Obtener HTML de la página
print("[+] Obteniendo listado de archivos...")
resp = requests.get(URL)
resp.raise_for_status()

soup = BeautifulSoup(resp.text, "html.parser")

# Buscar todos los enlaces que terminen en .xls, .xlsx o .csv
links = []
for a in soup.find_all("a", href=True):
    href = a["href"]
    if href.endswith((".xls", ".xlsx", ".csv")):
        # Asegurar que el enlace sea absoluto
        if href.startswith("/"):
            href = "https://datosretc.mma.gob.cl" + href
        links.append(href)

print(f"[+] Encontrados {len(links)} archivos para descargar.")

# Descargar archivos
for url in links:
    filename = os.path.join(DEST_DIR, os.path.basename(url))
    print(f"  -> Descargando {filename}")
    r = requests.get(url, stream=True)
    r.raise_for_status()
    with open(filename, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

print("[+] Descarga finalizada. Archivos guardados en:", DEST_DIR)
