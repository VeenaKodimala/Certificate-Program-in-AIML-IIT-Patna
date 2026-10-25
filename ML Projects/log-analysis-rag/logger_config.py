import logging
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent/"Application Logs"

LOG_DIR.mkdir(parents=True,exist_ok=True)
DEBUG_LOG=LOG_DIR/"debug.log"
ERROR_LOG=LOG_DIR/"error.log"

def setup_logging():
    logger=logging.getLogger()
    #Root stays at WARNING so third-party libs (httpx, urllib3, huggingface_hub...) don't emit DEBUG; project loggers opt in to DEBUG in get_logger().
    logger.setLevel(logging.WARNING)

    #getattr syntax: getattr(obj,parameter name,default_value if param doesn't exists)
    if getattr(logger,"_rag_log_configured",False):
        return

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | "
        "%(filename)s:%(lineno)d | %(message)s"
    )

    #ALL LEVELS OF LOG - DEBIG -> THEN DEBUG + ALL ABOVE
    debug_handler = logging.FileHandler(DEBUG_LOG,encoding="utf-8")
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(formatter)

    #Only errors have to be captured
    error_handler = logging.FileHandler(ERROR_LOG,encoding="utf-8")
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    # console_handler = logging.StreamHandler()
    # console_handler.setLevel(logging.INFO)
    # console_handler.setFormatter(formatter)

    logger.addHandler(debug_handler)
    logger.addHandler(error_handler)
    # logger.addHandler(console_handler)

    logger._rag_log_configured = True

def get_logger(name:str) -> logging.Logger:
    setup_logging()
    logger = logging.getLogger(name=name)
    logger.setLevel(logging.DEBUG)
    return logger





