from typing import Dict
from typing import Union

from flask import abort
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import request
from flask import render_template
from flask import url_for
from werkzeug.wrappers.response import Response

from app.database.exceptions import MissingRequiredField
from app.database.exceptions import RegisterNotFound
from app.database.repositories import PostRepository
from app.view.blueprints.auth import login_required
from app.view.database import get_database_connection
from app.view.exceptions import NotPostOwner


blueprint = Blueprint('blog', __name__)


@blueprint.route('/', methods=('GET',))
def index() -> str:
    connection = get_database_connection()
    posts = PostRepository.select_all(connection)

    return render_template('blog/index.html', posts=posts)


@blueprint.route('/create', methods=('GET', 'POST'))
@login_required
def create() -> Union[Response, str]:
    if request.method == 'POST':
        try:
            title = request.form.get('title', '')
            body = request.form.get('body', '')
            connection = get_database_connection()
            PostRepository.insert_one(connection, title, body, g.user['iduser'])

        except (MissingRequiredField, RegisterNotFound) as error:
            flash(str(error))

        else:
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


@blueprint.route('/<int:idpost>/update', methods=('GET', 'POST'))
def update(idpost: int) -> Union[Response, str]:
    post = get_post(idpost)

    if request.method == 'POST':
        try:
            connection = get_database_connection()
            title = request.form.get('title', '')
            body = request.form.get('body', '')
            PostRepository.update_one(connection, post['idpost'], title=title, body=body)

        except (RegisterNotFound, MissingRequiredField) as error:
            flash(str(error))

        else:
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@blueprint.route('/<int:idpost>/delete', methods=('POST',))
def delete(idpost: int) -> Response:
    post = get_post(idpost)
    connection = get_database_connection()
    PostRepository.delete_one(connection, post['idpost'])

    return redirect(url_for('blog.index'))


def get_post(idpost: int, check_author: bool = True) -> Dict:
    try:
        connection = get_database_connection()
        post = PostRepository.select_one(connection, idpost=idpost)

        if check_author and post['id_user'] != g.user['iduser']:
            raise NotPostOwner

    except RegisterNotFound as error:
        abort(404, str(error))

    except NotPostOwner as error:
        abort(403, str(error))

    else:
        return post
