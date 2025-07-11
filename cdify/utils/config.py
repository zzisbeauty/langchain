import os
import sys
import json

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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


secret_key = os.getenv("APP_KEY")
database_key = os.getenv("DATABASE_KEY")


BASE_URL = '/hanwei/v1' # my local server base url
SERVER_BASE_URL = 'http://10.0.15.21/v1' # dify server base url


# ollama embedding model config
embedding_model_config = "bge-m3:latest"
embedding_model_provider_config = 'langgenius/ollama/ollama'

# ollama rerank model config
# reranking_model_name_config = "linux6200/bge-reranker-v2-m3:latest"
# reranking_provider_name_config = "langgenius/ollama/ollama"

# xinference rerank model config   
reranking_model_name_config = "bge-reranker-base" # "bce-reranker-base_v1" 
reranking_provider_name_config = "xinference"


db_hearders = {
    "Authorization": f"Bearer {database_key}",
    "Content-Type": "application/json",
}

db_hearders_upload_files = {
    "Authorization": f"Bearer {database_key}",
}

app_headers = {
    "Authorization": f"Bearer {secret_key}",
    "Content-Type": "application/json",
}