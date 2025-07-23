from flask import Blueprint, request, jsonify, Response  
from cdify.utils.config import *
from cdify.utils.decorators import timed_request


""" × 搁置方法
此代码基于 sdk 完成 dify 请求
但是 postman 请求一直没反应，有一些bug没有确定问题在哪里
"""


chat_bp = Blueprint('chat', __name__)

@chat_bp.route(BASE_URL + '/chat/create', methods=['POST'])  
@timed_request
def create_chat_session():  
    """创建新对话会话并保持监听状态"""  
    data = request.get_json()  
    user_id = data.get('user_id', '') if data else ''  
    initial_message = data.get('message', '') if data else ''  
      
    if not user_id:  
        return {  
            'code': -1,   
            'data': "",   
            'message': '请提供要查询的 user_id'  
        }  

    if not initial_message:  
        return {  
            'code': -1,   
            'data': "",   
            'message': '请提供初始消息内容'  
        }  
  
    from cdify.dify_client.conv_with_client_sdk import create_chat_session_with_listener
    response = create_chat_session_with_listener(user_id=user_id, message=initial_message)  

    if not response:  
        return {  
            'code': -1,   
            'data': "",   
            'message': 'Create chat session failed!'  
        }  
      
    # 返回流式响应，保持连接监听  
    def generate_stream():  
        for chunk in response:  
            yield f"data: {json.dumps(chunk)}\n\n"  
      
    return Response(generate_stream(), mimetype='text/event-stream')




@chat_bp.route(BASE_URL + '/conversations/list/<user_id>', methods=['GET'])  
@timed_request  
def get_user_conversation_ids(user_id):  
    """获取用户的所有会话ID列表"""  
    if not user_id:  
        return {  
            'code': -1,   
            'data': "",   
            'message': '请提供要查询的 user_id'  
        }  
      
    # 获取查询参数  
    param = request.args.to_dict()  
    limit = int(param.get('limit', 50))  
      
    from cdify.dify_client.conv_with_client_sdk import get_user_conversation_ids
    response = get_user_conversation_ids(user_id=user_id, limit=limit)  
      
    if not response:  
        return {  
            'code': -1,   
            'data': "",   
            'message': 'Get user conversation IDs failed!'  
        }  
      
    return {  
        'code': 0,   
        'data': response,   
        'message': 'Get user conversation IDs successful!'  
    }




@chat_bp.route(BASE_URL + '/conversation/export/<conversation_id>', methods=['GET'])  
@timed_request  
def export_conversation_data():  
    """导出指定conversation的完整对话数据"""  
    param = request.args.to_dict()  
    conversation_id = param.get('conversation_id', '')  
    user_id = param.get('user_id', '')  
      
    if not conversation_id:  
        return {  
            'code': -1,   
            'data': "",   
            'message': '请提供要导出的 conversation_id'  
        }  
      
    if not user_id:  
        return {  
            'code': -1,   
            'data': "",   
            'message': '请提供 user_id'  
        }  

    from cdify.dify_client.conv_with_client_sdk import export_conversation_json
    response = export_conversation_json(conversation_id=conversation_id, user_id=user_id)  
      
    if not response:  
        return {  
            'code': -1,   
            'data': "",   
            'message': 'Export conversation data failed!'  
        }  
      
    return {  
        'code': 0,   
        'data': response,   
        'message': 'Export conversation data successful!'  
    }