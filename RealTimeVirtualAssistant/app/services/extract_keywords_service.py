import os
import configparser
from groq import Groq
from app.configs.logging_config import setup_logger
from app.prompts.prompt import get_keyword_prompt

# Configure logger
logger = setup_logger()


class ConfigurationManagerForKeywords:
    """
    A class to manage configuration and Groq client initialization.
    Encapsulates parameters, model, and client details.
    """

    def __init__(self):
        """
        Initialize the ConfigurationManager with default values.
        """
        self.parameters = []  # List of parameters to extract from the image text
        self.model = None  # Model name for Groq API
        self.client = None  # Groq API client instance
        logger.info("ConfigurationManager initialized.")

    def load_config(self):
        """
        Load configuration from the config.ini file.
        Ensures that the API key, model, and parameters are properly set.
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
            api_key = config["DEFAULT"].get("key", "").strip()
            if not api_key:
                logger.error("API key is missing or empty.")
                raise KeyError("API key is missing or empty.")
            logger.info("API key successfully loaded.")
            self._initialize_groq(api_key)

            # Retrieve the model
            self.model = config["DEFAULT"].get("model_keyword", "").strip()
            if not self.model:
                logger.error("Model is missing or empty.")
                raise KeyError("Model is missing or empty.")
            logger.info(f"Model '{self.model}' successfully loaded.")

            # Retrieve the list of parameters
            self.parameters = [param.strip() for param in config["DEFAULT"].get("parameters", "").split(",") if param.strip()]
            if not self.parameters:
                logger.error("Parameters are missing or empty.")
                raise KeyError("Parameters are missing or empty.")
            logger.info(f"Parameters successfully loaded: {self.parameters}")

        except FileNotFoundError as e:
            logger.error(f"Configuration file error: {str(e)}")
            raise
        except KeyError as e:
            logger.error(f"Configuration key error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while loading configuration: {str(e)}")
            raise

    def _initialize_groq(self, api_key):
        """
        Initialize the Groq client with the provided API key.
        Ensures the client is ready for use.

        Args:
            api_key (str): The API key for Groq.
        """
        try:
            logger.info("Initializing Groq client.")
            self.client = Groq(api_key=api_key)
            logger.info("Groq client initialized successfully.")
        except Exception as e:
            error_message = (
                "Failed to initialize Groq client. Please ensure the API key is valid, "
                "your network connection is active, and the Groq service is reachable. "
                f"Error details: {e}"
            )
            logger.error(error_message)
            raise RuntimeError(error_message)



class KeywordExtractor:
    def __init__(self, image_text, config_manager):
        """
        Initialize the KeywordExtractor with the provided image text and configuration manager.
        
        Args:
            image_text (dict): Dictionary containing the text extracted from the image.
            config_manager (ConfigurationManager): An instance of ConfigurationManager to access configuration and Groq client.
        """
        self.image_text = image_text
        self.config_manager = config_manager
        logger.info("KeywordExtractor initialized.")

    def _extract_data(self):
        """
        Extract and clean up the data from the image_text based on dynamic parameters.

        Returns:
            dict: Extracted data organized by parameters.
        """
        try:
            logger.info("Extracting data from the image text.")
            extracted_info = self.image_text.get('extracted_info', [])

            # Organize extracted information by the configured parameters
            extracted_data = {}
            for param in self.config_manager.parameters:
                values = [
                    str(entry.get(param, "")).strip()  # Convert to string and strip extra spaces
                    for entry in extracted_info if param in entry and str(entry.get(param, "")).strip()
                ]

                # Add only if values exist for the parameter
                if values:
                    extracted_data[param] = values

            if not extracted_data:
                logger.warning("No valid extracted data found. Returning an empty dictionary.")

            logger.debug(f"Final extracted data: {extracted_data}")
            return extracted_data

        except Exception as e:
            logger.error(f"Error during data extraction: {str(e)}")
            raise ValueError(f"Error extracting data from image text: {str(e)}")


    def _generate_keywords(self, extracted_data):
        """
        Generate keywords based on the extracted data using the Groq API.
        
        Args:
            extracted_data (dict): Data extracted from the image text.

        Returns:
            list: List of keywords extracted by the Groq API.
        """
        try:
            logger.info("Generating keywords from extracted data.")
            # Flatten all extracted values into a single list
            extracted_words = [item for sublist in extracted_data.values() for item in sublist]

            # If no words found, log and return an empty list
            if not extracted_words:
                logger.warning("No words found in the extracted data. Returning an empty keyword list.")
                return []

            # Send extracted words to the Groq API for keyword extraction
            chat_completion = self.config_manager.client.chat.completions.create(
                messages=get_keyword_prompt(extracted_words),  # Correct assignment
                model=self.config_manager.model,
            )

            response = chat_completion.choices[0].message.content.strip()
            # Split response by commas to get individual keywords
            keywords = [keyword.strip() for keyword in response.split(",")]
            logger.info(f"Keywords generated: {keywords}")
            return keywords

        except Exception as e:
            logger.error(f"Error during keyword extraction: {e}")
            return []

    def _extract_keywords(self):
        """
        Main method to extract keywords from the image text.
        Ensures configuration is loaded and processes the image text.

        Returns:
            list: List of extracted keywords.
        """
        try:
            logger.info("Starting keyword extraction process.")
            # Ensure configuration is loaded
            self.config_manager.load_config()

            # Extract the necessary data from the image_text
            extracted_data = self._extract_data()

            # If no data extracted, log and return an empty list
            if not extracted_data:
                logger.warning("No data extracted. Returning an empty keyword list.")
                return []

            # Log the extracted data for debugging purposes
            logger.debug(f"Extracted data to process: {extracted_data}")

            # Generate and return the keywords
            return self._generate_keywords(extracted_data)

        except ValueError as ve:
            logger.error(f"ValueError during keyword extraction process: {str(ve)}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error during keyword extraction process: {str(e)}")
            return []
