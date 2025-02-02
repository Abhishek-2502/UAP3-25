import torch
from app.models import BERTModel
from app.configs.logging_config import setup_logger

# Configure logger
logger = setup_logger()


class TextEmbedder:
    """
    A class to generate text embeddings using a pre-trained BERT model.
    """

    def __init__(self, bert_model: BERTModel):
        """
        Initialize the TextEmbedder with a BERTModel instance.

        Args:
            bert_model (BERTModel): An instance of the BERTModel class.
        """
        self.tokenizer = bert_model.get_tokenizer()
        self.model = bert_model.get_model()

    def _generate_text_embeddings(self, text: str) -> list:
        """
        Generate the embedding for a given text.

        Args:
            text (str): The input text to generate the embedding for.

        Returns:
            list: A list of floats representing the text embedding.
        """
        try:
            logger.info(f"Generating embedding for text: '{text[:50]}'")

            # Tokenize the input text
            logger.debug("Tokenizing text.")
            inputs = self.tokenizer(
                text, return_tensors='pt', truncation=True, padding=True, max_length=512
            )

            # Get embeddings from the model
            logger.debug("Fetching embeddings from the model.")
            with torch.no_grad():
                outputs = self.model(**inputs)

            # Extract the embeddings from the last hidden state using the [CLS] token representation
            text_embedding = outputs.last_hidden_state[0][0].numpy()  # Convert to numpy array

            # Log the shape of the embedding
            logger.debug(f"text embedding generated with shape: {text_embedding.shape}")

            logger.info("Text embedding generated successfully.")
            return text_embedding.tolist()

        except Exception as e:
            logger.error(f"Error while generating text embedding: {str(e)}")
            return []
