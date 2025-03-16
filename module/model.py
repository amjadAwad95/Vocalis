from abc import ABC, abstractmethod


class Model(ABC):
    @abstractmethod
    async def run(self):
        pass
