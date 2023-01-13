import os
import requests
from dotenv import load_dotenv
import json
from celery import Celery

celery_app = Celery(
    "tasks", broker="redis://localhost:6379", CELERY_RESULT_BACKEND="redis://localhost:6379"
)

load_dotenv()


class WhatsAppWrapper:
    API_URL = "https://graph.facebook.com/v15.0/"
    API_TOKEN = os.getenv("WHATSAPP_API_TOKEN")
    NUMBER_ID = os.getenv("WHATSAPP_NUMBER_ID")

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {self.API_TOKEN}",
            "Content-Type": "application/json",
        }
        self.API_URL = self.API_URL + self.NUMBER_ID

    def send_template_message(self, template_name, language_code, phone_number):
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": language_code
                }
            }
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

    @celery_app.task(name="send_message")
    def send_normal_message(self, replay, phone_number):
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "to": phone_number,
            "text": {
                "body": replay,
            }
        })

        response = requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)

        assert response.status_code == 200, "Error sending message"

        return response.status_code
