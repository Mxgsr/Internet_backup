# src/downloader.py
import yt_dlp
import logging
from pathlib import Path

def descargar_video(url: str, carpeta_base: Path) -> bool:
    """
    Descarga un video o pista de audio usando yt-dlp de forma segura.
    Retorna True si la descarga fue exitosa o ya existía, False si falló.
    """
    
    # Archivo histórico para lograr la "Idempotencia" (no repetir descargas)
    archivo_historial = carpeta_base / ".downloaded.txt"

    # Configuramos las reglas del motor yt-dlp
    opciones = {
        # Guardamos organizando por plataforma (ej. Tidal) y luego el título
        'outtmpl': str(carpeta_base / '%(extractor_key)s' / '%(title)s.%(ext)s'),
        'format': 'bestaudio/best',  # Como tienes links de Tidal, priorizamos audio
        'merge_output_format' : 'mkv',
        'download_archive': str(archivo_historial),
        'quiet': True,
        'no_warnings': True,
    }

    try:
        logging.info(f"Procesando: {url}")
        
        # Inicia el motor de yt-dlp usando un bloque 'with' pasándole 'opciones'.
        with yt_dlp.YoutubeDL(opciones) as ydl:
            ydl.download([url])
        logging.info(f"Éxito: {url}")
        return True

    # Capturamos primero el error específico de la librería (ej: video borrado)
    except yt_dlp.utils.DownloadError as e:
        logging.error(f"No se pudo descargar {url}. Razón: {e}")
        return False
        
    # Capturamos cualquier otro error catastrófico (ej: disco duro lleno)
    except Exception as e:
        logging.error(f"Error crítico inesperado en {url}: {e}")
        return False