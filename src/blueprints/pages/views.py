from flask import current_app as app
from flask import (Blueprint,
                   render_template,
                   request,
                   jsonify)

import sqlite3
import pandas as pd

page = Blueprint('pages', __name__, template_folder='templates')


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