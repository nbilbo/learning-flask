from pathlib import Path
from typing import Iterator

import pytest

from app.database.connections import LocalConnection
from app.database.exceptions import AlreadyRegistered
from app.database.exceptions import MissingRequiredField
from app.database.exceptions import RegisterNotFound
from app.database.repositories import UserRepository


@pytest.fixture(scope='function')
def connection() -> Iterator[LocalConnection]:
    local_connection = LocalConnection('sqlite:///test.sqlite')
    yield local_connection
    Path('test.sqlite').unlink()


def test_insert_one_must_return_some_value(connection: LocalConnection) -> None:
    user = UserRepository.insert_one(connection, 'admin', 'admin')

    assert user is not None


def test_insert_one_must_return_dict(connection: LocalConnection) -> None:
    user = UserRepository.insert_one(connection, 'admin', 'admin')

    assert isinstance(user, dict)


@pytest.mark.parametrize('key', ('iduser', 'username', 'password', 'posts'))
def test_insert_one_must_return_dict_with_key(connection: LocalConnection, key: str) -> None:
    user = UserRepository.insert_one(connection, 'admin', 'admin')

    assert user.get(key, None) is not None


@pytest.mark.parametrize('username, password', [('admin', ''), ('', 'password')])
def test_insert_one_raises_exception_if_required_field_is_blank(
    connection: LocalConnection, username: str, password: str
) -> None:
    with pytest.raises(MissingRequiredField):
        UserRepository.insert_one(connection, username, password)


def test_insert_one_raises_exception_if_username_already_registered(connection: LocalConnection) -> None:
    UserRepository.insert_one(connection, 'admin', 'admin')
    with pytest.raises(AlreadyRegistered):
        UserRepository.insert_one(connection, 'admin', 'admin')


def test_select_one_must_return_dict_if_register_exist(connection: LocalConnection) -> None:
    user = UserRepository.insert_one(connection, 'admin', 'admin')
    register = UserRepository.select_one(connection, iduser=user['iduser'])

    assert isinstance(register, dict)


@pytest.mark.parametrize('key', ('iduser', 'username', 'password', 'posts'))
def test_select_one_must_return_dict_with_key(connection: LocalConnection, key: str) -> None:
    user = UserRepository.insert_one(connection, 'admin', 'admin')
    register = UserRepository.select_one(connection, iduser=user['iduser'])

    assert register.get(key, None) is not None


def test_select_one_must_raises_exception_if_user_not_found(connection: LocalConnection) -> None:
    with pytest.raises(RegisterNotFound):
        UserRepository.select_one(connection, iduser=1)
