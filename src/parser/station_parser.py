import datetime
import re
import logging
from typing import Any, Type, Tuple, Optional, Literal

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class StationDataParser:
    """
    A parser class to extract station data from HTML content using BeautifulSoup.
    """
    def __init__(self, page_html):
        """
        Initializes the parser with HTML content.

        Args:
            page_html (str): The HTML content to parse.
        """
        self.soup = BeautifulSoup(page_html, "lxml")
        self.status_timestamp = datetime.datetime.now()

    def parse_data(self) -> list[dict[str, Any]]:
        """
        Parses the HTML content and extracts data for each station in a structured list of dictionaries.

        Returns:
            list: A list of dictionaries, each containing data about a station.
        """
        stations = self.soup.tbody.find_all("tr")  # Ищем таблицу станций
        station_list = []
        for station_row in stations:
            station = dict()
            station["info"] = dict()
            station["socket"] = dict()
            station["status"] = dict()
            station["info"]["number"], _ = self._parse_number(station_row)
            station["info"]["city"], station["info"]["address"] = self._parse_address(station_row)
            station["socket"]["power"], station["info"]["name"] = self._parse_name(station_row)
            station["status"]["timestamp"] = self.status_timestamp

            for el in self._parse_type_status(station_row):
                station["status"]["status"], station["socket"]["socket"] = el
                station_list.append(station)

        return station_list

    @staticmethod
    def _parse_number(station_row):
        number_ = station_row.find('td', class_="text-center d-none d-md-table-cell col-2").text
        return StringMethods(number_).extract_data(pattern=r'№ (\d+)', data_type=int)

    @staticmethod
    def _parse_address(station_row):
        address_ = station_row.find('td', class_="text-center d-none d-md-table-cell col-4").text
        return StringMethods(address_).extract_data(pattern=r'г\. ([\w\s-]+),')

    @staticmethod
    def _parse_name(station_row):
        name_ = station_row.find('td', class_="text-center col-4").text
        return StringMethods(name_).extract_data(pattern=r', (\d+(\.\d+)?) kWh', data_type=int)

    @staticmethod
    def _parse_type_status(station_row):
        """
        Extracts the status and type from the status column for a station.
        """
        status_socket_elements = station_row.find('td', class_="text-center status col-2").find_all("span")
        return (StringMethods(status_socket.text).cut_words(1) for status_socket in status_socket_elements)

    def print_example_debug(self):
        print(self.soup.tbody.find('tr', {'data-id': 365}))
        print(self.soup.tbody.find('tr', {'data-id': 329}))
        print(self.soup.prettify())
