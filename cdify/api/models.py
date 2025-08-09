from flask import Blueprint, request  
import json  
from cdify.utils.config import *  
from cdify.utils.decorators import timed_request  
  
# 创建模型选择的Blueprint  
model_select = Blueprint('model_select', __name__)  




@model_select.route(BASE_URL + '/llm/my_llms', methods=['GET'])  
@timed_request  
def get_available_models():  
    """  
    获取可用模型列表接口，请求参数：  
    model_type: 模型类型 (text-embedding, llm, rerank)  
    """  
    model_type = request.args.get('model_type', 'text-embedding')  
    from cdify.dify_client.model_service import get_models_by_type  
    response = get_models_by_type(model_type)  
    if response.get('success', False):  
        return {'code': 0, 'data': response.get('data', []), 'message': 'Get models successful!'}
    else:  
        return {'code': -1, 'data': [], 'message': f'Get models failed: {response.get("error", "Unknown error")}'}  




# @model_select.route(BASE_URL + '/user/set_tenant_info', methods=['GET'])
# @timed_request  
# def get_default_model():  
#     """  
#     获取默认模型接口  
#     请求参数：  
#     - model_type: 模型类型  
#     """  
#     model_type = request.args.get('model_type', 'text-embedding')  
#     from cdify.dify_client.model_service import get_default_model  
#     response = get_default_model(model_type)  
#     if response.get('success', False):  
#         return {'code': 0, 'data': response.get('data', {}), 'message': 'Get default model successful!'}  
#     else:  
#         return {'code': -1, 'data': {}, 'message': f'Get default model failed: {response.get("error", "Unknown error")}'}  



@model_select.route(BASE_URL + '/user/set_tenant_info', methods=['POST'])  
@timed_request  
def set_default_model():  
    """  
    设置默认模型接口; 请求参数
    {  
        "model_type": "text-embedding",  
        "provider": "zhipuai",  
        "model": "embedding-3"  
    }  
    """  
    data = request.get_data()  
    json_data = json.loads(data.decode("utf-8"))  

    model_type = json_data.get('model_type', '')  
    provider = json_data.get('provider', '')  
    model = json_data.get('model', '')

    if not model_type or not provider or not model:  
        return {'code': -1, 'data': "", 'message': 'Missing required parameters: model_type, provider, model'}  
    from cdify.dify_client.model_service import set_default_model  
    response = set_default_model(model_type, provider, model)  

    if response.get('success', False):  
        return {'code': 0,'data': "", 'message': 'Set default model successful!'}  
    else:  
        return {'code': -1, 'data': "",  'message': f'Set default model failed: {response.get("error", "Unknown error")}'}
