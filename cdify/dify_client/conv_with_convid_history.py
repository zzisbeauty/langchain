# services/dify_chat_service.py  
import json, time
import requests  
from cdify.utils.config import *
  

def get_conversation_messages(user_id: str, conversation_id: str, limit: int = 20, first_id: str = None, export_json: bool = False):  
    """ 获取指定会话的对话历史，支持导出完整JSON格式  
    """  
    try:            
        if export_json:  
            # 导出模式：忽略传入的limit，分批获取所有消息  
            return _get_all_messages_for_export(app_headers, user_id, conversation_id)  
        else:  
            # 普通查询模式：统一限制limit范围  
            normalized_limit = min(max(limit, 1), MAX_LIMIT)  # 确保在1-100范围内  
              
            params = {  
                "user": user_id,  
                "conversation_id": conversation_id,  
                "limit": normalized_limit  
            }  
              
            if first_id:  
                params["first_id"] = first_id  
              
            response = requests.get(
                url=SERVER_BASE_URL + '/messages',
                headers=app_headers,  
                params=params,  
                timeout=30  
            )  
              
            response.raise_for_status()  
            result = response.json()  
            messages = result.get('data', [])  
              
            return _format_history_data(user_id, conversation_id, messages, result, normalized_limit)  
          
    except requests.exceptions.RequestException as e:  
        print(f"获取对话历史失败: {e}")  
        if hasattr(e, 'response') and e.response is not None:  
            print(f"错误响应内容: {e.response.text}")  
        return None  
    except Exception as e:  
        print(f"获取对话历史时发生未知错误: {e}")  
        return None  
  
def _get_all_messages_for_export(headers: dict, user_id: str, conversation_id: str):  
    """分批获取所有消息用于导出，统一使用最大limit"""  
    all_messages = []  
    first_id = None  
    has_more = True  
      
    while has_more:  
        params = {  
            "user": user_id,  
            "conversation_id": conversation_id,  
            "limit": MAX_LIMIT  # 统一使用最大允许值  
        }  
          
        if first_id:  
            params["first_id"] = first_id  
          
        response = requests.get(  
            url=SERVER_BASE_URL + '/messages',
            headers=headers,  
            params=params,  
            timeout=30  
        )  
          
        response.raise_for_status()  
        result = response.json()  
        messages = result.get('data', [])  
          
        if messages:  
            all_messages.extend(messages)  
            # 设置下一页的 first_id 为当前页最后一条消息的 ID  
            first_id = messages[-1].get('id')  
            has_more = result.get('has_more', False)  
        else:  
            has_more = False  
      
    return _format_export_data(user_id, conversation_id, all_messages, {"has_more": False})
  


def _format_export_data(user_id: str, conversation_id: str, messages: list, result: dict):  
    """格式化导出数据"""  
    export_data = {  
        "export_info": {  
            "conversation_id": conversation_id,  
            "user_id": user_id,  
            "export_timestamp": int(time.time()),  
            "export_date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),  
            "total_messages": len(messages)  
        },  
        "conversation_data": {  
            "conversation_id": conversation_id,  
            "message_count": len(messages),  
            "has_more": result.get('has_more', False),  
            "messages": []  
        }
    } 
 
    # 格式化消息数据  
    for msg in messages:
        formatted_msg = {  
            "message_id": msg.get('id'),  
            "conversation_id": msg.get('conversation_id'),  
            "inputs": msg.get('inputs', {}),  
            "query": msg.get('query'),  
            "answer": msg.get('answer'),  
            "created_at": msg.get('created_at'),  
            "created_date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(msg.get('created_at', 0))),  
            "feedback": msg.get('feedback'),  
            "message_files": msg.get('message_files', []),  
            "retriever_resources": msg.get('retriever_resources', []),  
            "agent_thoughts": msg.get('agent_thoughts', [])  
        }  
        export_data["conversation_data"]["messages"].append(formatted_msg)  
      
    return export_data  
  
def _format_history_data(user_id: str, conversation_id: str, messages: list, result: dict, limit: int):  
    """格式化普通历史数据"""  
    formatted_messages = []  
      
    for msg in messages:  
        formatted_msg = {  
            "message_id": msg.get('id'),  
            "conversation_id": msg.get('conversation_id'),  
            "query": msg.get('query'),  
            "answer": msg.get('answer'),  
            "created_at": msg.get('created_at'),  
            "feedback": msg.get('feedback'),  
            "message_files": msg.get('message_files', []),  
            "retriever_resources": msg.get('retriever_resources', []),  
            "agent_thoughts": msg.get('agent_thoughts', [])  
        }  
        formatted_messages.append(formatted_msg)  
      
    return {  
        "conversation_id": conversation_id,  
        "user_id": user_id,  
        "messages": formatted_messages,  
        "has_more": result.get('has_more', False),  
        "limit": result.get('limit', limit),  
        "total_messages": len(formatted_messages)  
    }