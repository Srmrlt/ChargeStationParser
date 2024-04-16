import os
from datetime import datetime

from dotenv import load_dotenv

from src import get_page, print_log
from src.parsing import parse_data
from src.save_to_csv import save_to_csv
from src.scheduler import run_scheduler

load_dotenv()


class Job:
    def __init__(self):
        self.file_path = None
        self.change_file_name()
        self.job_function()

    def job_function(self):
        url = os.getenv("URL")
        page = get_page(url)
        if page:
            stations_data = parse_data(page)
            save_to_csv(stations_data, file_path=self.file_path)
            print_log(f"{datetime.now()}: Выполняю задачу...")

    def change_file_name(self):
        date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.file_path = f"data/charge_{date}.csv"
        print_log(f"Новое имя файла: {self.file_path}")


if __name__ == "__main__":
    job = Job()
    run_scheduler(job)
