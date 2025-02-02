import numpy as np
from PIL import Image, ImageEnhance
import cv2
from app.configs.logging_config import setup_logger

# Configure logger
logger = setup_logger()

class ImageProcessor:
    """
    A class to handle image preprocessing and conversion between PIL and OpenCV formats.
    """

    def __init__(self):
        """
        Initializes the ImageProcessor class.
        """
        logger.info("ImageProcessor initialized.")

    def preprocess_image(self, image: Image) -> Image:
        """
        Preprocesses the image by converting it to grayscale, enhancing contrast, and removing noise.

        Args:
            image (Image): The uploaded PIL Image object.

        Returns:
            Image: The preprocessed PIL Image object.
        """
        try:
            logger.info("Starting image preprocessing.")


            # Check if image is valid
            if not image:
                logger.error("No image provided to preprocess.")
                raise ValueError("The image provided is None or invalid.")

            # Convert the image to grayscale
            logger.debug("Converting image to grayscale.")
            gray_image = image.convert("L")

            # Enhance the contrast of the image
            logger.debug("Enhancing the contrast of the image.")
            enhancer = ImageEnhance.Contrast(gray_image)
            enhanced_image = enhancer.enhance(2.0)  # Contrast factor (adjust as needed)

            # Convert to OpenCV format and apply noise removal
            open_cv_image = np.array(enhanced_image)
            logger.debug("Removing noise with GaussianBlur.")
            denoised_image = cv2.GaussianBlur(open_cv_image, (5, 5), 0)

            # Convert back to PIL for compatibility
            processed_image = Image.fromarray(denoised_image)

            logger.info("Image preprocessing completed successfully.")
            return processed_image

        except ValueError as ve:
            logger.error(f"ValueError during image preprocessing: {str(ve)}")
            return None

        except Exception as e:
            logger.error(f"Unexpected error during image preprocessing: {str(e)}")
            return None

    def convert_image_to_cv_format(self, image: Image) -> np.ndarray:
        """
        Converts the PIL image to a format compatible with OpenCV (numpy array).

        Args:
            image (Image): The preprocessed PIL Image object.

        Returns:
            np.ndarray: The converted OpenCV image in BGR format.
        """
        try:
            logger.info("Converting image to OpenCV format.")

            # Check if image is valid
            if not image:
                logger.error("No image provided for conversion.")
                raise ValueError("The image provided is None or invalid.")

            # Convert PIL image to NumPy array (OpenCV works with numpy arrays)
            open_cv_image = np.array(image)

            # If the image is grayscale, expand dimensions
            if len(open_cv_image.shape) == 2:  # Grayscale image
                open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_GRAY2BGR)

            logger.info("Image converted to OpenCV format successfully.")
            return open_cv_image

        except ValueError as ve:
            logger.error(f"ValueError during image conversion: {str(ve)}")
            return None

        except cv2.error as cv_error:
            logger.error(f"OpenCV error during image conversion: {str(cv_error)}")
            return None

        except Exception as e:
            logger.error(f"Unexpected error during image conversion: {str(e)}")
            return None
