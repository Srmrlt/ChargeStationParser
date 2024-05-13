import copy
import datetime
import logging
from typing import Any, Tuple

import bs4

from .text_processing import TextDataExtractor

logger = logging.getLogger(__name__)


class StationDataParser:
    """
    A class to parse and extract data about charging stations from HTML content using BeautifulSoup.

    Attributes:
        soup (bs4.BeautifulSoup): BeautifulSoup object to parse HTML.
        status_timestamp (datetime.datetime): Timestamp when the status of the stations was last updated.
    """

    def __init__(self, page_html: str):
        """
        Initializes the StationDataParser with HTML content.

        Args:
            page_html (str): The HTML content to parse.

        Raises:
            Exception: If an error occurs while initializing the BeautifulSoup object.
        """
        try:
            self.soup = bs4.BeautifulSoup(page_html, "lxml")
        except Exception as e:
            logger.error(f"Error initializing BeautifulSoup: {e}")
            raise
        self.status_timestamp = datetime.datetime.now()

    def parse_data(self) -> list[dict[str, dict[str, Any]]]:
        """
        Parses the HTML content and extracts structured data for each charging station.

        Returns:
            list[dict[str, dict[str, Any]]]: A list of dictionaries where each dictionary represents
                                             a charging station and contains detailed information organized
                                             into 'info', 'socket', and 'status' categories.
        """
        stations = self.soup.tbody.find_all("tr")
        return [station for station_row in stations for station in self._parse_station_row(station_row)]

    def _parse_station_row(self, station_row: bs4.element.Tag):
        """
        Parses a single row of station data and generates a dictionary for each station with its details.

        Args:
            station_row (bs4.element.Tag): The HTML tag containing data for a single station.

        Yields:
            dict[str, dict[str, Any]]: A dictionary with detailed station data categorized into 'info',
                                        'socket', and 'status'.
        """
        station_ = {"info": {}, "socket": {}, "status": {}}
        station_["info"]["number"], _ = self._extract_station_id(station_row)
        station_["info"]["city"], station_["info"]["address"] = self._extract_location_details(station_row)
        station_["socket"]["power"], station_["info"]["name"] = self._extract_power_and_name(station_row)
        station_["status"]["timestamp"] = self.status_timestamp

        for el in self._extract_status_and_socket_types(station_row):
            station = copy.deepcopy(station_)
            station["status"]["status"], station["socket"]["socket"], station["socket"]["charger_port"] = el
            yield station

    @staticmethod
    def _extract_station_id(station_row: bs4.element.Tag) -> Tuple[int, str]:
        """
        Extracts the station number from the given HTML row.

        Args:
            station_row (bs4.element.Tag): The HTML tag containing the station number.

        Returns:
            Tuple[int, str]: A tuple containing the extracted station number and empty string.
        """
        number_: str = station_row.find("td", class_="text-center d-none d-md-table-cell col-2").text
        return TextDataExtractor(number_).extract_data(pattern=r"№ (\d+)", data_type=int)

    @staticmethod
    def _extract_location_details(station_row: bs4.element.Tag) -> Tuple[str, str]:
        """
        Extracts the city and address of the station from the given HTML row.

        Args:
            station_row (bs4.element.Tag): The HTML tag containing the address data.

        Returns:
            Tuple[str, str]: A tuple containing the city and address of the station.
        """
        address_: str = station_row.find("td", class_="text-center d-none d-md-table-cell col-4").text
        return TextDataExtractor(address_).extract_data(pattern=r"г\. ([\w\s-]+),")

    @staticmethod
    def _extract_power_and_name(station_row: bs4.element.Tag) -> Tuple[float, str]:
        """
        Extracts the name and power specification of the station from the given HTML row.

        Args:
            station_row (bs4.element.Tag): The HTML tag containing the name and power data.

        Returns:
            Tuple[float, str]: A tuple containing the power of the station in kWh and the name.
        """
        name_: str = station_row.find("td", class_="text-center col-4").text
        return TextDataExtractor(name_).extract_data(pattern=r", (\d+(\.\d+)?) kWh", data_type=float)

    @staticmethod
    def _extract_status_and_socket_types(station_row: bs4.element.Tag):
        """
        Extracts the status and type of sockets available at the station from the given HTML row.

        Args:
            station_row (bs4.element.Tag): The HTML tag containing the status data.

        Yields:
            Tuple[str, str]: Each tuple contains the status and the type of socket.
        """
        status_socket_elements = station_row.find("td", class_="text-center status col-2").find_all("span")
        for num, status_socket in enumerate(status_socket_elements, 1):
            status, socket = TextDataExtractor(status_socket.text).split_at_word(word_index=0)
            yield status, socket, num

    def print_html_structure(self):
        """
        Prints the prettified HTML content managed by BeautifulSoup. Useful for debugging.
        """
        print(self.soup.prettify())
