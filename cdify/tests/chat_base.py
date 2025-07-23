import requests  
import json  
  
"""
测试有效
"""

def test_dify_chat_api_simple():  
    # 配置信息  
    API_KEY = "app-9JzVwDz5flC5wItHBBI1n7gC"  # <-- 请替换为您的实际 App Key (以 app- 开头)  
    BASE_URL = "http://10.30.30.97:8080/v1" # <-- 您的 Dify 服务地址  
  
    # 请求头  
    headers = {  
        "Authorization": f"Bearer {API_KEY}",  
        "Content-Type": "application/json"  
    }  
  
    # 请求数据  
    data = {  
        "inputs": {},  
        "query": "你好，Dify",  
        "user": "test_user_001", # 确保提供 user 参数  
        "response_mode": "blocking" # 使用阻塞模式，方便调试  
    }  
  
    print(f"正在尝试连接到: {BASE_URL}/chat-messages")  
    print(f"使用的 API Key (前5位): {API_KEY[:5]}...")  
  
    try:  
        # 发送 POST 请求  
        response = requests.post(  
            f"{BASE_URL}/chat-messages",  
            headers=headers,  
            json=data,  
            timeout=30 # 设置超时时间  
        )  
  
        print(f"\n状态码: {response.status_code}")  
        print(f"响应头: {response.headers}")  
        print(f"响应内容: {response.text}")  
  
        if response.status_code == 200:  
            try:  
                result = response.json()  
                print(f"\n模型回复: {result.get('answer', '无回复')}")  
                print("测试成功！")  
            except json.JSONDecodeError:  
                print("\n错误: 响应内容不是有效的 JSON。")  
        else:  
            print(f"\n请求失败，状态码: {response.status_code}")  
            print("请检查 API Key 是否正确，以及 Dify 后端日志。")  
  
    except requests.exceptions.ConnectionError as e:  
        print(f"\n连接错误: 无法连接到服务器。请检查 BASE_URL 是否正确且 Dify 服务正在运行。错误详情: {e}")  
    except requests.exceptions.Timeout:  
        print("\n连接超时: 请求在规定时间内未收到响应。")  
    except Exception as e:  
        print(f"\n发生未知错误: {e}")  
  
if __name__ == "__main__":  
    test_dify_chat_api_simple()