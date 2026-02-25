# src/extractor.py
import re
from pathlib import Path
import logging

def extraer_url(texto: str) -> str:
    """
    Busca una URL válida dentro de una cadena de texto.
    Utiliza una expresión regular para encontrar patrones que comiencen con http:// o https://.
    
    Args:
        texto: La cadena de texto donde buscar la URL.
        
    Returns:
        La primera URL encontrada en el texto, o None si no se encuentra ninguna.
    """
    patron_url = r"(https?://\S+)"
    coincidencia = re.search(patron_url, texto)
    if coincidencia:
        return coincidencia.group(1)
    return None


def obtener_urls_desde_archivo(ruta_archivo: Path) -> list[str]:
    """
    Lee un archivo de texto línea por línea y extrae todas las URLs que encuentra.
    
    Args:
        ruta_archivo: La ruta al archivo de texto.
        
    Returns:
        Una lista de strings, donde cada string es una URL.
    """
    lista_urls = []
    try:
        # Leemos el archivo, lo dividimos en líneas y procesamos una por una.
        for linea in ruta_archivo.read_text(encoding="utf-8", errors="ignore").splitlines():
            # Quitamos espacios en blanco al principio y al final.
            linea_limpia = linea.strip()
            
            # Si la línea está vacía, la ignoramos.
            if not linea_limpia:
                continue
            
            # Intentamos extraer una URL de la línea.
            url_extraida = extraer_url(linea_limpia)
            
            if url_extraida:
                lista_urls.append(url_extraida)
            # Como caso alternativo, si la línea entera parece una URL, la agregamos.
            elif linea_limpia.startswith("http://") or linea_limpia.startswith("https://"):
                 lista_urls.append(linea_limpia)
                 
    except FileNotFoundError:
        logging.error(f"El archivo no se encontró en: {ruta_archivo}")
    except Exception as e:
        logging.error(f"Error inesperado al leer el archivo: {e}")
    
    return lista_urls