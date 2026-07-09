from abc import ABC, abstractmethod


class WhatsAppProvider(ABC):

    @abstractmethod
    def send_text(self, chat_id, text):
        raise NotImplementedError