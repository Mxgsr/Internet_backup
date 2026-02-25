# src/downloader.py
import yt_dlp
import logging
from pathlib import Path
from src import config

def descargar_video(url: str, carpeta_base: Path) -> bool:
    """
    Descarga un video o pista de audio de una URL utilizando yt-dlp.

    Esta función es "idempotente", lo que significa que si un video ya ha sido 
    descargado, no intentará descargarlo de nuevo. Esto se logra gracias al 
    archivo de historial de descargas.

    Args:
        url: La URL del video o audio a descargar.
        carpeta_base: La carpeta raíz donde se guardarán las descargas.

    Returns:
        True si la descarga fue exitosa o si el video ya existía.
        False si ocurrió un error durante la descarga.
    """
    
    # Construimos la ruta al archivo de historial de descargas.
    archivo_historial = carpeta_base / config.ARCHIVO_HISTORIAL_DESCARGAS

    # Hacemos una copia de las opciones de configuración para no modificar el original.
    opciones = config.OPCIONES_YT_DLP.copy()
    
    # Actualizamos las rutas en las opciones para que sean absolutas.
    opciones['outtmpl'] = str(carpeta_base / opciones['outtmpl'])
    opciones['download_archive'] = str(archivo_historial)

    try:
        logging.info(f"Procesando URL: {url}")
        
        # Usamos 'with' para asegurarnos de que los recursos de yt-dlp se liberen.
        with yt_dlp.YoutubeDL(opciones) as ydl:
            ydl.download([url])
            
        logging.info(f"Procesamiento finalizado para: {url}")
        return True

    # Capturamos errores específicos de la descarga (ej: video no disponible).
    except yt_dlp.utils.DownloadError as e:
        logging.error(f"No se pudo descargar '{url}'. Razón: {e}")
        return False
        
    # Capturamos cualquier otro error inesperado (ej: falta de espacio en disco).
    except Exception as e:
        logging.error(f"Ocurrió un error crítico e inesperado con '{url}': {e}")
        return False