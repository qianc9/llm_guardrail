import json
import logging
from flask import Flask, request, session, jsonify, make_response
from flask_session import Session
import os

import torch
from transformers import AutoTokenizer, AutoModel

from chat_history import ChatHistory
from exception.exceptions import RailCheckError
from llm.chatglm import ChatGLM
from llm.netgpt import NetGPT
from rails.input_rail import InputRail
from rails.output_rail import OutputRail
from rails.topical_rail import TopicalRail

app = Flask(__name__)

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 设置 Flask session 配置
app.config["SECRET_KEY"] = "supersecretkey"
app.config["SESSION_TYPE"] = "filesystem"  # 将 session 存储在服务器的文件系统中

# 初始化 session
Session(app)

# 初始化对话历史，加载进内存
chat_history = ChatHistory()

# 定义模型和 tokenizer 全局变量
model = None
tokenizer = None
llm = None

def load_model():
    global model, tokenizer, llm
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if model is None:
        model_name = "ChatGLM"
        if model_name == "ChatGLM":
            model_path = "/home/qianc/Models/chatglm3-6b"
            tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
            model = AutoModel.from_pretrained(model_path, trust_remote_code=True).to(device)
            llm = ChatGLM(model, tokenizer)
        elif model_name == "NetGPT":
            llm = NetGPT()

load_model()


input_rail = InputRail(llm)
topical_rail = TopicalRail(llm)
output_rail = OutputRail(llm)


@app.route("/api/query", methods=["POST"])
def handle_query():
    try:
        if not llm:
            raise Exception("fail to load model")

        if "session_id" not in session:
            session["session_id"] = os.urandom(24).hex()  # 生成一个新的 session_id

        session_id = session["session_id"]

        if not request.is_json:
            raise ValueError("Request must be JSON")

        user_query = request.json.get("query")
        # chat_history.add_message(session_id, "user", user_query)
        print(chat_history)

        try:
            input_rail.check(user_query, chat_history[session_id])
            topical_rail.check(user_query, chat_history[session_id])
            # llm_resp = llm.chat(user_query, chat_history[session_id])
            llm_resp = llm.chat(user_query)
            logging.info(f"模型输出:{llm_resp}")
            output_rail.check(llm_resp, None)
        except RailCheckError as e:
            llm_resp = e.message

        chat_history.add_message(session_id, "assistant", llm_resp)

        # 处理用户查询，这里简单返回用户的查询和 session_id
        response = {
            "session_id": session_id,
            "query": user_query,
            "response": llm_resp,
        }

        json_response = json.dumps(response, ensure_ascii=False)
        response_object = make_response(json_response, 200)
        response_object.headers["Content-Type"] = "application/json; charset=utf-8"
        return response_object
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify(
            {"error": "An unexpected error occurred", "message": str(e)}
        ), 500


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
