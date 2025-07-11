import os
import sys

import requests
from cdify.utils.config import *
from cdify.utils.loggers import logger



def say_hello():
    headers = {'Authorization': f'Bearer {secret_key}',}
    response = requests.get(url=SERVER_BASE_URL+'/info', headers=headers)

    # print("状态码:", response.status_code)
    # print("响应内容:", response.text)
    return response
