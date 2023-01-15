from flask import Flask
from src.blueprints.pages.views import page
from celery import Celery
from src.celery_task_registry import CELERY_TASK_LIST


def make_celery(app=None):
    """
    Make Celery App
    :param app: flask app instance
    :return: celery
    """

    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'],
                                     include=CELERY_TASK_LIST)

    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery


def create_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern.

    :return: Flask app
    """

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)

    if settings_override:
        app.config.update(settings_override)

    app.register_blueprint(page)

    return app


flask_app = create_app()
celery_app = make_celery(flask_app)
