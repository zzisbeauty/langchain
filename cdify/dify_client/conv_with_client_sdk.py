import json,time
from dify_client import ChatClient  
from cdify.utils.config import *
 
  
class DifyChatService:  
    def __init__(self):  
        self.client = ChatClient(secret_key)  
        self.client.base_url = SERVER_BASE_URL

_dify_service = DifyChatService()   # 全局服务实例




def create_chat_session_with_listener(user_id: str, message: str):  
    """ 创建新对话会话并保持监听状态  
    :param user_id: 用户ID  
    :param message: 初始消息  
    :return: 生成器，持续监听用户消息  
    """  
    try:  
        # 创建新对话（不传入conversation_id强制创建新的）  
        response = _dify_service.client.create_chat_message(  
            inputs={},  
            query=message,  
            user=user_id,  
            response_mode="streaming",  
            conversation_id=None,  # 强制创建新对话  
            files=None  
        )  
          
        response.raise_for_status()  
        conversation_id = None  
          
        # 处理初始响应并获取conversation_id  
        for line in response.iter_lines(decode_unicode=True):  
            if line and line.startswith('data: '):  
                data_str = line[6:]  
                if data_str.strip() and data_str != '[DONE]':  
                    try:  
                        data = json.loads(data_str)  
                          
                        if 'conversation_id' in data and conversation_id is None:  
                            conversation_id = data['conversation_id']  
                            # 返回会话创建成功信息  
                            yield {  
                                "type": "session_created",  
                                "conversation_id": conversation_id,  
                                "user_id": user_id,  
                                "status": "listening"  
                            }  

                        event_type = data.get('event')  
                        if event_type == 'message':  
                            answer_chunk = data.get('answer', '')  
                            if answer_chunk:  
                                yield {  
                                    "type": "message_chunk",  
                                    "content": answer_chunk,  
                                    "conversation_id": conversation_id  
                                }  
                        elif event_type == 'message_end':  
                            yield {  
                                "type": "message_complete",  
                                "conversation_id": conversation_id,  
                                "status": "waiting_for_input"  
                            }  
                            break  
                              
                    except json.JSONDecodeError:  
                        continue  

        # 保持监听状态，等待后续消息
        while True:
            yield {  
                "type": "heartbeat",  
                "conversation_id": conversation_id,  
                "timestamp": int(time.time()),  
                "status": "listening"  
            }  
            time.sleep(10)  # 每10秒发送心跳  
              
    except Exception as e:  
        yield {  
            "type": "error",  
            "message": f"创建对话会话失败: {str(e)}"  
        }  
  
def get_user_conversation_ids(user_id: str, limit: int = 50):  
    """ 获取用户的所有会话ID列表  
    :param user_id: 用户ID  
    :param limit: 返回数量限制  
    :return: 会话ID列表  
    """  
    try:  
        response = _dify_service.client.get_conversations(  
            user=user_id,  
            limit=limit  
        )  
          
        response.raise_for_status()  
        result = response.json()  
          
        # 提取会话ID列表  
        conversations = result.get('data', [])  
        conversation_ids = [  
            {  
                "conversation_id": conv.get('id'),  
                "name": conv.get('name'),  
                "created_at": conv.get('created_at'),  
                "updated_at": conv.get('updated_at'),  
                "status": conv.get('status')  
            }  
            for conv in conversations  
        ]  
          
        return {  
            "user_id": user_id,  
            "conversation_ids": conversation_ids,  
            "total_count": len(conversation_ids),  
            "has_more": result.get('has_more', False)  
        }  
          
    except Exception as e:  
        print(f"获取用户会话ID列表失败: {str(e)}")  
        return None  
  
def export_conversation_json(conversation_id: str, user_id: str):  
    """ 导出指定conversation的完整对话数据  
    :param conversation_id: 对话ID  
    :param user_id: 用户ID  
    :return: 完整对话数据JSON  
    """  
    try:  
        # 获取对话中的所有消息  
        response = _dify_service.client.get_conversation_messages(  
            user=user_id,  
            conversation_id=conversation_id,  
            limit=1000  # 获取大量消息  
        )  
          
        response.raise_for_status()  
        result = response.json()  
          
        messages = result.get('data', [])  
          
        # 构建完整的对话数据结构  
        conversation_data = {  
            "conversation_id": conversation_id,  
            "user_id": user_id,  
            "export_timestamp": int(time.time()),  
            "message_count": len(messages),  
            "messages": [  
                {  
                    "message_id": msg.get('id'),  
                    "query": msg.get('query'),  
                    "answer": msg.get('answer'),  
                    "created_at": msg.get('created_at'),  
                    "feedback": msg.get('feedback'),  
                    "message_files": msg.get('message_files', []),  
                    "retriever_resources": msg.get('retriever_resources', [])  
                }  
                for msg in messages  
            ]  
        }  
          
        return conversation_data  
          
    except Exception as e:  
        print(f"导出对话数据失败: {str(e)}")  
        return None