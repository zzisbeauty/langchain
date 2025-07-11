import os
import sys
import json

import requests
from cdify.utils.config import *
from cdify.utils.loggers import logger


def request_dbinfo(dataset_id = ''):
    url = SERVER_BASE_URL + f'/datasets/{dataset_id}'
    response = requests.get(url, headers=db_hearders)

    # print("状态码:", response.status_code)
    # print("响应内容:", response.text)
    try:
        return json.loads(response.text)
    except Exception as e:
        print(e)
        return ''