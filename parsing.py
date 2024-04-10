from datetime import datetime

from bs4 import BeautifulSoup


def parse_data(page_html):
    soup = BeautifulSoup(page_html, 'lxml')

    # print(soup.tbody.find('tr', {'data-id': 365}))
    # print(soup.tbody.find('tr', {'data-id': 329}))
    # print(soup.prettify())

    stations = soup.tbody.find_all('tr')  # Ищем таблицу станций

    stations_data = {
        "station_id": [],
        "station_number": [],
        "station_address": [],
        "station_name": [],
        "station_type": [],
    }

    for id1, station in enumerate(stations, start=1):
        station_types = station.find('td', class_="text-center status col-2").find_all("span")
        for id2, station_type in enumerate(station_types, start=1):
            data: dict = {
                "station_number": station.find('td', class_="text-center d-none d-md-table-cell col-2"),
                "station_address": station.find('td', class_="text-center d-none d-md-table-cell col-4"),
                "station_name": station.find('td', class_="text-center col-4"),
                "station_type": station_type,
            }

            # Удаляем лишние пробелы и спец символы (перенос строки)
            data = {key: data[key].text.strip().replace("\n", "").replace("\r", "")
                    for key in data.keys()}

            # Убираем статус из строки (первое слово). Остаётся тип станции
            data["station_type"] = ' '.join(data["station_type"].split()[1:])

            # Добавляем id записи вида: '1.1'
            data["station_id"] = f"{id1}.{id2}"

            # Добавляем данные по станции в общий словарь станций
            for key in data.keys():
                stations_data[key].append(data[key])

    return stations_data


def parse_status(page_html):
    soup = BeautifulSoup(page_html, 'lxml')

    stations = soup.tbody.find_all('tr')  # Ищем таблицу станций

    # Создаем объект даты и времени
    current_datetime = datetime.now().replace(microsecond=0)
    stations_data = {
        current_datetime: [],
    }

    for id1, station in enumerate(stations, start=1):
        station_types = station.find('td', class_="text-center status col-2").find_all("span")
        for id2, station_type in enumerate(station_types, start=1):
            data: dict = {
                current_datetime: station_type,
            }

            # Удаляем лишние пробелы и спец символы (перенос строки)
            data = {key: data[key].text.strip().replace("\n", "").replace("\r", "")
                    for key in data.keys()}

            # Убираем статус из строки (первое слово). Остаётся тип станции
            data[current_datetime] = data[current_datetime].split()[0]

            # Добавляем данные по станции в общий словарь станций
            for key in data.keys():
                stations_data[key].append(data[key])

    return stations_data
