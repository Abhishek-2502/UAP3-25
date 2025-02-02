import configparser
import os
from colorama import Fore, Style
import pyfiglet
from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from app.models.models import (
    TextModel
)

from app.services.ocr_service import ImageTextExtractor
from app.services.extract_keywords_service import KeywordExtractor
from app.services.extract_keywords_service import ConfigurationManagerForKeywords

from app.models.BERTModel import BERTModel
from input_layer.embedding_generator import TextEmbedder
from app.configs.logging_config import setup_logger



# Configure logger
logger = setup_logger()

"""
# Flow
    Accepts an image file and a query simultaneously.
    Extracts text from the image.
    Extracts keywords from the text.
    Generates embeddings for the extracted keywords.
    Retrieves similar documents based on the embeddings.
    Resolves the user query using the retrieved documents.
"""

logger.info("Setting up the ASCII banner for routers.")
ascii_banner = pyfiglet.figlet_format("API Service")
print(Fore.CYAN + ascii_banner + Style.RESET_ALL)
logger.info("ASCII banner displayed.")

def load_config():
    """
    Load configuration from the config.ini file.
    """
    try:
        config_path = "config/config.ini"
        logger.info(f"Attempting to load configuration from {config_path}")

        if not os.path.exists(config_path):
            logger.error(f"Config file not found at {config_path}. Please create it and try again.")
            raise FileNotFoundError(f"Config file not found at {config_path}.")

        config = configparser.ConfigParser()
        config.read(config_path)

        # Retrieve API key and initialize the client
        text_length_limit = config["DEFAULT"].getint("text_length_limit", "")
        if not text_length_limit:
            logger.error("text_length_limit is missing or empty.")
            raise KeyError("text_length_limit is missing or empty.")
        logger.info("text_length_limit successfully loaded.")
        return text_length_limit

    except FileNotFoundError as e:
        logger.error(f"Configuration file error: {str(e)}")
        raise
    except KeyError as e:
        logger.error(f"Configuration key error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error while loading configuration: {str(e)}")
        raise

ocr_router = APIRouter()
embedded_router = APIRouter()

@ocr_router.post(
    "/upload-image-with-query",
    summary="Extract text and keywords from an uploaded image.",
)
async def upload_image(file: UploadFile = File(...), query: str = Form(...)):
    """
    Extracts text from an uploaded image and generates keywords based on the extracted text.

    Parameters:
        - file: The image file containing the content to extract text from.
        - query: The user query that will be returned along with the extracted text and keywords.

    Returns:
        - A JSON response containing:
            - image_text: Extracted text from the image.
            - query: The user query.
            - keywords: Keywords extracted from the image text.
    """
    try:
        logger.info("Received an image and a query for OCR processing.")
        logger.debug(f"Query received: {query}")

        if not file.filename:
            logger.error("No file was uploaded.")
            raise HTTPException(status_code=400, detail="No file uploaded.")

        # Validate file type (you may extend this for allowed formats)
        allowed_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tiff"}
        file_extension = file.filename.split(".")[-1].lower()

        if f".{file_extension}" not in allowed_extensions:
            logger.error(f"Unsupported file format: {file_extension}")
            raise HTTPException(status_code=400, detail="Unsupported file format. Please upload an image.")

        # Extract text from the image
        try:
            logger.info("Initializing the ImageTextExtractor Class.")
            extractor = ImageTextExtractor(file)

            logger.info("Extracting text from the image.")
            extracted_data = extractor.extract_text_from_image()
            logger.debug("Extracted text completed")

            if not extracted_data:
                logger.warning("No text extracted from the image.")
                raise HTTPException(status_code=422, detail="No text found in the image.")

        except Exception as e:
            logger.error(f"Failed to extract text from the image: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail="Error extracting text from the image.")

        # Load keyword extraction configuration
        try:
            logger.info("Initializing the ConfigurationManagerForKeywords Class.")
            config_keywords = ConfigurationManagerForKeywords()

            logger.info("Loading configuration for keyword extraction.")
            config_keywords.load_config()

        except Exception as e:
            logger.error(f"Failed to load keyword extraction configuration: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail="Error loading keyword extraction configuration.")

        # Extract keywords
        try:
            logger.info("Extracting keywords from the extracted text.")
            keyword_extractor = KeywordExtractor(extracted_data, config_keywords)
            keywords = keyword_extractor._extract_keywords()
            if not keywords:
                logger.warning("No keywords extracted.")
                raise HTTPException(status_code=422, detail="No keywords found in the extracted text.")
            logger.debug(f"Extracted keywords: {keywords}")

        except Exception as e:
            logger.error(f"Keyword extraction failed: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail="Error extracting keywords.")

        logger.info("OCR processing completed successfully.")

        # Return the response with extracted text and keywords
        return {
            "image_text": extracted_data,
            "query": query,
            "keywords": keywords,
        }

    except HTTPException as http_exc:
        # FastAPI's HTTPException will be returned directly with status codes
        return {"error": http_exc.detail}

    except Exception as e:
        # Catch any unexpected errors
        logger.critical(f"Unexpected error in OCR processing: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error during image processing.")

@embedded_router.post("/generate-embeddings", summary="Generate embeddings for text.")
async def generate_embeddings(text: TextModel):
    """
    Generate embeddings for the given text using BERT and return the result.

    Args:
        text (TextModel): The input text model containing the text to be embedded.

    Returns:
        dict: A dictionary containing either the embeddings or an error message.
    """
    try:
        logger.info(f"Received request to generate embeddings for text: {text.text}")

        # Validate input text
        if not text.text or not text.text.strip():
            logger.warning("Received empty or invalid text input.")
            raise HTTPException(status_code=400, detail="Input text cannot be empty.")
        # Validate input text length
        text_length_limit=load_config()
        if len(text.text) >  text_length_limit:
            logger.warning(f"Text input exceeds allowed limit: {len(text.text)} characters.")
            raise HTTPException(status_code=400, detail="Text input is too long. Maximum length is 10,000 characters.")

        try:
            # Initialize the BERT model
            logger.info("Initializing BERT model for embedding generation.")
            bert_model = BERTModel()
            logger.info("BERT model initialized successfully.")
        except Exception as model_error:
            logger.critical(f"Failed to load BERT model: {str(model_error)}", exc_info=True)
            raise HTTPException(status_code=500, detail="Error loading BERT model.") from model_error

        try:
            # Initialize the TextEmbedder
            logger.info("Initializing TextEmbedder.")
            text_embedder = TextEmbedder(bert_model)
            logger.info("TextEmbedder initialized successfully.")
        except Exception as embedder_error:
            logger.critical(f"Failed to initialize TextEmbedder: {str(embedder_error)}", exc_info=True)
            raise HTTPException(status_code=500, detail="Error initializing text embedder.") from embedder_error

        try:
            # Generate embeddings
            logger.info("Generating embeddings for the given text.")
            generated_embeddings = text_embedder._generate_text_embeddings(text.text)

            # Validate the generated embeddings
            if not isinstance(generated_embeddings, list):
                logger.error("Generated embeddings are not a list.")
                raise HTTPException(status_code=500, detail="Generated embeddings must be a list.")

            if not all(isinstance(value, float) for value in generated_embeddings):
                logger.error("Generated embeddings contain non-float values.")
                raise HTTPException(status_code=500, detail="Generated embeddings must be a list of floats.")

            if len(generated_embeddings) == 0:
                logger.warning("Generated embeddings are empty.")
                raise HTTPException(status_code=422, detail="Generated embeddings are empty.")

            logger.info("Embeddings generated and validated successfully.")
            return {"generated_embeddings": generated_embeddings}

        except Exception as embedding_error:
            logger.error(f"Error during embedding generation: {str(embedding_error)}", exc_info=True)
            raise HTTPException(status_code=500, detail="Error generating embeddings.") from embedding_error

    except HTTPException as http_exc:
        return {"error": http_exc.detail}

    except Exception as e:
        logger.critical(f"Unexpected error in generate_embeddings: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error during embedding generation.")
    