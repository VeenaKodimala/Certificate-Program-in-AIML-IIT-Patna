import logging
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent/"Application Logs"

LOG_DIR.mkdir(parents=True,exist_ok=True)
DEBUG_LOG=LOG_DIR/"debug.log"
ERROR_LOG=LOG_DIR/"error.log"

def setup_logging():
    logger=logging.getLogger()
    #If level=DEBUG, then all level heigher INFO,ERROR,WARNING plus DEBUG will be loggeed.
    logger.setLevel(logging.DEBUG)

    if logging.handlers:
        return

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | "
        "%(filename)s:%(lineno)d | %(message)s"
    )