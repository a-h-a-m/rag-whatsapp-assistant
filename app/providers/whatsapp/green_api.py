from app.providers.whatsapp.provider import WhatsAppProvider
from whatsapp_api_client_python import API


class GreenAPIProvider(WhatsAppProvider):
    def __init__(self, instance_id, token):
        self.client = API.GreenAPI(
            instance_id,
            token
        )

    def send_text(self, chat_id, message):
        response = self.client.sending.sendMessage(
            chat_id,
            message
        )

        return response