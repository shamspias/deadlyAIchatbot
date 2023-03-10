from src.app import celery_app
from config.settings import GRAPH_API_URL, WHATSAPP_API_TOKEN, WHATSAPP_NUMBER_ID
import requests
import json
from flask import jsonify

celery = celery_app


class WhatsAppWrapper:
    API_URL = GRAPH_API_URL
    API_TOKEN = WHATSAPP_API_TOKEN
    NUMBER_ID = WHATSAPP_NUMBER_ID

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {self.API_TOKEN}",
            "Content-Type": "application/json",
        }
        self.API_URL = self.API_URL + self.NUMBER_ID

    def send_template_message(self, template_name, language_code, phone_number):
        payload = json.dumps({
            "object": "whatsapp_business_account",
            "entry": [{
                "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
                "changes": [{
                    "value": {

                        "messaging_product": "whatsapp",
                        "to": phone_number,
                        "type": "template",
                        "template": {
                            "name": template_name,
                            "language": {
                                "code": language_code
                            }
                        }
                    }
                }
                ]
            }
            ]
        })

        response = requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)

        assert response.status_code == 200, "Error sending message"

        return response.status_code

    def process_webhook_notification(self, data):
        """_summary_: Process webhook notification
        For the moment, this will return the type of notification
        """

        response = []

        for entry in data["entry"]:

            for change in entry["changes"]:
                try:
                    for mgs in change["value"]["messages"]:
                        response.append(
                            {
                                "type": change["field"],
                                "from": mgs["from"],
                                "mgs": mgs["text"]["body"],
                            }
                        )
                except:
                    response.append(
                        {
                            "type": change["field"],
                            "from": None,
                            "mgs": None,
                        }
                    )
        # Do whatever with the response
        return response


@celery.task(serializer='json', name="send_message")
def send_normal_message(replay, phone_number):
    payload = json.dumps({
        "messaging_product": "whatsapp",
        "to": phone_number,
        "text": {
            "body": replay,
        }
    })
    client = WhatsAppWrapper()

    response = requests.request("POST", f"{client.API_URL}/messages", headers=client.headers, data=payload)

    assert response.status_code == 200, jsonify({"error": "Error sending message"})

    return jsonify({"status": response.status_code})
