import os
import sys
from datetime import datetime

from dotenv import load_dotenv

from src import get_page
from src.parsing import parse_data, parse_status
from src.save_to_csv import add_data_to_file, save_new_file
from src.scheduler import run_scheduler

load_dotenv()
url = os.getenv("URL")

page = get_page(url)
stations_data = parse_data(page)
save_new_file(stations_data)


def job_function():
    stations_status = parse_status(get_page(url))
    add_data_to_file(stations_status)
    print(f"{datetime.now()}: Выполняю задачу...")
    sys.stdout.flush()


if __name__ == "__main__":
    run_scheduler(job_function)
