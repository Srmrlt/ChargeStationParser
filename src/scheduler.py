import time
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler


def run_scheduler(job_function):
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
