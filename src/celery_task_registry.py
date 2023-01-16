"""
Task List Registry to be included in celery
celery = Celery(app.import_name,
                    backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'],
                    include=CELERY_TASK_LIST)
"""

CELERY_TASK_LIST = [
    'src.blueprints.pages.tasks',
    # 'src.blueprints.pages.whatsapp_client',
    'src.blueprints.pages.open_ai_connection',
]
