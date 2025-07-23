import json  
import requests  
from typing import List, Optional, Dict, Any 
from cdify.utils.config import *
from cdify.utils.decorators import timed_request
from flask import Blueprint, request  



""" 基于知识库的对话接口 """


# routes/dynamic_knowledge_chat_routes.py  
dynamic_chat_bp = Blueprint('dynamic_chat', __name__)  
# BASE_URL = '/api/v1'  
  
@dynamic_chat_bp.route(BASE_URL + '/conversation/completion', methods=['POST'])  
@timed_request  
def chat_with_dynamic_dataset():  
    """动态指定知识库的聊天接口"""  
    data = request.get_json()  
    user_id = data.get('user_id', '')  
    message = data.get('message', '')  
    dataset_id = data.get('dataset_id', '')  # 动态指定的知识库ID  
    conversation_id = data.get('conversation_id')  
    streaming = data.get('streaming', False)  

    if not user_id:  
        return {'code': -1, 'data': "", 'message': '请提供 user_id'}  
      
    if not message:  
        return {'code': -1, 'data': "", 'message': '请提供 message'}  
      
    if not dataset_id:  
        return {'code': -1, 'data': "", 'message': '请提供 dataset_id'}  
    
    from cdify.dify_client.conv_with_dynamic_knowledge_chat_service import DynamicKnowledgeChatService
    chat_service = DynamicKnowledgeChatService()  

    response = chat_service.chat_with_specified_dataset(  
        user_id=user_id,  
        message=message,  
        dataset_id=dataset_id,  
        conversation_id=conversation_id,  
        streaming=streaming  
    )  
      
    if not response:  
        return {'code': -1, 'data': "", 'message': 'Chat with dataset failed!'}        
    return {'code': 0, 'data': response, 'message': 'Chat with dataset successful!'}
