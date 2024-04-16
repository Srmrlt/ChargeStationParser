import os

import requests

from src.utils import print_log


def get_page(url: str) -> str:
    """
    Функция для тестирования и отладки. Снижает количество запросов к сайту для избежания бана.
    Сохраняет результат запроса в файл index.html и дальнейшие запросы получения данных перенаправляются в этот файл.
    :param url:
    :return:
    """
    debug = os.getenv("DEBUG", False)
    file_path = "index.html"
    if debug:
        print_log("Режим DEBUG активен!!!")
        if not os.path.exists(file_path):
            data = _load_page(url)
            _write_html(data, file_path)
        return _read_html(file_path)

    return _load_page(url)


def _write_html(response: str, file_path: str):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(response)


def _read_html(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def _load_page(url: str) -> str:

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,"
                  "image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Генерируем исключение для некорректных HTTP кодов
        return response.text
    except Exception as e:
        print_log(f"An error in connection: {e}")
    return ""
