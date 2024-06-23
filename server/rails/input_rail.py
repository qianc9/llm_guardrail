import logging
from rails.rail import Rail
from exception.exceptions import RailCheckError
from util import genearte_prompt


class InputRail(Rail):
    def __init__(self, llm):
        super().__init__()
        self.llm = llm

    def check(self, query, history):
        logging.info("进入输入护栏")
        data = {"user_input": query}
        prompt = genearte_prompt("input_rail.tpl", data)
        llm_resp = self.llm.chat(prompt)
        if llm_resp == "否":
            print(f"输入护栏校验结果：{llm_resp}")
            raise RailCheckError("用户输入不合法，请重新输入")
