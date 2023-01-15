from flask import (Blueprint,
                   render_template,
                   request,
                   jsonify,
                   session)
from config.settings import WHATSAPP_HOOK_TOKEN

page = Blueprint('pages', __name__, template_folder='templates')

VERIFY_TOKEN = WHATSAPP_HOOK_TOKEN


# @page.route("/")
# def index():
#     """
#     Index / Main page
#     :return: html
#     """
#
#     return render_template('index.html')
#


@page.route("/send_template_message/", methods=["POST"])
def send_template_message():
    """_summary_: Send a message with a template to a phone number"""

    from open_ai_connection import ask, append_interaction_to_chat_log
    from src.blueprints.pages.whatsapp_client import WhatsAppWrapper

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


@page.route('/deadlyai/', methods=["POST", "GET"])
def deadly_text_chat():
    """
    Send mgs
    :return:
    """
    from src.blueprints.pages.open_ai_connection import ask, append_interaction_to_chat_log
    from src.blueprints.pages.whatsapp_client import WhatsAppWrapper

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
                response = client.send_normal_message(replay="Image will be added soon", phone_number=user)
            else:
                chat_log = session.get('chat_log')
                answer = ask.delay(incoming_msg, chat_log)
                session['chat_log'] = append_interaction_to_chat_log(incoming_msg, answer,
                                                                     chat_log)
                if user is not None:
                    response = client.send_normal_message(replay=answer, phone_number=user)
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
