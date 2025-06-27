import os
import sys
import json, requests
from flask import Flask, request

# sys.path.append("/home/langchain-core-0.3.64")
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.append(project_root)

from cdify.tools import *
from cdify.loggers import logger



def start_chat(data):
    chat_url = SERVER_BASE_URL + '/chat-messages'
    response = requests.post(chat_url, headers=app_headers, json=data)
    # print("状态码:", response.status_code)
    # print("响应内容:", response.text)
    return response
