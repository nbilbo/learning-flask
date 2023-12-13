from typing import Dict
from typing import Optional

from app.database.connections import LocalConnection
from app.database.entities import UserEntity
from app.database.exceptions import AlreadyRegistered
from app.database.exceptions import MissingRequiredField
from app.database.exceptions import RegisterNotFound


class UserRepository:
    @staticmethod
    def check_insert_one(conneciton: LocalConnection, username: str, password: str) -> None:
        if not len(username):
            raise MissingRequiredField('username')

        elif not len(password):
            raise MissingRequiredField('password')

        try:
            UserRepository.select_one(conneciton, username=username)
            raise AlreadyRegistered(username)

        except RegisterNotFound:
            pass

    @staticmethod
    def insert_one(connection: LocalConnection, username: str, password: str) -> Dict:
        UserRepository.check_insert_one(connection, username, password)

        with connection.Session() as session:
            user = UserEntity(username=username, password=password)
            session.add(user)
            session.commit()

            return user.asdict()

    @staticmethod
    def select_one(connection: LocalConnection, **kwargs) -> Dict:
        with connection.Session() as session:
            registers = session.query(UserEntity).filter_by(**kwargs).all()
            if len(registers):
                user = registers[0]
                return user.asdict()

        raise RegisterNotFound('user')
