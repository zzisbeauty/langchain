import os
import sys
import json

import requests
from cdify.utils.config import *



def delete_db(dataset_id):
    url = SERVER_BASE_URL + f"/datasets/{dataset_id}"
    try:
        requests.delete(url, headers=db_hearders)
        return f'delete DB {dataset_id} true'
    except:
        return f'delete DB {dataset_id} false'    

    # print("状态码:", response.status_code)
    # print("响应内容:", response.text)
    return response