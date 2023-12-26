import datetime
import json
import typing
import logging
import traceback

import nltk
from nltk.tokenize import BlanklineTokenizer
import spacy

from core.config import Settings
from services.spacy_extractor import SpacyExtractor
from services.langchain_framework import LangchainFramework
from handlers.custom_exceptions import CustomJSONError
from handlers.output_generator import generate_output
from core.constants import constants

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
except OSError:
    # If model is not available, download and install it
    spacy.cli.download(Settings.SPACY_MODEL)

extractor = SpacyExtractor(nlp)
langchain = LangchainFramework()

class DocumentAnalysis:
    """Document Analysis class."""

    # pylint: disable=too-many-arguments
    def __init__(self) -> None:
        """Initialisation.
        Args:
            
        """

    def full_analysis(self, 
                      input_text: str
                      ) -> None:
        """analyze documents and return a dictionary containing the various parts of\
        the documents broken down into key-value pairs.
        Returns:
          dict: A dictionary with the content of the documents and broken down into
                key-value pairs.
        """
        try:

            if input_text is None:
                raise CustomJSONError(constants.ERROR_CODE_500, constants.VALIDATE_INPUT_TEXT_NONE)
        
            if not isinstance(input_text, str):
                raise CustomJSONError(constants.ERROR_CODE_500, constants.VALIDATE_INPUT_TEXT_STRING)

            if not input_text.strip():
                raise CustomJSONError(constants.ERROR_CODE_500, constants.VALIDATE_INPUT_TEXT_EMPTY)
            
            self.input_text = input_text

            input_text = "\n".join(input_text.splitlines())
            
            report_struc: typing.Dict[str, typing.Any] = {}  # Final structure

            report_struc['language'] = langchain.language_detection(input_text)
            report_struc['linguistic_analysis'] = extractor.deep_linguistic_analysis(input_text)
            report_struc['keyphrases'] = langchain.keyphrase_extraction(input_text)
            report_struc['ner'] = extractor.entity_recognition(input_text)
            report_struc['sentiment'] = langchain.sentiment_analysis(input_text)
            report_struc['pii'] = langchain.pii_anonymization(input_text)

            return generate_output(True, data=report_struc)
        
        except CustomJSONError as e:
            logger.error(f"Custom JSON Error: {e.to_json()}")
            return e.to_json()

        except Exception as e:
            error_message = traceback.format_exc()
            logger.error(f"Unexpected error: {error_message}")
            return generate_output(False, error_code=500, message=constants.UNEXPECTED_ERROR)

    def language_detection(self, input_text: str) -> typing.Dict[str, typing.Any]:
        try:

            if input_text is None:
                raise CustomJSONError(constants.ERROR_CODE_500, constants.VALIDATE_INPUT_TEXT_NONE)
        
            if not isinstance(input_text, str):
                raise CustomJSONError(constants.ERROR_CODE_500, constants.VALIDATE_INPUT_TEXT_STRING)

            if not input_text.strip():
                raise CustomJSONError(constants.ERROR_CODE_500, constants.VALIDATE_INPUT_TEXT_EMPTY)
            
            input_text = "\n".join(input_text.splitlines())
            
            report_struc: typing.Dict[str, typing.Any] = {}  # Final structure
            report_struc['language'] = langchain.language_detection(input_text)

            return generate_output(True, data=report_struc)
        
        except CustomJSONError as e:
            logger.error(f"Custom JSON Error: {e.to_json()}")
            return e.to_json()

        except Exception as e:
            error_message = traceback.format_exc()
            logger.error(f"Unexpected error: {error_message}")
            return generate_output(False, error_code=500, message=constants.UNEXPECTED_ERROR)

    def deep_linguistic_analysis(self, input_text: str) -> typing.Dict[str, typing.Any]:
        try:
            if input_text is None:
                raise CustomJSONError(constants.ERROR_CODE_500, constants.VALIDATE_INPUT_TEXT_NONE)
        
            if not isinstance(input_text, str):
                raise CustomJSONError(constants.ERROR_CODE_500, constants.VALIDATE_INPUT_TEXT_STRING)

            if not input_text.strip():
                raise CustomJSONError(constants.ERROR_CODE_500, constants.VALIDATE_INPUT_TEXT_EMPTY)
            
            input_text = "\n".join(input_text.splitlines())
            
            report_struc: typing.Dict[str, typing.Any] = {}  # Final structure
            report_struc['disambiguaton'] = extractor.deep_linguistic_analysis(input_text)

            return generate_output(True, data=report_struc)
        
        except CustomJSONError as e:
            logger.error(f"Custom JSON Error: {e.to_json()}")
            return e.to_json()

        except Exception as e:
            error_message = traceback.format_exc()
            logger.error(f"Unexpected error: {error_message}")
            return generate_output(False, error_code=500, message=constants.UNEXPECTED_ERROR)
    
    def keyphrase_extraction(self, input_text: str) -> typing.Dict[str, typing.Any]:
        try:
            if input_text is None:
                raise CustomJSONError(constants.ERROR_CODE_500, constants.VALIDATE_INPUT_TEXT_NONE)
        
            if not isinstance(input_text, str):
                raise CustomJSONError(constants.ERROR_CODE_500, constants.VALIDATE_INPUT_TEXT_STRING)

            if not input_text.strip():
                raise CustomJSONError(constants.ERROR_CODE_500, constants.VALIDATE_INPUT_TEXT_EMPTY)
            
            input_text = "\n".join(input_text.splitlines())
            
            report_struc: typing.Dict[str, typing.Any] = {}  # Final structure
            report_struc['relevants'] = langchain.keyphrase_extraction(input_text)

            return generate_output(True, data=report_struc)
        
        except CustomJSONError as e:
            logger.error(f"Custom JSON Error: {e.to_json()}")
            return e.to_json()

        except Exception as e:
            error_message = traceback.format_exc()
            logger.error(f"Unexpected error: {error_message}")
            return generate_output(False, error_code=500, message=constants.UNEXPECTED_ERROR)
    
    def entity_recognition(self, input_text: str) -> typing.Dict[str, typing.Any]:
        try:
            if input_text is None:
                raise CustomJSONError(constants.ERROR_CODE_500, constants.VALIDATE_INPUT_TEXT_NONE)
        
            if not isinstance(input_text, str):
                raise CustomJSONError(constants.ERROR_CODE_500, constants.VALIDATE_INPUT_TEXT_STRING)

            if not input_text.strip():
                raise CustomJSONError(constants.ERROR_CODE_500, constants.VALIDATE_INPUT_TEXT_EMPTY)
            
            input_text = "\n".join(input_text.splitlines())
            
            report_struc: typing.Dict[str, typing.Any] = {}  # Final structure
            report_struc['ner'] = extractor.entity_recognition(input_text)

            return generate_output(True, data=report_struc)
        
        except CustomJSONError as e:
            logger.error(f"Custom JSON Error: {e.to_json()}")
            return e.to_json()

        except Exception as e:
            error_message = traceback.format_exc()
            logger.error(f"Unexpected error: {error_message}")
            return generate_output(False, error_code=500, message=constants.UNEXPECTED_ERROR)
    
    def sentiment_analysis(self, input_text: str) -> typing.Dict[str, typing.Any]:
        try:
            if input_text is None:
                raise CustomJSONError(constants.ERROR_CODE_500, constants.VALIDATE_INPUT_TEXT_NONE)
        
            if not isinstance(input_text, str):
                raise CustomJSONError(constants.ERROR_CODE_500, constants.VALIDATE_INPUT_TEXT_STRING)

            if not input_text.strip():
                raise CustomJSONError(constants.ERROR_CODE_500, constants.VALIDATE_INPUT_TEXT_EMPTY)
            
            input_text = "\n".join(input_text.splitlines())
            
            report_struc: typing.Dict[str, typing.Any] = {}  # Final structure
            report_struc['sentiment'] = langchain.sentiment_analysis(input_text)

            return generate_output(True, data=report_struc)
        
        except CustomJSONError as e:
            logger.error(f"Custom JSON Error: {e.to_json()}")
            return e.to_json()

        except Exception as e:
            error_message = traceback.format_exc()
            logger.error(f"Unexpected error: {error_message}")
            return generate_output(False, error_code=500, message=constants.UNEXPECTED_ERROR)
    
    def pii_anonymization(self, input_text: str) -> typing.Dict[str, typing.Any]:
        try:
            if input_text is None:
                raise CustomJSONError(constants.ERROR_CODE_500, constants.VALIDATE_INPUT_TEXT_NONE)
        
            if not isinstance(input_text, str):
                raise CustomJSONError(constants.ERROR_CODE_500, constants.VALIDATE_INPUT_TEXT_STRING)

            if not input_text.strip():
                raise CustomJSONError(constants.ERROR_CODE_500, constants.VALIDATE_INPUT_TEXT_EMPTY)
            
            input_text = "\n".join(input_text.splitlines())
            
            report_struc: typing.Dict[str, typing.Any] = {}  # Final structure
            report_struc['pii'] = langchain.pii_anonymization(input_text)

            return generate_output(True, data=report_struc)
        
        except CustomJSONError as e:
            logger.error(f"Custom JSON Error: {e.to_json()}")
            return e.to_json()

        except Exception as e:
            error_message = traceback.format_exc()
            logger.error(f"Unexpected error: {error_message}")
            return generate_output(False, error_code=500, message=constants.UNEXPECTED_ERROR)

