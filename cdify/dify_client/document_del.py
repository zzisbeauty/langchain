import os
import sys

import requests
from cdify.utils.config import *
from cdify.utils.loggers import logger



"""
curl --location --request DELETE 'http://10.0.15.21/v1/datasets/{dataset_id}/documents/{document_id}' \
--header 'Authorization: Bearer {api_key}'
"""
def docdelete(dataset_id, document_id):
    url = SERVER_BASE_URL + f'/datasets/{dataset_id}/documents/{document_id}'
    try:
        requests.delete(url, headers=db_hearders)
        return f'delete document true'
    except:
        return f'delete document false' 

    # print("状态码:",  response.status_code)
    # print("响应内容:", response.text)
    return response