# routes/chat_routes.py  
from flask import Blueprint, request, jsonify  
from cdify.utils.config import BASE_URL
from cdify.utils.decorators import timed_request


""" 基础对话接口。此接口方法可以被涵盖到 conversation_with_db_id 接口中"""

chat_bp = Blueprint('chat', __name__)  
  
@chat_bp.route(BASE_URL + '/conversation/completion', methods=['POST'])  
@timed_request  
def chat():  
    """统一的聊天接口 - 根据conversation_id自动判断新建或继续对话"""  
    data = request.get_json()  
      
    # 参数验证  
    user_id = data.get('user_id', '') if data else ''  
    message = data.get('message', '') if data else ''  
    conversation_id = data.get('conversation_id', '') if data else None 
    streaming = data.get('streaming', False) if data else False  
    if not user_id:
        return {'code': -1, 'data': "", 'message': '请提供要查询的 user_id'}  
    if not message:  
        return {'code': -1, 'data': "", 'message': '请提供要发送的 message'}  
  
    from cdify.dify_client.conv_with_client_requests import chat_with_dify
    response = chat_with_dify(  
        user_id=user_id,   
        message=message,   
        conversation_id=conversation_id,  
        streaming=streaming  
    )  
      
    if not response:  
        return {'code': -1, 'data': "", 'message': 'Chat failed!'}  
    return {'code': 0, 'data': response, 'message': 'Chat successful!'}  
  



@chat_bp.route(BASE_URL + '/conversationslist', methods=['GET'])    
@timed_request    
def get_conversations():    
    """ 获取用户对话列表 """
    param = request.args.to_dict()
    user_id = param.get('user_id', '') 
    limit = int(param.get('limit', 20))
    if not user_id:
        return {'code': -1, 'data': "", 'message': '请提供要查询的 user_id'}    

    from cdify.dify_client.conv_with_client_requests import get_user_conversations  
    response = get_user_conversations(user_id=user_id, limit=limit)
    if not response:    
        return {'code': -1, 'data': "", 'message': 'Get conversations failed!'}    
    return {    
        'code': 0, 'data': response, 'message': 'Get conversations successful!'}
