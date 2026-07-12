from abc import ABC, abstractmethod


class Tool(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def description(self):
        pass

    @abstractmethod
    def run(self, query):
        pass

    # @property
    # def requires_llm_response(self):
    #     return True
