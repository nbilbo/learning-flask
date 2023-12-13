from app import constants
from app.database.connections import LocalConnection


def get_database_connection() -> LocalConnection:
    return LocalConnection(f'sqlite:///{constants.LOCAL_DATABASE_PATH}')
