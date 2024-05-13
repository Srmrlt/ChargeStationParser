import asyncio
import logging
import os

from dotenv import load_dotenv

import src

load_dotenv()
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


async def job_function():
    """
    Asynchronously fetches a web page, parses station data from it, and updates the database with the new data.

    This function performs the following steps:
    1. Retrieves the URL from environment variables.
    2. Uses a web page loader to fetch the page at the given URL.
    3. If the page is successfully fetched, it parses the station data from the page.
    4. Adds the parsed station data to the database using an ORM method designed for station data.
    """
    url = os.getenv("URL")
    page = src.WebPageLoader(url).fetch_page()
    if page:
        stations_data = src.StationDataParser(page).parse_data()
        await src.StationOrmMethod().add_stations(stations_data)
        logger.debug("In progress ...")


if __name__ == "__main__":
    asyncio.run(src.run_scheduler(job_function))
