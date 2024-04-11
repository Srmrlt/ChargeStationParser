import os
from datetime import datetime
import time

from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv

from src.parsing import parse_data, parse_status
from src.save_to_csv import add_data_to_file, save_new_file
from src import get_page

load_dotenv()
url = os.getenv("URL")

page = get_page(url)
stations_data = parse_data(page)
save_new_file(stations_data)


def job_function():
    stations_status = parse_status(get_page(url))
    add_data_to_file(stations_status)
    print(f"{datetime.now()}: Выполняю задачу...")


def run_scheduler():
    scheduler = BackgroundScheduler()

    # Добавляем задачу с немедленным первым запуском и повторением каждую минуту
    scheduler.add_job(job_function, 'interval', minutes=1, next_run_time=datetime.now())
    scheduler.start()

    try:
        # Этот бесконечный цикл позволяет основному потоку оставаться активным,
        # чтобы немедленно реагировать на Ctrl+C.
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        print("Остановка планировщика...")
        # Останавливаем планировщик и ждем завершения всех запланированных заданий.
        scheduler.shutdown()


if __name__ == "__main__":
    run_scheduler()
