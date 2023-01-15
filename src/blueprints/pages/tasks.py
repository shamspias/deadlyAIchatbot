from src.app import celery_app
import random

celery = celery_app


@celery.task(bind=True)
def my_task(self):
    choice = random.choice(['Psi', 'Omega'])

    return choice
