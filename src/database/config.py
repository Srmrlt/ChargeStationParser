import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    POSTGRES_DB: str

    @property
    def db_url(self):
        """
        Generates a database connection URL for database libraries from the given settings.
        """
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings(
    POSTGRES_USER=os.getenv("POSTGRES_USER"),
    POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD"),
    DB_HOST=os.getenv("DB_HOST"),
    DB_PORT=int(os.getenv("DB_PORT")),
    POSTGRES_DB=os.getenv("POSTGRES_DB"),
)
