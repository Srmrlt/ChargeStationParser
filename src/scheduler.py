import time

import schedule


def run_scheduler(job):
    schedule.every().monday.do(job.change_file_name)
    schedule.every().minute.do(job.job_function)

    try:
        # Этот бесконечный цикл позволяет основному потоку оставаться активным,
        # чтобы немедленно реагировать на Ctrl+C.
        while True:
            schedule.run_pending()
            time.sleep(5)
    except (KeyboardInterrupt, SystemExit):
        print("Остановка планировщика...")
