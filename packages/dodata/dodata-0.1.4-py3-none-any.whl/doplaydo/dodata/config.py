"""SDK Configuration."""
from dotenv import find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from sqlalchemy.engine import URL
import os
import multiprocessing


def get_affinity() -> int:
    """Get number of cores/threads available.

    On (most) linux we can get it through the scheduling affinity. Otherwise,
    fall back to the multiprocessing cpu count.
    """
    try:
        threads = len(os.sched_getaffinity(0))
    except AttributeError:
        threads = multiprocessing.cpu_count()
    return threads


dotenv_path = find_dotenv(usecwd=True)


class Config(BaseSettings):  # noqa: D101
    model_config = SettingsConfigDict(env_file=dotenv_path, extra="ignore")

    dodata_url: str
    dodata_user: str
    dodata_password: str
    dodata_db: str
    dodata_db_user: str
    dodata_db_password: str
    dodata_db_name: str = "dodata"
    dodata_db_port: int = 5432
    debug: bool = False
    n_threads: int = get_affinity() // 2 or 1
    n_cores: int = get_affinity() // 2 or 1
    ssl_verify: bool = True

    @property
    def dodata_db_connection_url(self) -> URL:
        """Calculates the connection URI."""
        if not self.dodata_db.startswith("sqlite:///"):
            return URL.create(
                drivername="postgresql+psycopg2",
                username=self.dodata_db_user,
                password=self.dodata_db_password,
                host=self.dodata_db,
                port=self.dodata_db_port,
                database=self.dodata_db_name,
            )
        else:
            return URL.create(
                drivername="sqlite",
                host=self.dodata_db.removeprefix("sqlite:///"),
            )


@lru_cache
def get_settings() -> Config:
    """The one and only settings."""
    return Config()
