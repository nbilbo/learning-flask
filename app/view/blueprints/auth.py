import functools
from typing import Callable
from typing import Union

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import request
from flask import render_template
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from werkzeug.wrappers.response import Response

from app import constants
from app.database.exceptions import AlreadyRegistered
from app.database.exceptions import MissingRequiredField
from app.database.exceptions import RegisterNotFound
from app.database.repositories import UserRepository
from app.view.database import get_database_connection
from app.view.exceptions import InvalidUsernamePassword


blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@blueprint.route('/register', methods=('GET', 'POST'))
def register() -> Union[Response, str]:
    if request.method == 'POST':
        try:
            username = request.form.get('username', '')
            password = request.form.get('password', '')
            connection = get_database_connection()
            user = UserRepository.insert_one(connection, username, generate_password_hash(password))

        except (MissingRequiredField, AlreadyRegistered) as error:
            flash(str(error))

        else:
            return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@blueprint.route('/login', methods=('GET', 'POST'))
def login() -> Union[Response, str]:
    if request.method == 'POST':
        try:
            username = request.form.get('username', '')
            password = request.form.get('password', '')
            connection = get_database_connection()
            user = UserRepository.select_one(connection, username=username)
            if not check_password_hash(user['password'], password):
                raise InvalidUsernamePassword

        except (MissingRequiredField) as error:
            flash(str(error))

        except (RegisterNotFound, InvalidUsernamePassword):
            flash('Invalid username or password.')

        else:
            session.clear()
            session['iduser'] = user['iduser']
            return redirect(url_for('blog.index'))

    return render_template('auth/login.html')


@blueprint.route('/logout', methods=('GET',))
def logout() -> Response:
    session.clear()

    return redirect(url_for('blog.index'))


@blueprint.before_app_request
def load_user():
    iduser = session.get('iduser', None)

    if iduser is None:
        g.user = None
    else:
        connection = get_database_connection()
        user = UserRepository.select_one(connection, iduser=iduser)
        g.user = user


def login_required(view) -> Callable:
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
