import os
import sys
import json, requests


sys.path.append(r'E:\langchain-core-0.3.64')
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.append(project_root)


from cdify.tools import *


def upload_file_with_metadata(db_id, file_name, file_path, data_json):
    # url = f'http://localhost:80/v1/datasets/{db_id}/document/create_by_file'
    url = SERVER_BASE_URL + f'/datasets/{db_id}/document/create_by_file'

    # 构造 multipart/form-data 请求
    files = {
        'data': (None, data_json, 'application/json'),
        'file': open(file_path, 'rb')
    }

    response = requests.post(url, headers=db_hearders_upload_files, files=files)
    print('Status Code:', response.status_code)
    print('Response:', response.text)
    return response
