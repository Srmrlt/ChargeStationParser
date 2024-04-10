import os

from get_page import get_page


def get_data(url: str, debug: bool = False) -> str:
    """
    Функция для тестирования и отладки. Снижает количество запросов к сайту для избежания бана.
    Сохраняет результат запроса в файл index.html и дальнейшие запросы получения данных перенаправляются в этот файл.
    :param url:
    :param debug:
    :return:
    """
    if debug:
        if not os.path.exists("index.html"):
            data = get_page(url)
            write_html(data)
        return read_html()

    return get_page(url)


def write_html(response: str):
    with open("index.html", "w", encoding="utf-8") as file:
        file.write(response)


def read_html() -> str:
    with open("index.html", "r", encoding="utf-8") as file:
        return file.read()
