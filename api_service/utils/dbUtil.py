import databases
import sqlalchemy
from functools import lru_cache
import config
from models import metadata


# 1. using Pydantic to load configuration
@lru_cache()
def setting():
    return config.Settings()


def database_pgsql_url_config():
    return str(
        setting().DB_CONNECTION
        + "://"
        + setting().DB_USERNAME
        + ":"
        + setting().DB_PASSWORD
        + "@"
        + setting().DB_HOST
        + ":"
        + setting().DB_PORT
        + "/"
        + setting().DB_DATABASE
    )


database = databases.Database(database_pgsql_url_config())
engine = sqlalchemy.create_engine(database_pgsql_url_config())
metadata.create_all(engine)
