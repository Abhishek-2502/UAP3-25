import os
import sys
import configparser
import uvicorn
from app.configs.logging_config import setup_logger

# Setup logger
logger = setup_logger()

# Load configuration with error handling
config = configparser.ConfigParser()

try:
    config_path = "config/config.ini"
    logger.info(f"Attempting to load configuration from {config_path}")

    if not os.path.exists(config_path):
        logger.error(f"Config file not found at {config_path}. Please create it and try again.")
        raise FileNotFoundError(f"Config file not found at {config_path}.")

    config = configparser.ConfigParser()
    config.read(config_path)

    # Read server settings with error handling
    HOST = config["server"].get("host", "").strip()
    PORT = config["server"].getint("port", "")
    RELOAD = config["server"].getboolean("reload", "")
    LOGLEVEL = config["server"].get("loglevel", "").strip()

except (configparser.Error, ValueError, KeyError) as config_error:
    logger.critical(f"Error reading configuration: {str(config_error)}", exc_info=True)
    sys.exit(1)

def main():
    try:
        logger.info(f"Starting FastAPI app on {HOST}:{PORT} (reload={RELOAD})")
        uvicorn.run("app.main:app", host=HOST, port=PORT, reload=RELOAD, log_level=LOGLEVEL)
    except Exception as e:
        logger.critical(f"Failed to start the FastAPI app: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
