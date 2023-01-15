from src.app import celery_app
import random

celery = celery_app


@celery.task(bind=True)
def my_task(self):
    choice = random.choice(['Alpha',
                            'Beta',
                            'Gamma',
                            'Delta',
                            'Epsilon',
                            'Zeta',
                            'Eta',
                            'Theta',
                            'Iota',
                            'Kappa',
                            'Lambda',
                            'Mu',
                            'Nu',
                            'Xi',
                            'Omicron',
                            'Pi',
                            'Rho',
                            'Sigma',
                            'Tau',
                            'Upsilon',
                            'Phi',
                            'Chi',
                            'Psi',
                            'Omega'])

    return choice
