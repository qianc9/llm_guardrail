import torch
from llm.llm import Llm


class ChatGLM(Llm):
    def __init__(self, model, tokenizer):
        super().__init__()
        self.model = model
        self.tokenizer = tokenizer
        self.model.eval()

    def chat(self, user_prompt, system_prompt=None, history=[]):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        inputs = self.tokenizer(user_prompt, return_tensors="pt").to(device)

        with torch.no_grad():
            outputs = self.model.generate(**inputs, max_length=8000)

        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return generated_text
