import json,time, requests
# from dify_client import ChatClient
from cdify.utils.config import *
 
  
# class DifyChatService:  
#     def __init__(self):  
#         self.client = ChatClient(secret_key)  
#         self.client.base_url = SERVER_BASE_URL

# _dify_service = DifyChatService()   # 全局服务实例


def chat_with_dify(user_id: str, message: str, conversation_id: str = None, streaming: bool = False):  
    """ 统一的 Dify 聊天服务 - 根据conversation_id自动判断新建或继续对话  
    :param user_id: 用户ID  
    :param message: 用户消息  
    :param conversation_id: 对话ID，None则创建新对话，有值则继续对话  
    :param streaming: 是否流式响应  
    :return: 对话响应数据  
    """  
    try:  
        # 构建请求数据  
        data = {  
            "inputs": {},  
            "query": message,  
            "user": user_id,  
            "response_mode": "streaming" if streaming else "blocking"  
        }

        # 根据conversation_id判断是否继续对话  
        if conversation_id:  
            data["conversation_id"] = conversation_id

        response = requests.post(  
            url = SERVER_BASE_URL + "/chat-messages",  
            headers=app_headers,  
            json=data,  
            stream=streaming,  
            timeout=300
        )  

        response.raise_for_status()  
          
        if streaming:  
            return _handle_streaming_response(response)  
        else:  
            result = response.json()  
            return {  
                "conversation_id": result.get('conversation_id'),  
                "answer": result.get('answer'),  
                "message_id": result.get('message_id'),  
                "is_new_conversation": conversation_id is None  
            }  

    except Exception as e:  
        print(f"聊天失败: {str(e)}")  
        return None  
  
def get_user_conversations(user_id: str, limit: int = 20):  
    """ 获取用户对话列表 
    """  
    try:          
        params = {  
            "user": user_id,  
            "limit": limit  
        }  
          
        response = requests.get(  
            url= SERVER_BASE_URL + "/conversations",  
            headers=app_headers,  
            params=params,  
            timeout=30  
        )  
          
        response.raise_for_status()  
        result = response.json()  
          
        return {  
            "user_id": user_id,  
            "conversations": result.get('data', []),  
            "has_more": result.get('has_more', False),  
            "limit": limit  
        }  
          
    except Exception as e:  
        print(f"获取对话列表失败: {str(e)}")  
        return None  
  
def _handle_streaming_response(response):  
    """ 处理流式响应 
    """  
    conversation_id = None  
    full_answer = ""  
      
    try:  
        for line in response.iter_lines(decode_unicode=True):  
            if line and line.startswith('data: '):  
                data_str = line[6:]  
                if data_str.strip() and data_str != '[DONE]':  
                    try:  
                        data = json.loads(data_str)  
                          
                        if 'conversation_id' in data and conversation_id is None:  
                            conversation_id = data['conversation_id']  
                          
                        event_type = data.get('event')  
                        if event_type == 'message':  
                            answer_chunk = data.get('answer', '')  
                            if answer_chunk:  
                                full_answer += answer_chunk  
                        elif event_type == 'message_end':  
                            break  
                        elif event_type == 'error':  
                            return None  
                              
                    except json.JSONDecodeError:  
                        continue  
          
        return {  
            "conversation_id": conversation_id,  
            "answer": full_answer,  
            "streaming": True  
        }  
          
    except Exception as e:  
        print(f"流式响应处理失败: {str(e)}")  
        return None