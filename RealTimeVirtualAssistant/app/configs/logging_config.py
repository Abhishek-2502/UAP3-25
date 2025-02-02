import logging
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class ColoredFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: Fore.YELLOW,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.MAGENTA,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT,
    }

    def format(self, record):
        color = self.COLORS.get(record.levelno, "")
        message = super().format(record)
        return f"{color}{message}"

def setup_logger():
    logger = logging.getLogger("RealTimeVirtualAssistant")

    if not logger.hasHandlers():  # Prevent adding multiple handlers
        formatter = ColoredFormatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        logger.setLevel(logging.DEBUG)  # Adjust log level as needed
        logger.addHandler(handler)
    return logger
