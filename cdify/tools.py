import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.append(project_root)

import platform

OS_NAME = platform.system()

from dotenv import load_dotenv



# config info
if OS_NAME == "Windows":
    # print("Windows")
    sys.path.append(r'E:\langchain-core-0.3.64')
    # LOAD ENV CONFIG AND SETTINGS
    load_dotenv(r'E:\langchain-core-0.3.64\cdify\.env')
    ...
elif OS_NAME == "Linux":
    sys.path.append('/home/langchain-core-0.3.64')
    # LOAD ENV CONFIG AND SETTINGS
    load_dotenv('/home/langchain-core-0.3.64/cdify/.env')
    ...
    # print("Linux")
else:
    ...
    # print(f"Other OS: {OS_NAME}")


secret_key = os.getenv("APP_KEY")
database_key = os.getenv("DATABASE_KEY")



# CONFIG SETTINGS
BASE_URL = '/hanwei'
SERVER_BASE_URL = 'http://10.0.15.21/v1'


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



# 接口计时
import time
from functools import wraps

def timed_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        response = func(*args, **kwargs)
        duration = time.time() - start
        print(f"请求耗时: {duration:.3f} 秒")
        return response
    return wrapper



from pathlib import Path

def get_filename(file_path):
    return Path(file_path).name


'''shell    
curl --location --request POST 'http://localhost:80/v1/datasets/25ca2669-42cc-4e06-8de2-b7bb009c56a4/document/create_by_file' \
--header 'Authorization: Bearer dataset-BF2ihbySxTuftWOJnZMBTDTH' \
--form 'data={
  "indexing_technique": "high_quality",
  "process_rule": {
    "rules": {
      "pre_processing_rules": [
        {"id": "remove_extra_spaces", "enabled": true},
        {"id": "remove_urls_emails", "enabled": true}
      ],
      "segmentation": {
        "separator": "###",
        "max_tokens": 500
      }
    },
    "mode": "custom"
  }
};type=application/json' \
--form 'file=@"/home/git/files/长文-2.txt"'
'''