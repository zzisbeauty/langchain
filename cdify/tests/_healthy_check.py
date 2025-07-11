import os,sys,requests

# sys.path.append("/home/langchain-core-0.3.64")
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.append(project_root)

from cdify.tools import *


url = 'http://10.0.15.21/v1/info'
headers = {
    'Authorization': f'Bearer {secret_key}',
}

@timed_request  # = True  # 是否启用请求耗时统计
def get_info(url, headers):
    return requests.get(url, headers=headers)


if __name__ == "__main__":
    print("开始请求...")
    response = get_info(url, headers)
    print("状态码:", response.status_code)
    print("响应内容:", response.text)
