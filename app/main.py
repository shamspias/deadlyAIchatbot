import os
from dotenv import load_dotenv
from flask import Flask, request, session, jsonify

from celery import Celery

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

from utils.deadlyaibot import get_answer, append_interaction_to_chat_log
from app.whatsapp_client import WhatsAppWrapper

# if for some reason your conversation with the bot gets weird, change the secret key
load_dotenv()
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
VERIFY_TOKEN = os.getenv('WHATSAPP_HOOK_TOKEN')


# app.config['SECRET_KEY'] = '89djhff9lhkd93' # Testing


@app.route("/send_template_message/", methods=["POST"])
def send_template_message():
    """_summary_: Send a message with a template to a phone number"""

    if "language_code" not in request.json:
        return jsonify({"error": "Missing language_code"}), 400

    if "phone_number" not in request.json:
        return jsonify({"error": "Missing phone_number"}), 400

    if "template_name" not in request.json:
        return jsonify({"error": "Missing template_name"}), 400

    client = WhatsAppWrapper()

    response = client.send_template_message(
        template_name=request.json["template_name"],
        language_code=request.json["language_code"],
        phone_number=request.json["phone_number"],
    )
    print(response)
    return jsonify(
        {
            "data": response,
            "status": "success",
        },
    ), 200


@app.route('/deadlyai/', methods=["POST", "GET"])
def deadly_text_chat():
    if request.method == "GET":
        if request.args.get('hub.verify_token') == VERIFY_TOKEN:
            return request.args.get('hub.challenge')
        return "Authentication failed. Invalid Token."

    if request.method == "POST":
        client = WhatsAppWrapper()
        row_data = request.get_json()
        data = client.process_webhook_notification(row_data)
        user = data[0]['from']
        incoming_msg = data[0]['mgs']

        if incoming_msg is not None:
            if incoming_msg.startswith("/image"):
                response = client.send_normal_message("Image will be added soon", user)
            else:
                chat_log = session.get('chat_log')
                answer = get_answer(incoming_msg, chat_log)
                session['chat_log'] = append_interaction_to_chat_log(incoming_msg, answer,
                                                                     chat_log)
                if user is not None:
                    response = client.send_normal_message(answer, user)
                else:
                    response = "No User"
        else:
            response = "No Data"

        return jsonify(
            {
                "data": response,
                "status": "success",
            },
        ), 200


if __name__ == '__main__':
    app.run(debug=os.getenv("DEBUG"))
