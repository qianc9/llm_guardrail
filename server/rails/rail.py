from abc import ABC, abstractmethod


class Rail(ABC):

    @abstractmethod
    def check(self, query, history):
        pass