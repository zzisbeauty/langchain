import os
import sys
import json

import requests
from cdify.utils.config import *
from cdify.utils.loggers import logger


def requests_datasets_list(
    page=1, 
    limit=100,
    keyword='',
    tag_ids = '',
):
    """ 获取知识库列表 """
    url = SERVER_BASE_URL + f"/datasets?page={page}&limit={limit}&keyword={keyword}"
    response = requests.get(url, headers=db_hearders)

    # print(type(response))
    # print(json.loads(response.text)['data'])
    # print("状态码:", response.status_code)
    # print("响应内容:", response.text)
    try:
        return json.loads(response.text)['data']
    except:
        return ''
