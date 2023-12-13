from typing import Dict
from typing import List

from app.database.connections import LocalConnection
from app.database.entities import PostEntity
from app.database.entities import UserEntity
from app.database.exceptions import MissingRequiredField
from app.database.exceptions import RegisterNotFound
from app.database.repositories import UserRepository


class PostRepository:
    @staticmethod
    def check_insert_one(connection: LocalConnection, title: str, body: str, id_user: int) -> None:
        if not len(title):
            raise MissingRequiredField('title')

        elif not len(body):
            raise MissingRequiredField('body')

        try:
            UserRepository.select_one(connection, iduser=id_user)
        except RegisterNotFound as error:
            raise error

    @staticmethod
    def check_update_one(connection: LocalConnection, title: str, body: str, id_user: int) -> None:
        if not len(title):
            raise MissingRequiredField('title')

        elif not len(body):
            raise MissingRequiredField('body')

        try:
            user = UserRepository.select_one(connection, iduser=id_user)
        except RegisterNotFound as error:
            raise error

    @staticmethod
    def insert_one(connection: LocalConnection, title: str, body: str, id_user: int) -> Dict:
        PostRepository.check_insert_one(connection, title, body, id_user)

        with connection.Session() as session:
            user = session.query(UserEntity).filter(UserEntity.iduser == id_user).one()
            post = PostEntity(title=title, body=body, user=user)
            session.add(post)
            session.commit()

            return post.asdict()

    @staticmethod
    def select_one(connection: LocalConnection, **kwargs) -> Dict:
        with connection.Session() as session:
            registers = session.query(PostEntity).filter_by(**kwargs).all()
            if len(registers):
                post = registers[0].asdict()
                return post

        raise RegisterNotFound('post')

    @staticmethod
    def select_all(connection: LocalConnection) -> List[Dict]:
        registers: List[Dict] = []
        with connection.Session() as session:
            for post in session.query(PostEntity).all():
                registers.append(post.asdict())

        return registers

    @staticmethod
    def update_one(connection: LocalConnection, idpost: int, **kwargs) -> Dict:
        post = PostRepository.select_one(connection, idpost=idpost)
        title = kwargs.get('title', post['title'])
        body = kwargs.get('body', post['body'])
        id_user = kwargs.get('id_user', post['id_user'])
        PostRepository.check_update_one(connection, title, body, id_user)

        with connection.Session() as session:
            register = session.query(PostEntity).filter(PostEntity.idpost == idpost).one()
            user = session.query(UserEntity).filter(UserEntity.iduser == id_user).one()
            register.title = title
            register.body = body
            register.user = user
            session.commit()

            return register.asdict()

    @staticmethod
    def delete_one(connection: LocalConnection, idpost: int) -> None:
        with connection.Session() as session:
            registers = session.query(PostEntity).filter(PostEntity.idpost == idpost).all()
            if len(registers):
                post = registers[0]
                session.delete(post)
                session.commit()
