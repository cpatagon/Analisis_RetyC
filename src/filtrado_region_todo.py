
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filtra todos los archivos RUEA-EFP por región.

Escanea la carpeta 'descargas_retc' buscando archivos con nombre
'ruea-efp-YYYY-ckan.csv' (y el XLSX 2021), filtra por la región indicada
(por defecto: 'Metropolitana de Santiago') y guarda los resultados en
'datos/filtrados_region/'. Además, genera un resumen de filas procesadas.

Uso:
  python filtrar_ruea_efp_rm.py --root . --region "Metropolitana de Santiago"

Requisitos: pandas, openpyxl
    pip install pandas openpyxl
"""
import argparse
import sys
from pathlib import Path
import re

import pandas as pd

EXPECTED_COLS = [
    "año","razon_social","rut_razon_social","nombre_establecimiento","id_vu","ciiu4","id_ciiu4",
    "rubro_vu","id_rubro_vu","region","provincia","comuna","id_comuna","latitud","longitud",
    "cantidad_toneladas","unidad","contaminantes","id_contaminantes","fuente_emisora_general","id_fuente_emisora"
]

NUMERIC_COMMA_COLS = ["latitud","longitud","cantidad_toneladas"]

def to_float_locale(val):
    if pd.isna(val):
        return pd.NA
    if isinstance(val, (int, float)):
        return val
    s = str(val).strip()
    if s == "":
        return pd.NA
    s = s.replace(",", ".")
    s = re.sub(r"\s+", "", s)
    try:
        return float(s)
    except Exception:
        return pd.NA

def normalize_columns(df):
    mapping = {c: str(c).strip() for c in df.columns}
    df = df.rename(columns=mapping)
    if all(col in df.columns for col in EXPECTED_COLS):
        df = df[EXPECTED_COLS]
    return df

def load_file(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path, sep=";", dtype=str, encoding="utf-8", engine="python")
    elif path.suffix.lower() in (".xlsx", ".xls"):
        return pd.read_excel(path, dtype=str)
    else:
        raise ValueError(f"Extensión no soportada: {path.suffix}")

def process_file(path: Path, region_target: str) -> pd.DataFrame:
    df = load_file(path)
    df = normalize_columns(df)
    if "region" not in df.columns:
        raise KeyError(f"El archivo {path.name} no contiene la columna 'region'.")
    df["region_norm"] = df["region"].map(lambda x: ("" if pd.isna(x) else str(x).strip().lower()))
    target = region_target.strip().lower()
    filtered = df[df["region_norm"] == target].copy()
    for col in NUMERIC_COMMA_COLS:
        if col in filtered.columns:
            filtered[col] = filtered[col].map(to_float_locale)
    if "region_norm" in filtered.columns:
        filtered = filtered.drop(columns=["region_norm"])
    cols = [c for c in EXPECTED_COLS if c in filtered.columns] + [c for c in filtered.columns if c not in EXPECTED_COLS]
    filtered = filtered[cols]
    return filtered

def main():
    ap = argparse.ArgumentParser(description="Filtra RUEA-EFP por región para todos los años disponibles")
    ap.add_argument("--root", default=".", help="Directorio raíz que contiene descargas_retc/ y datos/")
    ap.add_argument("--region", default="Metropolitana de Santiago", help="Nombre exacto de la región a filtrar")
    ap.add_argument("--outprefix", default="", help="Prefijo opcional para los archivos de salida (ej: 'RM_')")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    in_dir = root / "descargas_retc"
    out_dir = root / "datos" / "filtrados_region"
    out_dir.mkdir(parents=True, exist_ok=True)

    if not in_dir.exists():
        print(f"[✗] No existe la carpeta de entrada: {in_dir}", file=sys.stderr)
        sys.exit(1)

    candidates = sorted(list(in_dir.glob("ruea-efp-*-ckan.csv")) + list(in_dir.glob("ruea-efp-*-ckan.xlsx")))

    if not candidates:
        print(f"[!] No se encontraron archivos 'ruea-efp-*-ckan.(csv|xlsx)' en {in_dir}", file=sys.stderr)
        sys.exit(1)

    resumen = []
    for p in candidates:
        try:
            df_in = load_file(p)
            rows_in = len(df_in)
        except Exception as e:
            print(f"[!] Saltando {p.name} (error al leer): {e}", file=sys.stderr)
            resumen.append({"archivo": p.name, "filas_entrada": None, "filas_RM": None, "estado": f"error_lectura: {e}"})
            continue

        try:
            filtered = process_file(p, args.region)
        except Exception as e:
            print(f"[!] Saltando {p.name} (error al procesar): {e}", file=sys.stderr)
            resumen.append({"archivo": p.name, "filas_entrada": rows_in, "filas_RM": None, "estado": f"error_proceso: {e}"})
            continue

        rows_out = len(filtered)

        base = p.stem
        suf = "RM" if args.region.strip().lower() == "metropolitana de santiago" else args.region.strip().replace(" ", "_")
        base_out = f"{args.outprefix}{base}_{suf}" if args.outprefix else f"{base}_{suf}"

        out_csv = out_dir / f"{base_out}.csv"
        out_xlsx = out_dir / f"{base_out}.xlsx"

        try:
            filtered.to_csv(out_csv, index=False, encoding="utf-8-sig")
            filtered.to_excel(out_xlsx, index=False)
            estado = "ok"
        except Exception as e:
            print(f("[!] Error guardando {base_out}: {e}"), file=sys.stderr)
            estado = f"error_guardado: {e}"

        resumen.append({"archivo": p.name, "filas_entrada": rows_in, "filas_RM": rows_out, "estado": estado})

    df_resumen = pd.DataFrame(resumen, columns=["archivo","filas_entrada","filas_RM","estado"])
    df_resumen.to_csv(out_dir / "resumen_filtrado_ruea_efp.csv", index=False, encoding="utf-8-sig")
    print("[✓] Proceso completado.")
    print(f"    Archivos de salida en: {out_dir}")
    print(f"    Resumen: {out_dir / 'resumen_filtrado_ruea_efp.csv'}")

if __name__ == "__main__":
    main()
