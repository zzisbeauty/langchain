import os
import sys
import json, requests


sys.path.append(r'E:\langchain-core-0.3.64')
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.append(project_root)


from cdify.tools import *






def requests_dataset_files_url(dataset_id, document_id):
    url = SERVER_BASE_URL + f"/datasets/{dataset_id}/documents/{document_id}/upload-file"
    response = requests.get(url, headers=db_hearders)
    print("状态码:", response.status_code)
    print("响应内容:", response.text)
    try:
        return response.text # 防止请求超时等意外错误
    except:
        return ''