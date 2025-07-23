import json  
import uuid  
from flask import Flask, request, jsonify, Response  
from dify_client import ChatClient  
import requests  
  
app = Flask(__name__)  


class DifyChatService:  
    def __init__(self, api_key: str, base_url: str):  
        """  
        初始化 Dify 聊天服务  
        :param api_key: Dify App API 密钥  
        :param base_url: Dify 服务地址  
        """  
        self.client = ChatClient(api_key)  
        self.client.base_url = base_url  

    def create_new_chat(self, user_id: str, message: str, streaming: bool = True):  
        """
        创建新的对话（不传入 conversation_id，强制创建新对话）  
        :param user_id: 用户ID  
        :param message: 用户消息  
        :param streaming: 是否使用流式响应  
        :return: 聊天响应  
        """  
        try:  
            response = self.client.create_chat_message(  
                inputs={},  
                query=message,  
                user=user_id,  
                response_mode="streaming" if streaming else "blocking",  
                conversation_id=None,  # 不传入 conversation_id，强制创建新对话  
                files=None  
            )  
            response.raise_for_status()  
            return response  
        except Exception as e:  
            raise Exception(f"创建对话失败: {str(e)}")  

    def get_user_conversations(self, user_id: str, limit: int = 20):  
        """  
        获取用户的所有对话列表  
        :param user_id: 用户ID  
        :param limit: 返回的对话数量限制  
        :return: 对话列表  
        """  
        try:  
            response = self.client.get_conversations(  
                user=user_id,  
                limit=limit  
            )  
            response.raise_for_status()  
            return response.json()  
        except Exception as e:  
            raise Exception(f"获取对话列表失败: {str(e)}")  


# 配置 Dify 服务  
API_KEY = "your_app_key_here"  # 替换为您的实际 App Key  
BASE_URL = "http://10.30.30.97:8080/v1"  # 替换为您的 Dify 服务地址  
  
dify_service = DifyChatService(API_KEY, BASE_URL)  
  
@app.route('/chat/new', methods=['POST'])  
def create_new_chat():  
    """  
    创建新对话的 API 接口  
    POST /chat/new  
    {  
        "user_id": "用户ID",  
        "message": "用户消息",  
        "streaming": true/false (可选，默认true)  
    }  
    """  
    try:  
        data = request.get_json()  
          
        # 验证必需参数  
        if not data or 'user_id' not in data or 'message' not in data:  
            return jsonify({  
                "error": "缺少必需参数",  
                "message": "请提供 user_id 和 message 参数"  
            }), 400  
          
        user_id = data['user_id']  
        message = data['message']  
        streaming = data.get('streaming', True)  
          
        # 调用 Dify 服务创建新对话  
        response = dify_service.create_new_chat(user_id, message, streaming)  
          
        if streaming:  
            # 流式响应处理  
            def generate():  
                conversation_id = None  
                full_answer = ""  
                  
                for line in response.iter_lines(decode_unicode=True):  
                    if line and line.startswith('data: '):  
                        data_str = line[6:]  
                        if data_str.strip() and data_str != '[DONE]':  
                            try:  
                                data = json.loads(data_str)  
                                  
                                # 提取 conversation_id  
                                if 'conversation_id' in data and conversation_id is None:  
                                    conversation_id = data['conversation_id']  
                                  
                                event_type = data.get('event')  
                                if event_type == 'message':  
                                    answer_chunk = data.get('answer', '')  
                                    if answer_chunk:  
                                        full_answer += answer_chunk  
                                        yield f"data: {json.dumps({'type': 'message', 'content': answer_chunk})}\n\n"  
                                elif event_type == 'message_end':  
                                    yield f"data: {json.dumps({'type': 'end', 'conversation_id': conversation_id, 'full_answer': full_answer})}\n\n"  
                                    break  
                                elif event_type == 'error':  
                                    error_msg = data.get('message', '未知错误')  
                                    yield f"data: {json.dumps({'type': 'error', 'message': error_msg})}\n\n"  
                                    break  
                            except json.JSONDecodeError:  
                                continue  
              
            return Response(generate(), mimetype='text/event-stream')  
        else:  
            # 阻塞式响应处理  
            result = response.json()  
            return jsonify({  
                "success": True,  
                "conversation_id": result.get('conversation_id'),  
                "answer": result.get('answer'),  
                "message_id": result.get('message_id')  
            })  
      
    except Exception as e:  
        return jsonify({  
            "error": "服务器错误",  
            "message": str(e)  
        }), 500  
  
@app.route('/conversations/<user_id>', methods=['GET'])  
def get_user_conversations(user_id):  
    """  
    获取用户对话列表的 API 接口  
    GET /conversations/<user_id>?limit=20  
    """  
    try:  
        # 获取查询参数  
        limit = request.args.get('limit', 20, type=int)  
          
        # 验证参数  
        if limit < 1 or limit > 100:  
            return jsonify({  
                "error": "参数错误",  
                "message": "limit 参数必须在 1-100 之间"  
            }), 400  
          
        # 调用 Dify 服务获取对话列表  
        conversations = dify_service.get_user_conversations(user_id, limit)  
          
        return jsonify({  
            "success": True,  
            "user_id": user_id,  
            "conversations": conversations.get('data', []),  
            "has_more": conversations.get('has_more', False),  
            "limit": conversations.get('limit', limit)  
        })  
      
    except Exception as e:  
        return jsonify({  
            "error": "服务器错误",  
            "message": str(e)  
        }), 500  



@app.route('/health', methods=['GET'])  
def health_check():  
    """健康检查接口"""  
    return jsonify({  
        "status": "healthy",  
        "service": "Dify Chat API"  
    })  
  
if __name__ == '__main__':  
    app.run(debug=True, host='0.0.0.0', port=5000)