# src/config.py
from pathlib import Path

# --- CONFIGURACIÓN DE LOGS ---
# Define la carpeta donde se guardarán los archivos de registro.
CARPETA_LOGS = Path('logs')

# Define el nombre del archivo de registro.
ARCHIVO_LOG = CARPETA_LOGS / "backup.log"

# Define el nivel de registro (DEBUG, INFO, WARNING, ERROR, CRITICAL).
NIVEL_LOG = "INFO"

# Define el formato de los mensajes de registro.
FORMATO_LOG = '%(asctime)s - %(levelname)s - %(message)s'

# Define la codificación de caracteres para el archivo de registro.
CODIFICACION_LOG = 'utf-8'


# --- CONFIGURACIÓN DE ARCHIVOS ---
# Define el nombre del archivo que contiene las URLs a descargar.
ARCHIVO_URLS = Path('links.txt')

# Define el nombre del archivo que almacena el historial de descargas.
# Este archivo ayuda a evitar que se descarguen los mismos videos multiples veces.
ARCHIVO_HISTORIAL_DESCARGAS = ".downloaded.txt"


# --- CONFIGURACIÓN DE YT-DLP ---
# Opciones para la librería yt-dlp.
# Puedes encontrar más opciones en la documentación de yt-dlp:
# https://github.com/yt-dlp/yt-dlp#usage-and-options
OPCIONES_YT_DLP = {
    # Define la plantilla para nombrar los archivos descargados.
    # Se guardarán en una carpeta con el nombre de la plataforma (ej. Youtube)
    # y el nombre del video.
    'outtmpl': '%(extractor_key)s/%(title)s.%(ext)s',

    # Define el formato de video y audio a descargar.
    # 'bestvideo*+bestaudio/best' intenta descargar la mejor calidad de video y audio por separado
    # y luego los une. Si no es posible, descarga la mejor calidad disponible.
    'format': 'bestvideo*+bestaudio/best',

    # Define el formato del archivo de video cuando se unen video y audio.
    'merge_output_format': 'mkv',

    # Evita que yt-dlp imprima mensajes en la consola.
    'quiet': True,

    # Suprime las advertencias de yt-dlp.
    'no_warnings': True,
}
