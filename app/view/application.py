from flask import Flask

from app import constants
from app.database.repositories import UserRepository
from app.view.blueprints import auth
from app.view.blueprints import blog
from app.view.database import get_database_connection


def configure_blog_routes(application: Flask) -> None:
    application.register_blueprint(blog.blueprint)
    application.add_url_rule('/', endpoint='index')


def configure_auth_routes(application: Flask) -> None:
    application.register_blueprint(auth.blueprint)


def configure_default_settings(application: Flask) -> None:
    application.config.from_mapping(SECRET_KEY='dev')


def configure_instance_folder(application: Flask) -> None:
    if not constants.INSTANCE_DIR.exists():
        constants.INSTANCE_DIR.mkdir()


def create_app() -> Flask:
    application = Flask(
        __name__,
        instance_relative_config=True,
        template_folder=constants.TEMPLATES_DIR.absolute(),
        static_folder=constants.STATIC_DIR.absolute(),
    )

    configure_blog_routes(application)
    configure_auth_routes(application)
    configure_instance_folder(application)
    configure_default_settings(application)

    return application
