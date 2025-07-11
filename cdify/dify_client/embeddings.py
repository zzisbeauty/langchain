import os
import sys

import requests
from cdify.utils.config import *
from cdify.utils.loggers import logger




"""
curl --location --request GET 'http://10.0.15.21/v1/datasets/{dataset_id}/documents/{batch}/indexing-status' \
--header 'Authorization: Bearer {api_key}'
"""
# http://10.0.15.21/v1/datasets/2252d06e-b335-46e2-bec7-c47101e65072/documents/20250702073600105213/indexing-status
def docProcess(dataset_id, batch):
    url = SERVER_BASE_URL + f'/datasets/{dataset_id}/documents/{batch}/indexing-status'
    response = requests.get(url, headers=db_hearders)
    # print("状态码:",  response.status_code)
    # print("响应内容:", response.text)
    return response