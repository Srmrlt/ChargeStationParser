import datetime
from typing import Any

from bs4 import BeautifulSoup


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
        self.status_time = datetime.datetime.now()

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
            self._parse_number(station, station_row)
            self._parse_address(station, station_row)
            self._parse_name(station, station_row)
            self._parse_type_status(station, station_row)
            station_list.append(station)

        return station_list

    def _parse_number(self, station, station_row):
        station_row = station_row.find('td', class_="text-center d-none d-md-table-cell col-2")
        station["number"] = self._clean_text(station_row)

    def _parse_address(self, station, station_row):
        station_row = station_row.find('td', class_="text-center d-none d-md-table-cell col-4")
        station["address"] = self._clean_text(station_row)

    def _parse_name(self, station, station_row):
        station_row = station_row.find('td', class_="text-center col-4")
        station["name"] = self._clean_text(station_row)

    def _parse_type_status(self, station, station_row):
        """
        Extracts the status and type from the status column for a station.

        Args:
            station (dict): The dictionary representing the station where status and type are added.
            station_row (bs4.element.Tag): The BeautifulSoup tag of the station row being parsed.
        """
        type_status_elements = station_row.find('td', class_="text-center status col-2").find_all("span")
        station["status"] = []
        station["type"] = []
        for type_status in type_status_elements:
            type_status_text = self._clean_text(type_status)
            station["status"].append(' '.join(type_status_text.split()[1:]))  # Первое слово - статус
            station["type"].append(type_status_text.split()[0])  # Остальное - тип станции

    def _get_data(self, parent, tag, attrs=dict()):
        """
        Safely extracts text from a specified tag within a parent element.

        Args:
            parent (bs4.element.Tag): The parent BeautifulSoup tag from which to find and extract text.
            tag (str): The tag type to look for.
            attrs (dict): Attributes to match in the search for the tag.

        Returns:
            str: The cleaned text from the found element, or None if no element is found.
        """
        element = parent.find(tag, attrs)
        return self._clean_text(element) if element else None

    @staticmethod
    def _clean_text(element) -> str:
        """
        Cleans the text extracted from an HTML element.

        Args:
            element (bs4.element.Tag): The BeautifulSoup tag from which text is extracted.

        Returns:
            str: The cleaned text.
        """
        # Удаляем лишние пробелы и спец символы (перенос строки)
        print(type(element))
        return element.text.strip().replace("\n", "").replace("\r", "")

    def print_example_debug(self):
        print(self.soup.tbody.find('tr', {'data-id': 365}))
        print(self.soup.tbody.find('tr', {'data-id': 329}))
        print(self.soup.prettify())
