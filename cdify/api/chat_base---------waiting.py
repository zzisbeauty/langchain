from flask import Blueprint, request
from cdify.utils.config import *
from cdify.utils.decorators import timed_request

chat_base = Blueprint('chat_base', __name__)

"""
todo 基础对话功能 - 待完成
"""


@chat_base.route(BASE_URL + '/chat', methods=['POST'])
@timed_request
def start_chat():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))

    # params check
    user_id = json_data.get('user_id', '') # hanwei-cdify
    if not user_id:
        return {'status_code': -1, 'info': 'No user_id provided', 'data': "",}
    
    conversation_id = json_data.get('conversation_id','')
    # todo 这里需要新增对话轮次的判断，保证 conversation id 的信息是有效的
    # json_data['conversation_id'] = ...
    
    query = json_data.get('query', '')
    # todo 这里需要修正，新增一下判断轮次后，对话默认信息的设定
    query = "你好。你是谁？" if not query else ...
    # json_data['query'] = ...


    from cdify.dify_client.chat_base import start_chat
    response = start_chat(data_new=json_data)
    if response.status_code != 200:
        return {'code': -1, 'data': "", 'message': '可能是服务器或网络异常，请检查网络或者服务器GPU模型是否正常运行！'}

    response = json.loads(response.text)  # chat server 完整返回的所有字段请参考 tools.py 中的 chat_return_all_columns
    message_id = response.get('message_id')
    conversation_id = response.get('conversation_id')
    try:
        answer = json.loads(response.get('answer'))    
    except json.JSONDecodeError:
        ...
    return {
        'data': {
            'conversation_id': conversation_id,
            'message_id': message_id,
            'answer': answer
        },
        'status_code': 0,
        'info': 'request chat info successful!'
    }