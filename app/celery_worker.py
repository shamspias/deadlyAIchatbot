from celery import Celery
from flask import Flask

app = Flask(__name__)
app.config.update(CELERY_CONFIG={
    'broker_url': 'redis://localhost:6379',
    'result_backend': 'redis://localhost:6379',
})


def make_celery(flask_app):
    celery = Celery(
        flask_app.import_name,
        result_backend=flask_app.config["RESULT_BACKEND_CELERY"],
        broker=flask_app.config["CELERY_BROKER_URL"],
    )
    celery.conf.update(flask_app.config)

    return celery


celery = make_celery(app)
