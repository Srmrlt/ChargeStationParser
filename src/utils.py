import sys


def print_log(message: str):
    print(message)
    sys.stdout.flush()  # Для вывода в логи docker
