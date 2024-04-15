from bs4 import BeautifulSoup


def parse_data(page_html):
    soup = BeautifulSoup(page_html, 'lxml')

    # print(soup.tbody.find('tr', {'data-id': 365}))
    # print(soup.tbody.find('tr', {'data-id': 329}))
    # print(soup.prettify())

    stations = soup.tbody.find_all('tr')  # Ищем таблицу станций

    stations_data = {
        "station_number": [],
        "station_address": [],
        "station_name": [],
        "station_type": [],
        "station_status": [],
    }

    for id1, station in enumerate(stations, start=1):
        station_types = station.find('td', class_="text-center status col-2").find_all("span")
        for id2, station_type in enumerate(station_types, start=1):
            data: dict = {
                "station_number": station.find('td', class_="text-center d-none d-md-table-cell col-2"),
                "station_address": station.find('td', class_="text-center d-none d-md-table-cell col-4"),
                "station_name": station.find('td', class_="text-center col-4"),
                "station_type": station_type,  # На данном этапе тип станции + статус
                "station_status": station_type,  # На данном этапе тип станции + статус
            }

            # Удаляем лишние пробелы и спец символы (перенос строки)
            data = {key: data[key].text.strip().replace("\n", "").replace("\r", "")
                    for key in data.keys()}

            # Получаем статус (первое слово)
            data["station_status"] = data["station_status"].split()[0]
            # Получаем тип станции, убирая статус
            data["station_type"] = ' '.join(data["station_type"].split()[1:])

            # Добавляем данные по станции в общий словарь станций
            for key in data.keys():
                stations_data[key].append(data[key])

    return stations_data
