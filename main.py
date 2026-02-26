import sys
print(f"--- Ejecutando desde: {sys.executable} ---")
import logging
from src.downloader import descargar_video
from src.extractor import obtener_urls_desde_archivo
from src import config


def configurar_sistema_de_logs():
    """
    Configura el sistema de logs para que guarde los mensajes en un archivo 
    y los muestre en la consola.
    """
    # Crea la carpeta de logs si no existe.
    config.CARPETA_LOGS.mkdir(exist_ok=True)
    
    # Configuración básica del logging.
    logging.basicConfig(
        level=config.NIVEL_LOG,
        filename=str(config.ARCHIVO_LOG),
        format=config.FORMATO_LOG,
        encoding=config.CODIFICACION_LOG
    )
    
    # Agrega un manejador para mostrar los logs también en la consola.
    consola = logging.StreamHandler()
    logging.getLogger('').addHandler(consola)

def procesar_descargas():
    """
    Función principal que orquesta el proceso de descarga de videos.
    1. Configura los logs.
    2. Obtiene la ruta de descarga desde las variables de entorno.
    3. Obtiene la lista de URLs a procesar (desde un archivo o desde la línea de comandos).
    4. Itera sobre la lista de URLs y las descarga una por una.
    """
    configurar_sistema_de_logs()
    logging.info("Iniciando el sistema de backup...")

    # Convertimos la ruta a un objeto Path para un manejo más robusto.
    ruta_base = config.BASE_DIR
    
    # --- LÓGICA DE OBTENCIÓN DE URLS ---
    urls_a_procesar = []

    # Si se pasa una URL como argumento en la línea de comandos, la usamos.
    if len(sys.argv) > 1:
        url_directa = sys.argv[1]
        urls_a_procesar.append(url_directa)
        logging.info(f"Se recibió una URL directamente por consola: {url_directa}")
    else:
        # Si no, leemos el archivo de URLs.
        logging.info(f"No se recibió URL por consola, se procederá a leer '{config.ARCHIVO_URLS}'.")
        if config.ARCHIVO_URLS.exists():
            urls_a_procesar = obtener_urls_desde_archivo(config.ARCHIVO_URLS)
            logging.info(f"Se encontraron {len(urls_a_procesar)} URLs en el archivo.")
        else:
            logging.warning(f"No se encontró el archivo '{config.ARCHIVO_URLS}' y tampoco se pasó una URL por consola.")
            return

    # --- MOTOR DE DESCARGA ---
    for url in urls_a_procesar:
        exito = descargar_video(url, ruta_base)
        
        if exito:
            logging.info(f"✅ Descarga finalizada con éxito: {url}")
        else:
            logging.warning(f"❌ Falló la descarga de: {url}")

    logging.info("=== Proceso de backup completado ===")

if __name__ == "__main__":
    procesar_descargas()