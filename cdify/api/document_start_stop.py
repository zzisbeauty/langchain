from flask import Blueprint, request  
import json  
import requests  
from cdify.utils.config import *  
from cdify.utils.decorators import timed_request  
  
# 创建文档启停的Blueprint  
doc_toggle = Blueprint('doc_toggle', __name__)  
  
@doc_toggle.route(BASE_URL + '/document/toggle', methods=['POST'])  
@timed_request  
def toggle_document_status():  
    """  
    文档启停接口  
    请求体格式：  
    {  
        "kb_id": "知识库ID",  
        "doc_id": "文档ID",   
        "action": "enable" 或 "disable"  
    }  
    """  
    data = request.get_data()  
    json_data = json.loads(data.decode("utf-8"))  
      
    dataset_id = json_data.get('kb_id', '')  
    document_id = json_data.get('doc_id', '')  
    action = json_data.get('action', '')  # enable 或 disable  
      
    # 验证必要参数  
    if not dataset_id or not document_id or not action:  
        return {  
            'code': -1,   
            'data': "",   
            'message': 'Missing required parameters: kb_id, doc_id, action'  
        }  
      
    if action not in ['enable', 'disable']:  
        return {  
            'code': -1,  
            'data': "",  
            'message': 'Invalid action. Must be "enable" or "disable"'  
        }  

    # 调用核心服务逻辑  
    from cdify.dify_client.document_toggle import doc_toggle_status  
    response = doc_toggle_status(dataset_id, document_id, action)  
      
    if response.get('success', False):  
        return {  
            'code': 0,   
            'data': "",   
            'message': f'Document {action} successful!'  
        }
    else:  
        return {
            'code': -1,   
            'data': "",
            'message': f'Document {action} failed: {response.get("error", "Unknown error")}'  
        }
