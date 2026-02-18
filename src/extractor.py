# src/extractor.py
import re
from pathlib import Path
import logging

def extraer_url(url: str) -> str:
    """
    Busca una URL dentro de una cadena de texto usando Regex.
    """
    es_url = r"(https?://\S+)"
    coincide = re.search(es_url, url)
    if coincide:
        return coincide.group(1)
    return None


def obtener_urls_desde_archivo(ruta_archivo: Path):
    """
    Lee un archivo línea por línea y devuelve una lista de URLs.
    Usa un bloque try-except por si el archivo no existe.
    """
    url_list = []
    try:
        for row in ruta_archivo.read_text(encoding="utf-8", errors="ignore").splitlines():
            strip = row.strip()
            if not strip:
                continue
            url_extraida = extraer_url(strip)
            if url_extraida:
                url_list.append(url_extraida)
            else:
                if strip.startswith("http://") or strip.startswith("https://"):
                 url_list.append(strip)
    except FileNotFoundError:
        logging.error(f"El archivo no se encontró en: {ruta_archivo}")
    except Exception as e:
        logging.error(f"Error inesperado al leer archivo: {e}")
    
    return url_list