# routes/chat_routes.py  
from flask import Blueprint, request  
from cdify.utils.config import BASE_URL
from cdify.utils.decorators import timed_request
  
chat_bp_history_with_convid = Blueprint('chat_history', __name__)  
  

# routes/chat_routes.py  
@chat_bp_history_with_convid.route(BASE_URL + '/conversation/history', methods=['GET'])  
@timed_request  
def get_conversation_history():  
    """获取指定会话的对话历史，支持导出为完整JSON格式"""  
    param = request.args.to_dict()  
    user_id = param.get('user_id', '')  
    conversation_id = param.get('conversation_id', '')  
    limit = int(param.get('limit', 20))  
    # 是当前页第一条消息的 ID，用于获取该消息之前创建的消息
    # 如果您设置 first_id=2，系统会查找 ID 为 2 的消息，然后返回在该消息时间之前创建的消息
    # 当 export_json = false 时，接口返回的是分页的会话消息列表，受 limit 和 first_id 控制，通常只返回一页（比如 20 条）
        # 普通查询：返回一页消息，结构简单，适合前端滚动加载。
    # 当 export_json=true 时，服务端会自动循环分页，把所有消息都查出来，
        # 组装成一个完整的 JSON 导出结构（比如包含导出时间、总条数等元信息），而不是只返回一页数据。
        # 此时 limit 参数会被忽略，服务端会自动用最大允许的 limit 分批抓取，直到所有消息都返回为止。
        # 导出模式：返回全部消息，结构更完整，适合一次性保存为 JSON 文件。
        # 导出全部消息时，必须分批抓取所有数据并合并，不能只靠一次 API 调用（因为 limit 最大 100），
        # 所以服务端代码会自动循环分页，最终返回所有消息的完整 JSON。
    first_id = param.get('first_id', '')  
    export_json = param.get('export_json', 'false').lower() == 'true'  # 新增导出参数  
      
    if not user_id:  
        return {  
            'code': -1,   
            'data': "",   
            'message': '请提供要查询的 user_id'  
        }  
      
    if not conversation_id:  
        return {  
            'code': -1,   
            'data': "",   
            'message': '请提供 conversation_id'  
        }  
    from cdify.dify_client.conv_with_convid_history import get_conversation_messages
    response = get_conversation_messages(  
        user_id=user_id,   
        conversation_id=conversation_id,   
        limit=limit,  
        first_id=first_id if first_id else None,  
        export_json=export_json  # 传递导出参数  
    )  
      
    if not response:  
        return {  
            'code': -1,   
            'data': "",   
            'message': 'Get conversation history failed!'  
        }  
      
    message = 'Export conversation data successful!' if export_json else 'Get conversation history successful!'  
    return {  
        'code': 0,   
        'data': response,   
        'message': message  
    }