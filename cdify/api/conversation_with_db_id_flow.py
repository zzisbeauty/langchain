import sys, os

""" 无法更改工作流中已经设置的 db id 因此这种调用 app 接口的方式完成知识库检索对话的方案不通，但是这个代码过程是合理的
"""


# test info
# chat = SimpleDynamicChat("app-b7VK5TkbDaT5DPxqz7oZbynF")  
# dataset_id="e5176734-ead9-44cf-8bd6-124bc73564e0",  


def find_project_root(marker_files=('pyproject.toml', '.git', 'requirements.txt')):
    path = os.path.abspath(__file__)
    while path != os.path.dirname(path):
        if any(os.path.exists(os.path.join(path, marker)) for marker in marker_files):
            return path
        path = os.path.dirname(path)
    raise RuntimeError("Project root not found.")

project_root = find_project_root()
if project_root not in sys.path:
    sys.path.insert(0, project_root)


from cdify.utils.config import *


import requests, time
from flask_cors import CORS  
from flask import Flask, request, jsonify  

from typing import Dict, Optional, Any  
  
app = Flask(__name__)  
CORS(app)  
  
class ConversationManager:  
    """会话管理器，处理用户会话状态"""  
      
    def __init__(self):  
        # 存储格式: {user_id: {dataset_id: conversation_id}}  
        self.user_conversations: Dict[str, Dict[str, str]] = {}  
        # 存储会话详细信息: {conversation_id: {user_id, dataset_id, created_at}}  
        self.conversation_details: Dict[str, Dict[str, Any]] = {}  
      
    def get_conversation_id(self, user_id: str, dataset_id: str) -> Optional[str]:  
        """获取用户在特定知识库下的会话ID"""  
        return self.user_conversations.get(user_id, {}).get(dataset_id)  
      
    def create_conversation(self, user_id: str, dataset_id: str, conversation_id: str):  
        """创建新会话记录"""  
        if user_id not in self.user_conversations:  
            self.user_conversations[user_id] = {}  
          
        self.user_conversations[user_id][dataset_id] = conversation_id  
        self.conversation_details[conversation_id] = {  
            "user_id": user_id,  
            "dataset_id": dataset_id,  
            "created_at": time.time()  
        }  
      
    def get_user_conversations(self, user_id: str) -> Dict[str, str]:  
        """获取用户的所有会话"""  
        return self.user_conversations.get(user_id, {})  
  
class DifyAPIClient:  
    """Dify API客户端"""  
      
    def __init__(self, api_key: str, base_url: str = SERVER_BASE_URL):  
        self.api_key = api_key  
        self.base_url = base_url  
      
    def chat(self, query: str, user_id: str, dataset_id: str = None,   
             conversation_id: str = None) -> Dict[str, Any]:  
        """调用Dify聊天接口"""  
        url = f"{self.base_url}/chat-messages"  
          
        headers = {  
            "Authorization": f"Bearer {self.api_key}",  
            "Content-Type": "application/json"  
        }  
          
        data = {  
            "inputs": {},  
            "query": query,  
            "user": user_id,  
            "response_mode": "blocking"  
        }  
          
        # 动态传递知识库ID  
        if dataset_id:  
            data["inputs"]["dataset_id"] = dataset_id  
          
        # 继续会话  
        if conversation_id:  
            data["conversation_id"] = conversation_id  
          
        try:  
            response = requests.post(url, headers=headers, json=data)  
            response.raise_for_status()  
            return response.json()  
        except requests.exceptions.RequestException as e:  
            raise Exception(f"API调用失败: {str(e)}")  


# 全局实例  
conversation_manager = ConversationManager()  
dify_client = DifyAPIClient("app-b7VK5TkbDaT5DPxqz7oZbynF")  # 替换为实际API密钥  
  
@app.route('/api/chat', methods=['POST'])  
def chat():  
    """  
    聊天接口  
      
    请求参数:  
    - user_id: 用户ID (必填)  
    - query: 用户问题 (必填)  
    - dataset_id: 知识库ID (可选) , 有默认值
    - conversation_id: 会话ID (可选，用于继续对话)  
    """  
    try:  
        data = request.get_json()  
          
        # 参数验证  
        user_id = data.get('user_id')  
        query = data.get('query')  
        dataset_id = data.get('dataset_id', 'e5176734-ead9-44cf-8bd6-124bc73564e0')  
        conversation_id = data.get('conversation_id')  
        if not user_id:  
            return jsonify({"error": "user_id是必填参数"}), 400  
        if not query:  
            return jsonify({"error": "query是必填参数"}), 400  
          
        # 会话管理逻辑  
        current_conversation_id = None  
          
        if conversation_id:  
            # 验证会话ID是否属于当前用户和知识库  
            conv_details = conversation_manager.conversation_details.get(conversation_id)  
            if conv_details and conv_details['user_id'] == user_id:  
                if not dataset_id or conv_details['dataset_id'] == dataset_id:  
                    current_conversation_id = conversation_id  
          
        # 如果没有有效的会话ID，检查是否需要创建新会话  
        if not current_conversation_id and dataset_id:  
            existing_conv_id = conversation_manager.get_conversation_id(user_id, dataset_id)  
            if existing_conv_id:  
                current_conversation_id = existing_conv_id  
          
        # 调用Dify API  
        result = dify_client.chat(  
            query=query,  
            user_id=user_id,  
            dataset_id=dataset_id,  
            conversation_id=current_conversation_id  
        )
          
        # 处理新会话ID  
        new_conversation_id = result.get('conversation_id')  
        if new_conversation_id and dataset_id:  
            if new_conversation_id != current_conversation_id:  
                # 创建新会话记录  
                conversation_manager.create_conversation(user_id, dataset_id, new_conversation_id)  
          
        return jsonify({  
            "success": True,  
            "data": {  
                "answer": result.get('answer', ''),  
                "conversation_id": new_conversation_id,  
                "user_id": user_id,  
                "dataset_id": dataset_id,  
                "message_id": result.get('message_id'),  
                "metadata": result.get('metadata', {})  
            }  
        })  
          
    except Exception as e:  
        return jsonify({  
            "success": False,  
            "error": str(e)  
        }), 500  




@app.route('/api/conversations/<conversation_id>/reset', methods=['POST'])  
def reset_conversation(conversation_id):  
    """重置会话（开始新对话）"""  
    try:  
        data = request.get_json()  
        user_id = data.get('user_id')  
          
        if not user_id:  
            return jsonify({"error": "user_id是必填参数"}), 400  
          
        # 验证会话所有权  
        conv_details = conversation_manager.conversation_details.get(conversation_id)  
        if not conv_details or conv_details['user_id'] != user_id:  
            return jsonify({"error": "会话不存在或无权限"}), 403  
          
        # 删除会话记录，下次对话将创建新会话  
        dataset_id = conv_details['dataset_id']  
        if user_id in conversation_manager.user_conversations:  
            if dataset_id in conversation_manager.user_conversations[user_id]:  
                del conversation_manager.user_conversations[user_id][dataset_id]  
          
        if conversation_id in conversation_manager.conversation_details:  
            del conversation_manager.conversation_details[conversation_id]  
          
        return jsonify({  
            "success": True,  
            "message": "会话已重置"  
        })  
          
    except Exception as e:  
        return jsonify({  
            "success": False,  
            "error": str(e)  
        }), 500  


@app.route('/health', methods=['GET'])  
def health_check():  
    """健康检查"""  
    return jsonify({  
        "status": "ok",  
        "message": "Dify Chat Server运行正常"  
    })  
  
if __name__ == '__main__':  
    print("启动Dify Chat Server...")  
    print("请确保已设置正确的API密钥")  
    app.run(debug=True, host='0.0.0.0', port=5627)