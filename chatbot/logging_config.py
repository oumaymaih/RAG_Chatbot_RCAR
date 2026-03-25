import logging
import warnings

# chatbot/logging_config.py
import logging
import warnings

def configure_logging(log_file="app.log", log_to_console=False):
    """
    Configure le logging global pour toute l'application
    et capture tous les warnings pour les enregistrer dans le fichier de logs.
    """
    handlers = [logging.FileHandler(log_file, mode='a', encoding='utf-8')]
    if log_to_console:
        handlers.append(logging.StreamHandler())

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
        handlers=handlers
    )

    # Capture tous les warnings Python vers le logger
    logging.captureWarnings(True)
    
    # Forcer l'affichage de tous les warnings (même DeprecationWarning)
    warnings.simplefilter("always")

    logging.info("📄 Logging configuré et prêt à enregistrer tous les warnings.")



















# Version qui n'enregistre pas les warnings #
#def configure_logging(log_file="app.log", log_to_console=False):
    #"""
    #Configure logging global pour toute l'application.
    #Redirige aussi les warnings vers le logging.
    #"""
    #handlers = [logging.FileHandler(log_file, mode='a', encoding='utf-8')]
    #if log_to_console:
        #handlers.append(logging.StreamHandler())

    #logging.basicConfig(
        #level=logging.INFO,
        #format="%(asctime)s [%(levelname)s] %(message)s",
        #handlers=handlers
    #)

    # Redirige les warnings Python vers le logging
    #def warn_to_log(message, category, filename, lineno, file=None, line=None):
        #logging.warning(f"{filename}:{lineno}: {category.__name__}: {message}")

    #warnings.showwarning = warn_to_log

    # Ignore certains warnings si tu veux un log plus propre
    #warnings.filterwarnings("ignore", category=DeprecationWarning)
    #warnings.filterwarnings("ignore", category=UserWarning)