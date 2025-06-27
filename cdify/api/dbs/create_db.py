import os
import sys

sys.path.append(r'E:\langchain-core-0.3.64')
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.append(project_root)

from cdify.tools import *

import json
import requests




def create_db_new(db_name):
    url = SERVER_BASE_URL + "/datasets"
    response = requests.post(url, headers=db_hearders, json={"name":db_name})

    # print("状态码:", response.status_code)
    # print("响应内容:", response.text)
    return response


def create_db_old(data):
    """ 使用复杂 parameters | old db create function """
    url = SERVER_BASE_URL + "/datasets"
    response = requests.post(url, headers=db_hearders, json=data)

    # print("状态码:", response.status_code)
    # print("响应内容:", response.text)
    return response
