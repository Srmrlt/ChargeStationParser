import os
from datetime import datetime

from dotenv import load_dotenv

from src import get_page, print_log
from src.parsing import parse_data
from src.save_to_csv import save_to_csv
from src.scheduler import run_scheduler

load_dotenv()


def job_function():
    url = os.getenv("URL")
    year_week = datetime.now().strftime('%Y-%W')
    file_path = f"data/charge_{year_week}.csv"  # Имя файла обновляется каждую неделю
    page = get_page(url)
    stations_data = parse_data(page)
    save_to_csv(stations_data, file_path=file_path)
    print_log(f"{datetime.now()}: Выполняю задачу...")


if __name__ == "__main__":
    run_scheduler(job_function)
