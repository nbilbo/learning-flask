from pathlib import Path
from typing import Iterator

import pytest

from app.database.connections import LocalConnection
from app.database.exceptions import MissingRequiredField
from app.database.exceptions import RegisterNotFound
from app.database.repositories import PostRepository
from app.database.repositories import UserRepository


@pytest.fixture(scope='function')
def connection() -> Iterator[LocalConnection]:
    local_connection = LocalConnection('sqlite:///test.sqlite')
    yield local_connection
    Path('test.sqlite').unlink()


def test_insert_one_must_return_some_value(connection: LocalConnection) -> None:
    user = UserRepository.insert_one(connection, 'admin', 'admin')
    post = PostRepository.insert_one(connection, 'Title', 'Body', user['iduser'])

    assert post is not None


def test_insert_one_must_return_dict(connection: LocalConnection) -> None:
    user = UserRepository.insert_one(connection, 'admin', 'admin')
    post = PostRepository.insert_one(connection, 'Title', 'Body', user['iduser'])

    assert isinstance(post, dict)


@pytest.mark.parametrize('key', ('idpost', 'title', 'body', 'id_user', 'username', 'created'))
def test_insert_one_must_return_dict_with_key(connection: LocalConnection, key: str) -> None:
    user = UserRepository.insert_one(connection, 'admin', 'admin')
    post = PostRepository.insert_one(connection, 'Title', 'Body', user['iduser'])

    assert post.get(key, None) is not None


def test_insert_one_must_update_user_posts(connection: LocalConnection) -> None:
    user = UserRepository.insert_one(connection, 'admin', 'admin')
    post = PostRepository.insert_one(connection, 'Title', 'Body', user['iduser'])

    updated_user = UserRepository.select_one(connection, iduser=user['iduser'])
    posts = updated_user.get('posts', [])

    assert len(posts) > 0


@pytest.mark.parametrize('title, body', [('Title', ''), ('', 'Body')])
def test_insert_one_raises_exception_if_required_field_is_blank(
    connection: LocalConnection, title: str, body: str
) -> None:
    user = UserRepository.insert_one(connection, 'admin', 'admin')
    with pytest.raises(MissingRequiredField):
        PostRepository.insert_one(connection, title, body, user['iduser'])


def test_insert_one_raises_exception_if_user_not_found(connection: LocalConnection) -> None:
    with pytest.raises(RegisterNotFound):
        post = PostRepository.insert_one(connection, 'Title', 'Body', 1)


def test_select_one_must_raises_exception_if_post_not_found(connection: LocalConnection) -> None:
    with pytest.raises(RegisterNotFound):
        PostRepository.select_one(connection, idpost=1)


def test_select_one_must_return_dict_if_register_exist(connection: LocalConnection) -> None:
    user = UserRepository.insert_one(connection, 'admin', 'admin')
    post = PostRepository.insert_one(connection, 'Title', 'Body', user['iduser'])
    register = PostRepository.select_one(connection, idpost=post['idpost'])

    assert isinstance(register, dict)


@pytest.mark.parametrize('key', ('idpost', 'title', 'body', 'id_user', 'username', 'created'))
def test_select_one_must_return_dict_with_key(connection: LocalConnection, key: str) -> None:
    user = UserRepository.insert_one(connection, 'admin', 'admin')
    post = PostRepository.insert_one(connection, 'Title', 'Body', user['iduser'])
    register = PostRepository.select_one(connection, idpost=post['idpost'])

    assert register.get(key, None) is not None


def test_select_all_must_return_all_registers(connection: LocalConnection) -> None:
    first_user = UserRepository.insert_one(connection, 'admin', 'admin')
    PostRepository.insert_one(connection, 'Title', 'Body', first_user['iduser'])
    PostRepository.insert_one(connection, 'Title Two', 'Body Two', first_user['iduser'])

    second_user = UserRepository.insert_one(connection, 'admin2', 'admin2')
    PostRepository.insert_one(connection, 'Title', 'Body', second_user['iduser'])
    PostRepository.insert_one(connection, 'Title Two', 'Body Two', second_user['iduser'])

    updated_first_user = UserRepository.select_one(connection, iduser=first_user['iduser'])
    updated_second_user = UserRepository.select_one(connection, iduser=second_user['iduser'])
    posts = PostRepository.select_all(connection)

    assert len(posts) == len(updated_first_user['posts']) + len(updated_second_user['posts'])


@pytest.mark.parametrize('field, value', [('title', 'updated title'), ('body', 'updated body')])
def test_update_one_must_persist_field_changes(connection: LocalConnection, field: str, value: str) -> None:
    user = UserRepository.insert_one(connection, 'admin', 'admin')
    post = PostRepository.insert_one(connection, 'Title', 'Body', user['iduser'])

    eval(f'PostRepository.update_one(connection, post["idpost"], {field}="{value}")')
    updated_post = PostRepository.select_one(connection, idpost=post['idpost'])

    assert updated_post[field] == value


def test_update_one_raises_exception_if_idpost_not_found(connection) -> None:
    user = UserRepository.insert_one(connection, 'admin', 'admin')
    post = PostRepository.insert_one(connection, 'Title', 'Body', user['iduser'])

    with pytest.raises(RegisterNotFound):
        PostRepository.update_one(connection, -1, title='Updated title', body='Updated body')


@pytest.mark.parametrize('field', ('title', 'body'))
def test_update_one_raises_exception_if_field_is_blank(connection: LocalConnection, field: str) -> None:
    user = UserRepository.insert_one(connection, 'admin', 'admin')
    post = PostRepository.insert_one(connection, 'Title', 'Body', user['iduser'])

    with pytest.raises(MissingRequiredField):
        eval(f'PostRepository.update_one(connection, post["idpost"], {field}="")')


def test_update_one_raises_exception_if_id_user_not_found(connection: LocalConnection) -> None:
    user = UserRepository.insert_one(connection, 'admin', 'admin')
    post = PostRepository.insert_one(connection, 'Title', 'Body', user['iduser'])

    with pytest.raises(RegisterNotFound):
        PostRepository.update_one(connection, post['idpost'], title='Updated title', body='Updated body', id_user=-1)


def test_delete_one_must_persist_changes(connection: LocalConnection) -> None:
    user = UserRepository.insert_one(connection, 'admin', 'admin')
    post = PostRepository.insert_one(connection, 'Title', 'Body', user['iduser'])
    PostRepository.delete_one(connection, post['idpost'])

    with pytest.raises(RegisterNotFound):
        PostRepository.select_one(connection, idpost=post['idpost'])
