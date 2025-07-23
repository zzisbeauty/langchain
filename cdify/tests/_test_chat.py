import requests  
import json, sys, os
  

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


from cdify.utils.config import *


def test_dify_chat_connection():  
    # 配置信息  
    API_KEY = secret_key
    BASE_URL = "http://10.30.30.97:8080/v1"  
      
    # 请求头  
    # headers = {  
    #     "Authorization": f"Bearer {API_KEY}",  
    #     "Content-Type": "application/json"  
    # }  
      
    # 请求数据  
    data = {  
        "inputs": {},  
        "query": "你好",  
        "user": "test_user",  
        "response_mode": "blocking"  # 使用阻塞模式，更容易调试  
    }  
      
    try:  
        # 发送请求  
        response = requests.post(  
            f"{BASE_URL}/chat-messages",  
            headers=app_headers,
            json=data,  
            timeout=30  
        )  
          
        print(f"状态码: {response.status_code}")  
        print(f"响应头: {response.headers}")  
        print(f"响应内容: {response.text}")  
          
        if response.status_code == 200:  
            result = response.json()  
            print(f"模型回复: {result.get('answer', '无回复')}")  
            return True  
        else:  
            print(f"请求失败: {response.status_code}")  
            return False  
              
    except Exception as e:  
        print(f"连接错误: {e}")  
        return False  
  
if __name__ == "__main__":  
    test_dify_chat_connection()