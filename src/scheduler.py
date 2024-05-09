import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

scheduler = AsyncIOScheduler()
logger = logging.getLogger(__name__)


async def run_scheduler(job):
    """
    Schedules and starts a job to be executed every minute at the beginning of the minute (when second is 0).

    Args:
    job (coroutine function): The asynchronous function to be scheduled and run every minute.

    This function adds the job to the scheduler using a cron trigger that fires every minute when the seconds are '0'.
    It then starts the scheduler to begin job execution. The function runs indefinitely until an interruption (like
    KeyboardInterrupt or SystemExit) occurs, upon which it logs the shutdown message and exits gracefully.
    """
    scheduler.add_job(job, CronTrigger(second="0"))
    scheduler.start()
    try:
        await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        logger.info("Stopping the scheduler ...")
        scheduler.shutdown()
