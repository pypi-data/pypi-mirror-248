import logging
import traceback

from core.config import Settings
from handlers.custom_exceptions import CustomJSONError
from handlers.output_generator import generate_output
from core.constants import constants, preprocess_operations

from musaddiquehussainlabs.text_preprocessing.operations import operations_dict

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

def preprocess_text(text: str, operations=None) -> str:
    """ Preprocess an input text by executing a series of preprocessing functions specified in functions list """

    try:

        if text is None:
                raise CustomJSONError(constants.ERROR_CODE_500, constants.VALIDATE_INPUT_TEXT_NONE)
        
        if not isinstance(text, str):
                raise CustomJSONError(constants.ERROR_CODE_500, constants.VALIDATE_INPUT_TEXT_STRING)

        if not text.strip():
                raise CustomJSONError(constants.ERROR_CODE_500, constants.VALIDATE_INPUT_TEXT_EMPTY)
        
        default_operations = [
            preprocess_operations.to_lower,
            preprocess_operations.remove_html,
            preprocess_operations.remove_url,
            preprocess_operations.remove_email,
            preprocess_operations.remove_phone_number,
            preprocess_operations.remove_itemized_bullet_and_numbering,
            preprocess_operations.remove_punctuation,
            preprocess_operations.remove_special_character,
            preprocess_operations.remove_whitespace,
            preprocess_operations.normalize_unicode,
            preprocess_operations.expand_contraction,
            preprocess_operations.convert_emoticons_to_words,
            preprocess_operations.convert_emojis_to_words,
            preprocess_operations.chat_words_conversion,
            preprocess_operations.remove_stopword,
            preprocess_operations.remove_freqwords,
            preprocess_operations.remove_rarewords
        ]

        # If operations are not supplied, use default operations
        if operations is None:
            operations = default_operations

        # Validate text input
        if not isinstance(text, str):
            raise CustomJSONError(constants.ERROR_CODE_500, constants.VALIDATE_INPUT_TEXT_STRING)

        if operations is None or not isinstance(operations, list) or not operations:
            raise CustomJSONError(constants.ERROR_CODE_500, constants.TEXTPREPROCESSING_OPERATIONS_EMPTY_NONE)

        for operation_name in operations:
            if operation_name not in operations_dict:
                raise CustomJSONError(constants.ERROR_CODE_500, constants.TEXTPREPROCESSING_INVALID_OPERATIONS.format(operation_name))

        processed_text = text
        for operation_name in operations:
            operation_func = operations_dict.get(operation_name)
            if operation_func:
                processed_text = operation_func(processed_text)

                # Ensure the processed_text is a string after each operation
                if not isinstance(processed_text, str):
                    processed_text = ' '.join(processed_text)

            else:
                raise ValueError(constants.TEXTPREPROCESSING_OPERATIONS_NOT_CALLABLE.format(operation_name))

        return generate_output(True, data=processed_text)
    
    except CustomJSONError as e:
        logger.error(f"Custom JSON Error: {e.to_json()}")
        return e.to_json()

    except Exception as e:
        error_message = traceback.format_exc()
        logger.error(f"Unexpected error: {error_message}")
        return generate_output(False, error_code=500, message=constants.UNEXPECTED_ERROR)
