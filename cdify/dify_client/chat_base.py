import os
import sys

import requests
from cdify.utils.config import *
from cdify.utils.loggers import logger


def start_chat(data):
    """ 发送聊天请求 with conversation_id """
    chat_url = SERVER_BASE_URL + '/chat-messages'
    response = requests.post(chat_url, headers=app_headers, json=data)

    # print("状态码:", response.status_code)
    # print("响应内容:", response.text)
    return response