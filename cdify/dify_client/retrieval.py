import os
import sys
import json
import requests
from cdify.utils.config import *
from cdify.utils.loggers import logger




def retrieval(dataset_id, data):
    url = SERVER_BASE_URL + f'/datasets/{dataset_id}/retrieve'
    response = requests.post(url, headers=db_hearders, json=data)
    
    # print("状态码:", response.status_code)
    # print("响应内容:", response.text)
    return response
