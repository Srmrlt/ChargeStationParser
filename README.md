# Charging Stations Data Scraper

This project is designed to scrape data from a website that provides information about electric vehicle charging stations, including station type, location, and current status (available, occupied, not working). The purpose of this project is to collect and analyze data to estimate the company's financial performance based on charging rates and station occupancy times.


## Project Overview

The scraper performs the following tasks:
1. Fetches the webpage with station statuses every minute.
2. Parses and validates the data according to the required fields.
3. Stores the data in a TimescaleDB (Postgres-based) database.

Additionally, the scraper logs the date when a new station appears on the list.

## Technologies Used

- **Python**: The core programming language for this project.
- **BeautifulSoup4**: For parsing HTML content.
- **SQLAlchemy**: ORM for database interaction.
- **Alembic**: For database migrations.
- **TimescaleDB**: A PostgreSQL-based database optimized for time-series data.
- **Asyncio**: For asynchronous data storage.
- **Docker**: For containerizing the application and database.

## Database Choice Justification

We chose TimescaleDB, an extension of PostgreSQL, due to its optimized handling of time-series data. This allows efficient storage and querying of timestamped data, which is crucial for analyzing station statuses over time.

## Data Flow

1. **Data Collection**: The scraper fetches the webpage every minute.
2. **Data Parsing**: Extracts relevant information using BeautifulSoup4.
3. **Data Validation**: Ensures data integrity and formats it for storage.
4. **Data Storage**: Asynchronously stores data in TimescaleDB using SQLAlchemy.

## Data Analysis

The collected data will be analyzed using Microsoft Power BI to evaluate financial performance metrics such as revenue based on charging station occupancy times.

## How to Run

1. **Clone the repository:**

    ```bash
    git clone git clone https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY_NAME.git
    cd YOUR_REPOSITORY_NAME
    ```

2. **Environment Setup:**

    Copy the example environment file to create your own environment variables file:

    ```bash
    cp .env.example .env
    ```

    Edit the `.env` file to suit your environment settings like database credentials.

3. **Build and Run with Docker Compose:**

    Use Docker Compose to build and run the services defined in the `docker-compose.yml` file:

    ```bash
    docker compose up --build -d
    ```

    This command will start all the required services in detached mode.
4. **Stopp the Service:**

   To stop all services, use the following Docker Compose command:

    ```bash
    docker compose down -v
    ```

## Thanks for Visiting!
