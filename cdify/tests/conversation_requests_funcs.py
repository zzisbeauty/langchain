import json, requests  

""" √ 
基于 requests api
直接使用 sdks/python-client/dify_client/client.py 11-22 中类似的 HTTP 请求逻辑，但不依赖 SDK；
这个实现完全基于 requests 库，避免了对 Dify SDK 的依赖，
    同时保持了与 sdks/python-client/dify_client/client.py:73-98 中 ChatClient.create_chat_message 相同的功能。
    可以保证对话有效展开，更轻量
"""

  
class DifyChatBot:  
    def __init__(self, api_key, base_url="http://10.30.30.97:8080/v1", user_id="test_user"):  
        """  
        初始化聊天机器人  
        :param api_key: 您的 Dify App API 密钥  
        :param base_url: 本地 Dify 服务地址  
        :param user_id: 用户标识符，用于区分不同用户的对话  
        """  
        self.api_key = api_key  
        self.base_url = base_url  
        self.user_id = user_id  
        self.conversation_id = None  # 用于存储和维护对话ID  
  
    def chat(self, message, streaming=True):  
        """  
        发送聊天消息并处理响应。  
        :param message: 用户输入的消息。  
        :param streaming: 是否使用流式响应。  
        :return: 机器人回复。  
        """  
        headers = {  
            "Authorization": f"Bearer {self.api_key}",  
            "Content-Type": "application/json"  
        }  
  
        data = {  
            "inputs": {},  
            "query": message,  
            "user": self.user_id,  
            "response_mode": "streaming" if streaming else "blocking",  
        }  
          
        # 如果存在 conversation_id，则传入以保持对话记忆  
        if self.conversation_id:  
            data["conversation_id"] = self.conversation_id  

        try:  
            response = requests.post(  
                f"{self.base_url}/chat-messages",  
                headers=headers,  
                json=data,  
                stream=streaming, # 启用流式传输  
                timeout=60  
            )  
  
            response.raise_for_status()  # 检查HTTP错误  
  
            if streaming:  
                return self._handle_streaming_response(response)  
            else:  
                return self._handle_blocking_response(response)  
  
        except requests.exceptions.RequestException as e:  
            print(f"请求错误: {e}")  
            if hasattr(e, 'response') and e.response is not None:  
                print(f"错误响应内容: {e.response.text}")  
            return f"错误: {str(e)}"  
        except Exception as e:  
            return f"未知错误: {str(e)}"  
  
    def _handle_streaming_response(self, response):  
        """处理流式响应"""  
        full_answer = ""  
        for line in response.iter_lines(decode_unicode=True):  
            if line and line.startswith('data: '):  
                data_str = line[6:]  
                if data_str.strip() and data_str != '[DONE]':  
                    try:  
                        data = json.loads(data_str)  
                          
                        # 提取并保存 conversation_id  
                        if 'conversation_id' in data and self.conversation_id is None:  
                            self.conversation_id = data['conversation_id']  
                            # print(f"Debug: 获取到新的 conversation_id: {self.conversation_id}") # 调试信息  
  
                        if data.get('event') == 'message':  
                            answer_chunk = data.get('answer', '')  
                            if answer_chunk:  
                                full_answer += answer_chunk  
                                print(answer_chunk, end='', flush=True)  
                        elif data.get('event') == 'message_end':  
                            print() # 换行  
                            break # 流结束  
                    except json.JSONDecodeError as e:  
                        print(f"JSON 解析错误: {e}, 数据: {data_str}")  
                        continue  
        return full_answer  
  
    def _handle_blocking_response(self, response):  
        """处理阻塞式响应"""  
        result = response.json()  
        # 提取并保存 conversation_id  
        if 'conversation_id' in result:  
            self.conversation_id = result['conversation_id']  
        return result.get('answer', '无回复')  
  
    def reset_conversation(self):  
        """重置对话，开始新的对话"""  
        self.conversation_id = None  
        print("对话已重置。")  
  
    def get_conversation_history(self):  
        """  
        获取当前会话的历史消息。  
        需要 conversation_id 存在才能获取。  
        """  
        if not self.conversation_id:  
            print("没有当前会话ID，无法获取历史记录。")  
            return []  
  
        headers = {  
            "Authorization": f"Bearer {self.api_key}",  
            "Content-Type": "application/json"  
        }  
        params = {  
            "user": self.user_id,  
            "conversation_id": self.conversation_id,  
            "limit": 20 # 默认获取最近20条消息  
        }  
          
        try:  
            # 调用 Dify 的 /messages API 获取历史消息  
            response = requests.get(  
                f"{self.base_url}/messages",  
                headers=headers,  
                params=params,  
                timeout=30  
            )  
            response.raise_for_status()  
            history_data = response.json().get('data', [])  
            return history_data  
        except requests.exceptions.RequestException as e:  
            print(f"获取对话历史失败: {e}")  
            if hasattr(e, 'response') and e.response is not None:  
                print(f"错误响应内容: {e.response.text}")  
            return []  
  
def main():  
    API_KEY = "app-cE8dOILnen8ELCQSAdaFsNYE"  # 替换为您的实际 App Key  
    BASE_URL = "http://10.30.30.97:8080/v1"  
    USER_ID = "unique_user_id_123" # 为每个用户设置一个唯一ID  
  
    chatbot = DifyChatBot(API_KEY, BASE_URL, USER_ID)  
  
    print("Dify 聊天机器人已启动！输入 'quit' 退出，输入 'reset' 重置对话，输入 'history' 查看历史。")  
    print("-" * 50)  
  
    while True:  
        user_input = input("\n您: ")  
  
        if user_input.lower() == 'quit':  
            break  
        elif user_input.lower() == 'reset':  
            chatbot.reset_conversation()  
            continue  
        elif user_input.lower() == 'history':  
            history = chatbot.get_conversation_history()  
            if history:  
                print("\n--- 对话历史 ---")  
                for msg in reversed(history): # 倒序显示，最新的在最下面  
                    print(f"用户: {msg.get('query')}")  
                    print(f"机器人: {msg.get('answer')}")  
                print("----------------")  
            else:  
                print("没有对话历史。")  
            continue  
          
        print("机器人: ", end='')  
        response = chatbot.chat(user_input, streaming=True)  
        # print(f"\n完整回复: {response}") # 如果需要查看完整回复，取消注释  
  
if __name__ == "__main__":  
    main()