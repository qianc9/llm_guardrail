from abc import ABC, abstractmethod


class Llm(ABC):

    @abstractmethod
    def chat(self, user_prompt, system_prompt):
        pass