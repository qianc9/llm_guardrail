from collections import defaultdict, deque


class ChatHistory:
    def __init__(self, max_size=100) -> None:
        self.histories = defaultdict(lambda: deque(maxlen=max_size))

    def add_message(self, session_id, user, content):
        self.histories[session_id].append({"user": user, "content": content})

    def __getitem__(self, session_id):
        return list(self.histories[session_id])
