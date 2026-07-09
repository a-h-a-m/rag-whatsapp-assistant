from abc import ABC, abstractmethod


class AIProvider(ABC):

    @abstractmethod
    def chat(self, messages):
        raise NotImplementedError


    @abstractmethod
    def transcribe(self, file_path):
        raise NotImplementedError


    @abstractmethod
    def embed(self, text):
        raise NotImplementedError