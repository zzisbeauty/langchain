import os
import sys
import json, requests


sys.path.append(r'E:\langchain-core-0.3.64')
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.append(project_root)


from cdify.tools import *



def edit_db(dataset_id, data):
    url = SERVER_BASE_URL + f"/datasets/{dataset_id}"
    response = requests.patch(url, headers=db_hearders, json=data)
    # print("状态码:", response.status_code)
    # print("响应内容:", response.text)
    return response
