from io import BytesIO
from PIL import Image
import pytesseract
from fastapi import UploadFile
import cv2
from input_layer.image_processor import ImageProcessor
from app.configs.logging_config import setup_logger

# Configure logger
logger = setup_logger()

class ImageTextExtractor:
    """
    A class to handle the text extraction process from an image using OCR.
    """

    def __init__(self, file: UploadFile):
        """
        Initialize the ImageTextExtractor class with an uploaded file.

        Args:
            file (UploadFile): The uploaded image file.
        """
        self.file = file

    def extract_text_from_image(self):
        """
        Extract text from the uploaded image by preprocessing, binarizing,
        and applying OCR.

        Returns:
            dict: A dictionary containing extracted text information and other metadata.
        """
        try:
            logger.info("Starting text extraction process.")

            # Read the uploaded image file
            try:
                logger.debug("Reading the image file into memory.")
                image = Image.open(BytesIO(self.file.file.read()))
                logger.debug("Image successfully loaded.")
            except Exception as e:
                logger.error(f"Error opening image: {str(e)}")
                raise ValueError(f"Failed to open image: {str(e)}")

            # Initialize the ImageProcessor class
            image_processor = ImageProcessor()

            # Preprocess the image
            try:
                logger.debug("Preprocessing the image.")
                preprocessed_image = image_processor.preprocess_image(image)
                logger.debug("Image preprocessing completed.")
            except Exception as e:
                logger.error(f"Error during image preprocessing: {str(e)}")
                raise ValueError(f"Error during preprocessing: {str(e)}")

            # Convert the image to OpenCV format
            try:
                logger.debug("Converting preprocessed image to OpenCV format.")
                open_cv_image = image_processor.convert_image_to_cv_format(preprocessed_image)
                logger.debug("Conversion to OpenCV format successful.")
            except Exception as e:
                logger.error(f"Error converting image to OpenCV format: {str(e)}")
                raise ValueError(f"Error converting to OpenCV format: {str(e)}")

            # Apply binarization for better OCR results
            try:
                logger.debug("Applying adaptive thresholding for binarization.")
                gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
                binarized_image = cv2.adaptiveThreshold(
                    gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
                )
                logger.debug("Binarization completed.")
            except Exception as e:
                logger.error(f"Error during binarization: {str(e)}")
                raise ValueError(f"Error during binarization: {str(e)}")

            # Use pytesseract to get detailed OCR data
            try:
                logger.debug("Performing OCR on the processed image.")
                custom_config = "--oem 3 --psm 6"  # Optimal configuration for mixed text
                ocr_data = pytesseract.image_to_data(
                    binarized_image, config=custom_config, output_type=pytesseract.Output.DICT
                )
                logger.debug("OCR performed successfully.")
            except pytesseract.TesseractError as tesseract_error:
                logger.error(f"Tesseract error during OCR: {str(tesseract_error)}")
                raise ValueError(f"Tesseract OCR failed: {str(tesseract_error)}")
            except Exception as e:
                logger.error(f"Unexpected error during OCR: {str(e)}")
                raise ValueError(f"Error during OCR: {str(e)}")

            # Prepare the JSON response structure
            extracted_info = []
            try:
                logger.debug("Processing OCR data into structured response.")
                for i in range(len(ocr_data["text"])):
                    if int(ocr_data["conf"][i]) > 0:  # Only include words with confidence greater than 0
                        extracted_info.append({
                            "word": ocr_data["text"][i],
                            "x": ocr_data["left"][i],
                            "y": ocr_data["top"][i],
                            "width": ocr_data["width"][i],
                            "height": ocr_data["height"][i],
                            "level": ocr_data["level"][i],
                            "block_num": ocr_data["block_num"][i],
                            "par_num": ocr_data["par_num"][i],
                            "line_num": ocr_data["line_num"][i],
                            "word_num": ocr_data["word_num"][i],
                            "confidence": ocr_data["conf"][i],
                            "fontname": "N/A",  # Placeholder, as Tesseract does not provide fontname directly
                            "fontsize": "N/A",  # Placeholder, Tesseract does not provide fontsize directly
                            "orientation": "N/A",  # Placeholder
                            "script": "N/A"  # Placeholder
                        })
                logger.debug("OCR data processed into structured response.")
            except Exception as e:
                logger.error(f"Error processing OCR data: {str(e)}")
                raise ValueError(f"Error processing OCR data: {str(e)}")

            logger.info("Text extraction completed successfully.")
            return {"extracted_info": extracted_info}

        except ValueError as ve:
            logger.error(f"ValueError during text extraction: {str(ve)}")
            return {"error": f"ValueError: {str(ve)}"}

        except Exception as e:
            logger.error(f"Unexpected error during text extraction: {str(e)}")
            return {"error": f"Unexpected error: {str(e)}"}
