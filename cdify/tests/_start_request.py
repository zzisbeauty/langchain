import os,sys,requests

# sys.path.append("/home/langchain-core-0.3.64")
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.append(project_root)

from cdify.tools import *

# API 发起会话 without conversation_id
chat_url = "http://10.0.15.21/v1/chat-messages"
headers = {
    "Authorization": f"Bearer {secret_key}",
    "Content-Type": "application/json",  
}

data = {
    "inputs": {},
    # "query": "What are the specs of the iPhone 13 Pro Max?",
    "query": "你好，CDify！请帮我查询一下iPhone 13 Pro Max的规格。",
    "response_mode": "blocking",  # "streaming" or "blocking"
    "conversation_id": "",
    "user": "hanwei-cdify",
    # "files": [
    #     {
    #         "type": "image",
    #         "transfer_method": "remote_url",
    #         "url": "https://cloud.dify.ai/logo/logo-site.png"
    #     }
    # ]
}

@timed_request # = True  # 是否启用请求耗时统计
def chat_request():
    """发送聊天请求"""
    response = requests.post(chat_url, headers=headers, json=data)
    print("状态码:", response.status_code)
    print("响应内容:", response.text)
    return response
    


# API 获取下一轮会话建议列表
# user = "hanwei-cdify-apipost-09:09"
# message_id = "9728d589-fdbf-47cf-9760-721a4f667353"
# url = f"http://10.0.15.21/v1/messages/9728d589-fdbf-47cf-9760-721a4f667353/suggested?user=hanwei-cdify-apipost-09:09"



# API 获取会话ID下的对话历史
url = "http://10.0.15.21/v1/messages?user=hanwei-cdify-apipost-09:09&conversation_id=7c8645a3-98d1-4555-9888-f76513752671"
headers = {
    "Authorization": "Bearer app-sumagDtdGpZUYfcAltQxENk7",  # 替换 {api_key} 为你的真实 API Key
}
@timed_request
def get_conversation_id():
    """获取会话ID"""
    response = requests.get(url, headers=headers)
    print("状态码:", response.status_code)
    print("响应内容:", response.text)
    return response.json()


if __name__ == "__main__":
    print("开始请求...")
    response = chat_request()
    # response = get_conversation_id()

    if response.status_code == 200:
        print("请求成功, 响应内容:", response)
    else:
        print("请求失败，状态码:", response.status_code)
