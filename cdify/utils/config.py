import os
import sys
import json

# project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# if project_root not in sys.path:
#     sys.path.append(project_root)

def find_project_root(current_path, marker='.git'):
    """ 从当前路径向上查找，直到找到包含 marker（如 .git）的目录 """
    while current_path != os.path.dirname(current_path):
        if os.path.exists(os.path.join(current_path, marker)):
            return current_path
        current_path = os.path.dirname(current_path)
    return current_path  # 最后返回根目录

project_root = find_project_root(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)



# config info： 获取环境变量信息
import platform
from dotenv import load_dotenv

OS_NAME = platform.system()

if OS_NAME == "Windows":
    sys.path.append(r'E:\langchain-core-0.3.64')
    load_dotenv(r'E:\langchain-core-0.3.64\cdify\.env')
    ...
elif OS_NAME == "Linux":
    sys.path.append('/home/langchain-core-0.3.64')
    load_dotenv('/home/langchain/cdify/.env')
    ...
else:
    ... # 此时报错，不清楚操作系统类型


# base dify configs
MAX_LIMIT = 100 # # 对 dify 中的导出做一个统一的控制
BASE_URL = '/hanwei/v1' # base url in local api path



# hanwei windows dify server
SERVER_URL = 'http://10.30.30.97:8080'
SERVER_BASE_URL = 'http://10.30.30.97:8080/v1'
SERVER_BASE_URL_CONSOLE = "http://10.30.30.97:8080/console/api"
secret_key = 'app-b7VK5TkbDaT5DPxqz7oZbynF'
database_key = 'dataset-T2Hi8kmyqQCMmh6ZEtwOV2Xt'
console_key = "x44sVYhh1ET8cCVdAj90JdYeqgEpkeIAm6MwXjxSrlUpnY5CUTmsFvX9"


# server.15.12
...

# server other
...


# windows model server

# ollama embedding model config
embedding_model_config = "bge-m3:latest"
embedding_model_provider_config = 'langgenius/ollama/ollama'
# ollama rerank model config
# reranking_model_name_config = "linux6200/bge-reranker-v2-m3:latest"
# reranking_provider_name_config = "langgenius/ollama/ollama"

# windows xinference rerank model config   
reranking_model_name_config = "bge-reranker-base" # "bce-reranker-base_v1" 
reranking_provider_name_config = "xinference"





# APP 后端服务 API header 封装
db_hearders = {
    "Authorization": f"Bearer {database_key}",
    "Content-Type": "application/json",
}

db_hearders_console = {
    'Authorization': f'Bearer {console_key}', # 使用管理员密钥 - Windows dify
    "Content-Type": "application/json",
    "X-WORKSPACE-ID":"cb80d333-6ecf-434d-9268-e69ed89f4e6a"
}

db_hearders_upload_files = {
    "Authorization": f"Bearer {database_key}",
}

app_headers = {
    "Authorization": f"Bearer {secret_key}",
    "Content-Type": "application/json",
}
