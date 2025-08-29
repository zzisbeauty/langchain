# routes/chat_routes.py 
import requests
from flask import Blueprint, request, jsonify  
from cdify.utils.config import BASE_URL
from cdify.utils.decorators import timed_request
import json  

""" 对话接口 with DB ID 
"""

chat_db = Blueprint('chatdb', __name__)  


@chat_db.route(BASE_URL + '/conversation/completion_db', methods=['POST'])  
@timed_request  
def completion_db():  
    """RAG增强的对话接口 - 支持动态知识库选择, kb_id 每次请求都要传入； conversation_id 必要时每次都传入"""  
    try:
        data = request.get_json()  
        # print(data)
        user_id = data.get('user_id', '') if data else ''  
        message = data.get('message', '') if data else ''  
        kb_id = data.get('kb_id', '') if data else None  # 知识库ID  
        streaming = data.get('streaming', True) if data else False  

        if not user_id:  
            return jsonify({"error": "user_id是必填参数"}), 400  
        if not message:  
            return jsonify({"error": "message是必填参数"}), 400  

        context = ""
        if kb_id: # 1. 如果指定了知识库，先进行检索
            context = retrieve_knowledge_internal(kb_id, message)
        print('context: ', context)

        if context: # 2. 格式化prompt  
            formatted_message = format_prompt_with_context(context, message)  
        else:  
            formatted_message = message  
          
        # 3. 调用内部对话接口  -  conversation id
        conversation_id = data.get('conversation_id', '') if data else None
        chat_data = {  
            "user_id": user_id,  
            "message": formatted_message,
            "streaming": streaming
        }  
          
        if conversation_id:  
            chat_data["conversation_id"] = conversation_id  
          
        # 调用您现有的对话接口  
        chat_response = call_internal_chat_api(chat_data)  
          
        # 4. 添加RAG相关信息到返回结果  
        if isinstance(chat_response, dict):  
            chat_response["rag_info"] = {  
                "kb_id": kb_id,  
                "context_used": bool(context),  
                "context_length": len(context) if context else 0  
            }  
          
        return jsonify(chat_response)  

    except Exception as e:  
        return jsonify({"error": f"服务错误: {str(e)}"}), 500  



def retrieve_knowledge_internal(kb_id: str, question: str) -> str:  
    """内部调用检索接口"""  
    try:  
        # 调用您现有的检索接口  
        retrieval_data = {"kb_id": kb_id, "question": question}  
        response = requests.post(f"http://10.0.15.21:5627{BASE_URL}/chunk/retrieval_test", json=retrieval_data)  
        response = json.loads(response.text)
        context = ''
        if response['code'] == 0:
            datas = response['data']['records']
            for idx, data in enumerate(datas):
                context += str(idx) + ". " + data['content'] + "\n"
        return context
    except Exception as e:  
        print(f"检索失败: {str(e)}")  
        return ""  


def format_prompt_with_context(context: str, user_message: str) -> str:  
    """格式化prompt"""  
    prompt_template = f"""请根据如下基础知识信息： {context} ，完成对用户问题的回答。
                          如果没有从基础知识信息中找到与用户问题相关的信息，就基于你已有的知识进行回答。
                          如果你确实不知道如何回答用户的问题，直接说明你不清楚即可。无论如何，不允许出现你胡言乱语胡乱答复用户的情况。  
  
用户问题：{user_message}"""  
      
    return prompt_template.format(context=context, user_message=user_message)  
  
def call_internal_chat_api(chat_data: dict):  
    """调用内部对话接口"""  
    try:  
        # 调用您现有的对话接口  
        response = requests.post(f"http://10.0.15.21:5627{BASE_URL}/conversation/completion", json=chat_data)  
          
        if response.status_code == 200:  
            return response.json()  
        else:  
            return {"error": "对话接口调用失败"}  
    except Exception as e:  
        return {"error": f"对话接口调用异常: {str(e)}"}