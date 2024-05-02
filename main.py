import os
from datetime import datetime
import logging

from dotenv import load_dotenv

import src

from src import print_log
from src.save_to_csv import save_to_csv
from src.scheduler import run_scheduler

load_dotenv()
logging.basicConfig(level=logging.INFO)


class Job:
    def __init__(self):
        self.file_path = None
        self.change_file_name()
        self.job_function()

    def job_function(self):
        url = os.getenv("URL")
        page = src.WebPageLoader(url).fetch_page()
        if page:
            stations_data = src.StationDataParser(page).parse_data()
            # save_to_csv(stations_data, file_path=self.file_path)
            print_log(f"{datetime.now()}: Выполняю задачу...")

    def change_file_name(self):
        date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.file_path = f"data/charge_{date}.csv"
        print_log(f"Новое имя файла: {self.file_path}")


if __name__ == "__main__":
    job = Job()
    run_scheduler(job)
