from core.config import Settings
from services.spacy_extractor import SpacyExtractor
from handlers.custom_exceptions import CustomJSONError
from handlers.output_generator import generate_output
from core.constants import constants
import spacy
import spacy.cli
import logging
import traceback

logger = logging.getLogger(__name__)
if not logger.handlers:
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(Settings.LOG_FILE_PATH)
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(Settings.LOG_FILE_FORMAT)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

# Please uncomment/comment below line if you wish to stop/start logging
# logger.disabled = True

try:
    nlp = spacy.load(Settings.SPACY_MODEL)
    extractor = SpacyExtractor(nlp)
except OSError:
    # If model is not available, download and install it
    spacy.cli.download(Settings.SPACY_MODEL)

class nlp:
    """NLP tasks"""

    def __init__(self, component_type: str = None) -> None:
        self.settings = Settings()
        self.component_type = component_type

    def load(self, component_type: str):
        try:
            logger.info("loading component_type: " + component_type +  " started...")

            nlp = spacy.load(Settings.SPACY_MODEL)
            
            doc = nlp("Apple is looking at buying U.K. startup for $1 billion")
            for token in doc:
                print(token.text)
            
        except Exception as e:
            error_message = traceback.format_exc()
            logger.error(f"Unexpected error: {error_message}")
            return generate_output(False, error_code=500, message="Unexpected error occurred. Check logs for details.")

    @staticmethod
    def predict(component_type: str, input_text: str):
        try:
            
            if component_type is None:
                raise CustomJSONError(constants.ERROR_CODE_500, constants.VALIDATE_COMPONENT_TYPE_NONE)
            
            if input_text is None:
                raise CustomJSONError(constants.ERROR_CODE_500, constants.VALIDATE_INPUT_TEXT_NONE)
            
            if not isinstance(component_type, str):
                raise CustomJSONError(constants.ERROR_CODE_500, constants.VALIDATE_COMPONENT_TYPE_STRING)
            
            if not isinstance(input_text, str):
                raise CustomJSONError(constants.ERROR_CODE_500, constants.VALIDATE_INPUT_TEXT_STRING)

            if not component_type.strip():
                raise CustomJSONError(constants.ERROR_CODE_500, constants.VALIDATE_COMPONENT_TYPE_EMPTY)   

            if not input_text.strip():
                raise CustomJSONError(constants.ERROR_CODE_500, constants.VALIDATE_INPUT_TEXT_EMPTY)           

            predicted_result = extractor.predict_nlp_component(component_type, input_text)
            
            if predicted_result is not None and bool(predicted_result):
                return predicted_result
            return generate_output(True, data=constants.COMPONENT_TYPE_UNSUPPORTED)
        
        except CustomJSONError as e:
            logger.error(f"Custom JSON Error: {e.to_json()}")
            return e.to_json()

        except Exception as e:
            error_message = traceback.format_exc()
            logger.error(f"Unexpected error: {error_message}")
            return generate_output(False, error_code=500, message=constants.UNEXPECTED_ERROR)

    def train(self):
        try:
            logger.info("data preprocessing started...")
            
        except Exception as ex:
            logger.error(str(ex))

    def PretrainedPipeline(self):
        try:
            logger.info("data preprocessing started...")
            
        except Exception as ex:
            logger.error(str(ex))

