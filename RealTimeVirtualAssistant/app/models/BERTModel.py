from transformers import BertTokenizer, BertModel
from app.configs.logging_config import setup_logger

# Configure logger
logger = setup_logger()


class BERTModel:
    """
    A class to manage the pre-trained BERT model and tokenizer.
    """

    def __init__(self, model_name: str = 'bert-base-uncased'):
        """
        Initialize the BERT model and tokenizer.

        Args:
            model_name (str): The name of the pre-trained BERT model.
        """
        try:
            logger.info(f"Loading pre-trained BERT model: {model_name}")
            self.tokenizer = BertTokenizer.from_pretrained(model_name)
            self.model = BertModel.from_pretrained(model_name)
            logger.info("BERT model and tokenizer loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize BERT model: {str(e)}")
            raise e

    def get_tokenizer(self):
        """
        Get the tokenizer instance.
        """
        logger.info("Retrieving BERT tokenizer instance.")
        return self.tokenizer

    def get_model(self):
        """
        Get the model instance.
        """
        logger.info("Retrieving BERT model instance.")
        return self.model
