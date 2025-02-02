from fastapi import FastAPI
from colorama import Fore, Style
import pyfiglet
from app.configs.logging_config import setup_logger
from app.routers.routers import ocr_router, embedded_router

# Configure logger
logger = setup_logger()

class RAGFrameworkChatbot:
    """
    A class-based implementation for the RAG Framework Chatbot using FastAPI.
    Encapsulates app initialization and router inclusion.
    """

    def __init__(self):
        """
        Initialize the RAG Framework Chatbot.
        Sets up the FastAPI application and includes routers.
        """
        logger.info("Initializing the RAG Framework Chatbot application.")
        self.app = FastAPI(title="RAG Framework Chatbot", version="1.0.0")
        self._setup_ascii_banner()
        self._include_routers()
        logger.info("RAG Framework Chatbot application initialization complete.")

    def _setup_ascii_banner(self):
        """
        Display an ASCII banner for the RAG Framework Chatbot.
        """
        logger.info("Setting up the ASCII banner.")
        ascii_banner = pyfiglet.figlet_format("RAG Framework Chatbot")
        print(Fore.CYAN + ascii_banner + Style.RESET_ALL)
        logger.info("ASCII banner displayed.")

    def _include_routers(self):
        """
        Include routers for different functionalities in the FastAPI app.
        """
        logger.info("Including routers into the FastAPI application.")
        try:
            self.app.include_router(ocr_router, prefix="/ocr", tags=["OCR"])
            logger.info("OCR router included successfully.")
            self.app.include_router(embedded_router, prefix="/embedded", tags=["Embedded"])
            logger.info("Embedded router included successfully.")
        except Exception as e:
            logger.error(f"Error including routers: {str(e)}", exc_info=True)
            raise

    def get_app(self):
        """
        Retrieve the FastAPI application instance.

        Returns:
            FastAPI: The FastAPI application instance.
        """
        logger.info("Retrieving the FastAPI application instance.")
        return self.app

# Initialize the RAG Framework Chatbot
try:
    logger.info("Starting RAG Framework Chatbot initialization.")
    rag_framework = RAGFrameworkChatbot()
    app = rag_framework.get_app()
    logger.info("RAG Framework Chatbot initialized and app instance retrieved.")
except Exception as e:
    logger.critical(f"Critical failure during chatbot initialization: {str(e)}", exc_info=True)
    raise
