from abc import ABC, abstractmethod


class Prompt(ABC):
    @abstractmethod
    def generate(self, text: str) -> str:
        pass
