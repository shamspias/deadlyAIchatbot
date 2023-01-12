import os
from dotenv import load_dotenv
from flask import Flask, request, session, jsonify
from utils.deadlyaibot import get_answer, append_interaction_to_chat_log

from app.whatsapp_client import WhatsAppWrapper

app = Flask(__name__)
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


@app.route("/webhook/", methods=["POST", "GET"])
def webhook_whatsapp():
    """
    __summary__: Get message from the webhook
    To test the app
    """

    if request.method == "GET":
        if request.args.get('hub.verify_token') == VERIFY_TOKEN:
            return request.args.get('hub.challenge')
        return "Authentication failed. Invalid Token."

    client = WhatsAppWrapper()

    response = client.process_webhook_notification(request.get_json())

    # Do anything with the response
    # Sending a message to a phone number to confirm the webhook is working

    return jsonify({"status": "success"}, 200)


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
        if incoming_msg.startswith("/image"):
            response = client.send_normal_message("Image will be added soon", user)
        else:
            chat_log = session.get('chat_log')
            answer = get_answer(incoming_msg, chat_log)
            session['chat_log'] = append_interaction_to_chat_log(incoming_msg, answer,
                                                                 chat_log)

            response = client.send_normal_message(answer, user)

        return jsonify(
            {
                "data": response,
                "status": "success",
            },
        ), 200


if __name__ == '__main__':
    app.run(debug=os.getenv("DEBUG"))
