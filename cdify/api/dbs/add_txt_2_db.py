import os
import sys
import json, requests


sys.path.append(r'E:\langchain-core-0.3.64')
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.append(project_root)


from cdify.tools import *


def requests_create_dataset_with_txt(db_id, data):    
    url = SERVER_BASE_URL + f'/datasets/{db_id}/document/create-by-text'
    response = requests.post(url, headers=db_hearders, json=data)
    print("状态码:", response.status_code)
    print("响应内容:", response.text)
    return response



if __name__ == "__main__":
    print("向数据库中导入数据集...")
    create_response = requests_create_dataset_with_txt()
    # print(create_response['message'])
    print("创建数据集响应:", json.dumps(create_response, indent=2, ensure_ascii=False))
