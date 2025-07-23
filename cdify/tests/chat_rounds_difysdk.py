import json  
import uuid  
from dify_client import ChatClient, DifyClient # 导入 DifyClient 用于设置 base_url  
  
class DifyChatBotSDK:  
    def __init__(self, api_key: str, base_url: str = "http://10.30.30.97:8080/v1"):  
        """  
        初始化聊天机器人  
        :param api_key: 您的 Dify App API 密钥 (以 app- 开头)  
        :param base_url: 本地 Dify 服务地址  
        """  
        # ChatClient 继承自 DifyClient，可以直接设置 base_url  
        self.client = ChatClient(api_key)# [3]
        self.client.base_url = base_url #[4]
        self.user_id = str(uuid.uuid4()) # 为每个会话生成一个唯一的 user_id [5](#16-4) </cite>  
        self.conversation_id = None # 用于存储和维护对话ID [6](#16-5) </cite>  


class DifyChatBotSDK:  
    def __init__(self, api_key: str, base_url: str = "http://10.30.30.97:8080/v1"):  
        """  
        初始化聊天机器人  
        :param api_key: 您的 Dify App API 密钥 (以 app- 开头)  
        :param base_url: 本地 Dify 服务地址  
        """  
        self.client = ChatClient(api_key)  
        self.client.base_url = base_url  
        self.user_id = str(uuid.uuid4())  
        self.conversation_id = None

    def chat(self, message: str, streaming: bool = True) -> str:  
        """  
        发送聊天消息并处理响应。  
        :param message: 用户输入的消息。  
        :param streaming: 是否使用流式响应。  
        :return: 机器人回复。  
        """
        try:  
            response = self.client.create_chat_message(  
                inputs={}, # 应用定义的变量，此处为空 [7](#16-6) </cite>  
                query=message, # 用户输入内容 [8](#16-7) </cite>  
                user=self.user_id, # 用户标识符 [5](#16-4) </cite>  
                response_mode="streaming" if streaming else "blocking", # [9](#16-8) </cite>  
                conversation_id=self.conversation_id, # 传入对话ID以保持记忆 [10](#16-9) </cite>  
                files=None # 如果需要上传文件，可以在这里传入文件列表 [11](#16-10) </cite>  
            )  
            response.raise_for_status() # 检查 HTTP 错误状态码  
            if streaming:  
                return self._handle_streaming_response(response)  
            else:  
                return self._handle_blocking_response(response)  
        except Exception as e:  
            return f"错误: {str(e)}"  
  
    def _handle_streaming_response(self, response) -> str:  
        """处理流式响应"""  
        full_answer = ""  
        for line in response.iter_lines(decode_unicode=True):  
            if line and line.startswith('data: '):  
                data_str = line[6:] # 移除 'data: ' 前缀  
                if data_str.strip() and data_str != '[DONE]':  
                    try:  
                        data = json.loads(data_str)  
                          
                        # 提取并保存 conversation_id  
                        if 'conversation_id' in data and self.conversation_id is None:  
                            self.conversation_id = data['conversation_id']# [12](#16-11) </cite>  
  
                        if data.get('event') == 'message': # 处理消息事件 [13](#16-12) </cite>  
                            answer_chunk = data.get('answer', '')  
                            if answer_chunk:  
                                full_answer += answer_chunk  
                                print(answer_chunk, end='', flush=True)  
                        elif data.get('event') == 'message_end': # 消息流结束事件 [14](#16-13) </cite>  
                            print() # 换行  
                            break # 流结束  
                    except json.JSONDecodeError as e:  
                        print(f"JSON 解析错误: {e}, 数据: {data_str}")  
                        continue  
        return full_answer  
  
    def _handle_blocking_response(self, response) -> str:  
        """处理阻塞式响应"""  
        result = response.json()  
        # 提取并保存 conversation_id
        if 'conversation_id' in result:  
            self.conversation_id = result['conversation_id'] #[12](#16-11) </cite>  
        return result.get('answer', '无回复')  
  
    def reset_conversation(self):  
        """重置对话，开始新的对话"""  
        self.conversation_id = None  
        print("对话已重置。")  
  
    def get_conversation_history(self) -> list:  
        """  
        获取当前会话的历史消息。  
        需要 conversation_id 存在才能获取。  
        """  
        if not self.conversation_id:  
            print("没有当前会话ID，无法获取历史记录。")  
            return []  
        try:  
            # 使用 SDK 的 get_conversation_messages 方法 [15](#16-14) </cite>  
            response = self.client.get_conversation_messages(  
                user=self.user_id,  
                conversation_id=self.conversation_id,  
                limit=20 # 默认获取最近20条消息  
            )  
            response.raise_for_status()  
            history_data = response.json().get('data', [])  
            return history_data  
        except Exception as e:  
            print(f"获取对话历史失败: {e}")  
            return []  
  
def main():  
    API_KEY = "app-9JzVwDz5flC5wItHBBI1n7gC" # 替换为您的实际 App Key (以 app- 开头)  
    BASE_URL = "http://10.30.30.97:8080/v1" # 您的本地 Dify 服务地址  
  
    chatbot = DifyChatBotSDK(API_KEY, BASE_URL)  
  
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
  
if __name__ == "__main__":  
    main()