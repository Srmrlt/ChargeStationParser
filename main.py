import os

from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler

from parsing import parse_data, parse_status
from save_to_csv import add_data_to_file, save_new_file
from utils import get_data

load_dotenv()
url = os.getenv("URL")

page = get_data(url)
stations_data = parse_data(page)
save_new_file(stations_data)


def job_function():
    stations_status = parse_status(page)
    add_data_to_file(stations_status)
    print("Выполняю задачу...")


scheduler = BlockingScheduler()
scheduler.add_job(job_function, 'interval', minutes=1)
scheduler.start()
