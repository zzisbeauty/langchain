import os
import sys
import json, requests


sys.path.append(r'E:\langchain-core-0.3.64')
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.append(project_root)


from cdify.tools import *


""" https://zhuanlan.zhihu.com/p/1918706240747451513 """

def upload_file(local_file_path, api_key):
    file_type = 'application/octet-stream'  # 可根据实际类型调整
    url = f'{SERVER_BASE_URL}/files/upload'
    headers = {'Authorization': f'Bearer {api_key}'}
    with open(local_file_path, 'rb') as file:
        files = {'file': (os.path.basename(local_file_path), file, file_type)}
        data = {'user': 'difyAdmin'}
        response = requests.post(url, headers=headers, files=files, data=data)
    if response.status_code == 201:
        print(f"[上传成功] {local_file_path}")
        return response.json()['id']
    else:
        print(f"[上传失败] {local_file_path}，状态码: {response.status_code}")
        return None