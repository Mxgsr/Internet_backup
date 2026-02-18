import sys
print(f"--- Ejecutando desde: {sys.executable} ---")
import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from src.downloader import descargar_video

# Importamos tu función. Fíjate que usamos 'src.extractor'
from src.extractor import obtener_urls_desde_archivo

# Cargar variables del archivo .env
load_dotenv()

def configurar_logs():
    """Configura el logging para que guarde en un archivo y muestre en consola."""
    log_folder = Path('logs')
    log_folder.mkdir(exist_ok=True)
    log_file = log_folder / "backup.log"
    logging.basicConfig(
        level=logging.INFO,
        filename=str(log_file),
        format='%(asctime)s - %(levelname)s - %(message)s',
        encoding='utf-8'
    )
    console = logging.StreamHandler()
    logging.getLogger('').addHandler(console)

def ejecutar():
    configurar_logs()
    logging.info("Iniciando el sistema de backup...")

    # Cero Hardcoding: Leemos la ruta desde el .env
    ruta_str = os.getenv("BASE_DIR")
    
    if not ruta_str:
        logging.error("No se encontró la variable BASE_DIR en el .env")
        return

    # Convertimos el string a un objeto Path profesional
    ruta_base = Path(ruta_str).expanduser()
    
    # --- PRUEBA DEL EXTRACTOR ---
    archivo_lista = Path('lista.txt')
    if not archivo_lista.exists():
        logging.warning(f"No se encontró el archivo {archivo_lista}.")
        return
    
    url_encontradas = obtener_urls_desde_archivo(archivo_lista)
    url_quantity = len(url_encontradas)
    logging.info(f"Se han encontrado {url_quantity} URLs en el archivo")
    for row in url_encontradas:
        print(f"{row}")
    
    logging.info(f"Ruta de backups configurada en: {ruta_base}")

    # EL MOTOR DE DESCARGA
    for url in url_encontradas:
        # Llamamos a la función que creamos en src/downloader.py
        exito = descargar_video(url, ruta_base)
        
        if exito:
            logging.info(f"✅ Finalizado con éxito: {url}")
        else:
            logging.warning(f"❌ Falló la descarga de: {url}")

    logging.info("=== Proceso de backup completado ===")

if __name__ == "__main__":
    ejecutar()