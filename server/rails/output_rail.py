import logging
from exception.exceptions import RailCheckError
from rails.rail import Rail
from util import genearte_prompt


class OutputRail(Rail):
    def __init__(self, llm):
        super().__init__()
        self.llm = llm

    def check(self, query, history=None):
        logging.info("进入输出护栏")
        data = {"llm_resp": query}
        prompt = genearte_prompt("output_rail.tpl", data)
        llm_resp = self.llm.chat(prompt)
        if llm_resp == "否":
            print(f"输出护栏校验结果：{llm_resp}")
            raise RailCheckError("模型输出不合法，请重新提问")
        