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



def say_hello():
    headers = {'Authorization': f'Bearer {secret_key}',}
    response = requests.get(url=SERVER_BASE_URL+'/info', headers=headers)

    # print("状态码:", response.status_code)
    # print("响应内容:", response.text)

    return response

