from rails.rail import Rail


class TopicalRail(Rail):
    def __init__(self, llm):
        super().__init__()
        super().__init__()
        self.llm = llm

    def check(self, query, history):
        return None