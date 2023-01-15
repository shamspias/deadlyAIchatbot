from flask import (Blueprint,
                   render_template,
                   request,
                   jsonify,
                   session)
from config.settings import WHATSAPP_HOOK_TOKEN
from open_ai_connection import ask, append_interaction_to_chat_log
from whatsapp_client import WhatsAppWrapper

page = Blueprint('pages', __name__, template_folder='templates')

VERIFY_TOKEN = WHATSAPP_HOOK_TOKEN


@page.route("/")
def index():
    """
    Index / Main page
    :return: html
    """

    return render_template('index.html')


@page.route("/_execute_task", methods=['POST'])
def _execute_task():
    """
    Invoke this function from an Ajax Call
    :return: json
    """
    from src.blueprints.pages.tasks import my_task

    if request.method == 'POST':
        # Invoke celery task
        task = my_task.delay()

    return jsonify({'taskID': task.id}), 201
