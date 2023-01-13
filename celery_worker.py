from celery import Celery
from app.main import app


def make_celery(flask_app):
    celery = Celery(
        flask_app.import_name,
        result_backend=flask_app.config["RESULT_BACKEND_CELERY"],
        broker=flask_app.config["CELERY_BROKER_URL"],
    )
    celery.conf.update(flask_app.config)

    return celery


celery = make_celery(app)
