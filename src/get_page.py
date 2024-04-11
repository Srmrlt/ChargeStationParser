import os

import requests


def get_page(url: str, debug: bool = False) -> str:
    """
    Функция для тестирования и отладки. Снижает количество запросов к сайту для избежания бана.
    Сохраняет результат запроса в файл index.html и дальнейшие запросы получения данных перенаправляются в этот файл.
    :param url:
    :param debug:
    :return:
    """
    if debug:
        if not os.path.exists("../index.html"):
            data = _load_page(url)
            _write_html(data)
        return _read_html()

    return _load_page(url)


def _write_html(response: str):
    with open("index.html", "w", encoding="utf-8") as file:
        file.write(response)


def _read_html() -> str:
    with open("index.html", "r", encoding="utf-8") as file:
        return file.read()


def _load_page(url: str) -> str:

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,"
                  "image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text

    raise requests.HTTPError(f'Failed to fetch page: {url}. '
                             f'Status code: {response.status_code}', response=response)
