import json
import os
from http import HTTPStatus
from typing import Any, Dict, List

import requests
from dotenv import load_dotenv
from logger_local.Logger import Logger
from message_local.MessageImportance import MessageImportance
from message_local.MessageLocal import MessageLocal
from message_local.Recipient import Recipient

from .WhatsAppLocalConstants import (WHATSAPP_API_URL, WHATSAPP_HEADERS,
                                     WHATSAPP_MESSAGE_INFORU_API_TYPE_ID,
                                     get_logger_object)

load_dotenv()

INFORU_AUTH_TOKEN = os.getenv("INFORU_AUTH_TOKEN")


class WhatsAppMessageInforuLocal(MessageLocal):
    # don't rename the parameters, unless you do that in MessagesLocal.send_sync.message_local.__init__ as well
    def __init__(self, original_body: str, to_recipients: List[Recipient],
                 importance: MessageImportance = MessageImportance.MEDIUM) -> None:
        super().__init__(original_body=original_body, importance=importance, to_recipients=to_recipients,
                         api_type_id=WHATSAPP_MESSAGE_INFORU_API_TYPE_ID)
        self.logger = Logger.create_logger(object=get_logger_object())

    def send(self, Message_Media: str = None) -> Dict[str, Any]:
        try:
            # Can also add: "FirstName", "LastName", "CouponCode", "MessageMedia"
            recipients_details = [{"Phone": recipient.get_canonical_telephone()} for recipient in self.get_recipients()]
            # TODO: should we POST for each recipient or can we use the same message for all of them?
            message = list(self.get_body_after_text_template().values())[0]
            self.logger.start("WhatsApp message send", object={
                "message": message, "messageMedia": Message_Media})
            payload = {
                "Data": {
                    "Message": message,
                    "Recipients": recipients_details
                }
            }
            if Message_Media:
                payload["Data"]["messageMedia"] = Message_Media
            url = WHATSAPP_API_URL
            headers = {
                **WHATSAPP_HEADERS,
                'Authorization': INFORU_AUTH_TOKEN
            }
            payload_json = json.dumps(payload)
            if os.getenv("REALLY_SEND_WHATSAPP"):
                response = requests.post(url, headers=headers, json=payload_json)
            else:
                print("Supposed to send the following payload to InforU: " + payload_json)
                return {"status": "success", "message": "Message sent successfully"}

            # Check the response using HTTPStatus.OK from the http library.
            if response.status_code == HTTPStatus.OK:
                self.logger.info("Request Payload: " + json.dumps(payload))
                self.logger.info("Request Headers: " + str(headers))
                self.logger.info("Response Status Code: " + str(response.status_code))
                self.logger.info("Response Content: " + response.text)
                self.logger.info(f"WhatsApp sent successfully to {recipients_details}.")
                self.logger.info("Response: " + response.text)
            else:
                self.logger.error(
                    f"SMS sending failed to {recipients_details} with status code: {response.status_code}")

            # Assuming the function returns a dictionary with some data
            return {"status": "success", "message": "Message sent successfully"}

        except Exception as e:
            self.logger.exception("Sending to WhatsApp via InforU failed", object=e)
            self.logger.end()
            raise
        finally:
            self.logger.end("WhatsApp message send")
