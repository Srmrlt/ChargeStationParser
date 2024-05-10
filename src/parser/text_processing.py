import logging
import re
from typing import Any, Tuple, Type

logger = logging.getLogger(__name__)


class TextDataExtractor:
    def __init__(self, data: str):
        self.data: str = data
        self.clean_text()

    def clean_text(self):
        """
        Cleans the text by stripping leading and trailing white spaces and removing all occurrences
        of newline and carriage return characters from the data.
        """
        self.data = self.data.strip().replace("\n", "").replace("\r", "")

    def extract_data(self, pattern: str, data_type: Type[Any] | None = None) -> Tuple[Any, str]:
        """
        Extracts data using a regular expression pattern and optionally converts the extracted data
        to the specified type.

        :param pattern: The regex pattern to extract data.
        :param data_type: The type to which the extracted data should be converted, e.g., int or float.
        :return: A tuple containing the converted extracted data and the modified string after data removal.
        """
        match = re.search(pattern, self.data)
        if match:
            extracted_data = match.group(1).strip()
            if data_type:
                extracted_data = self.safe_convert(data_type, data=extracted_data)
            return extracted_data, self.remove_data(pattern=pattern)
        logger.warning("No data to extract")
        return None, self.data

    def remove_data(self, pattern: str) -> str:
        """
        Removes data from the string based on the provided regex pattern.

        :param pattern: The regex pattern to remove data.
        :return: The string after the data has been removed.
        """
        self.data = re.sub(pattern, "", self.data).strip()
        return self.data

    def split_at_word(self, word_index: int) -> Tuple[str | None, str]:
        """
        Splits the string into two parts at the specified word index. The first part includes the text
         up to and including the word at the specified index, and the second part contains the text after that word.

        :param word_index: The 1-based index of the word at which to split the text.
        :return: A tuple containing:
                 - The text up to and including the specified word. None if the index exceeds the number of words.
                 - The remaining text after the specified word.
        """
        words = self.data.split()
        if len(words) < word_index + 1:
            return None, self.data
        text_before = " ".join(words[:word_index + 1])
        text_after = " ".join(words[word_index + 1:])

        return text_before, text_after

    def safe_convert(self, data_type: Type[Any], data: str | None = None) -> Any | None:
        """
        Safely converts a string to a specified type, catching and logging conversion errors.

        :param data_type: The type to which the data should be converted.
        :param data: The string data to convert. If None, converts the entire string of the object.
        :return: The converted data or None if conversion fails.
        """
        if data is None:
            data = self.data

        try:
            return data_type(data)
        except (ValueError, TypeError) as e:
            logger.error(f"Error during conversion: {e}")
            return None
