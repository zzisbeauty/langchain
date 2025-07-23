import json  
import requests  
from typing import Optional, Dict, Any  
from cdify.utils.config import *
  
class DynamicKnowledgeChatService:  
    def __init__(self):  
        self.api_key = secret_key
        self.base_url = SERVER_BASE_URL  
        self.headers = app_headers
        # self.headers = {  
        #     "Authorization": f"Bearer {self.api_key}",  
        #     "Content-Type": "application/json"  
        # }  
  
    def chat_with_specified_dataset(  
        self,   
        user_id: str,   
        message: str,   
        dataset_id: str,  
        conversation_id: Optional[str] = None,  
        streaming: bool = False  
    ) -> Dict[str, Any]:  
        """
        使用指定知识库进行聊天  
        :param user_id: 用户ID
        :param message: 用户消息
        :param dataset_id: 指定的知识库ID  
        :param conversation_id: 对话ID（可选）  
        :param streaming: 是否流式响应  
        :return: 聊天响应数据  
        """  
        try:  
            knowledge_context = self._retrieve_from_dataset(message, dataset_id)  
            if knowledge_context:  
                enhanced_query = f"""基于以下参考资料回答用户问题：  

{knowledge_context}  

用户问题：{message}  

请基于上述参考资料回答，如果参考资料中没有相关信息，则无需再结合参考资料，直接根据你拥有的知识答复用户即可，且此时答复的内容不要让用户看出来你检索了知识库的但没有查询到相关知识。"""  
            else:  
                enhanced_query = message  
              
            # 3. 调用聊天API  
            chat_data = {  
                "inputs": {},  
                "query": enhanced_query,  
                "user": user_id,  
                "response_mode": "streaming" if streaming else "blocking"  
            }  
              
            if conversation_id:  
                chat_data["conversation_id"] = conversation_id  

            response = requests.post(  
                f"{self.base_url}/chat-messages",  
                headers=self.headers,  
                json=chat_data,  
                stream=streaming,  
                timeout=60  
            )  
              
            response.raise_for_status()  
              
            if streaming:  
                return self._handle_streaming_response(response, dataset_id)  
            else:  
                result = response.json()  
                return {  
                    "conversation_id": result.get('conversation_id'),  
                    "answer": result.get('answer'),  
                    "message_id": result.get('message_id'),  
                    "dataset_used": dataset_id,  
                    "knowledge_enhanced": bool(knowledge_context)  
                }  
                  
        except Exception as e:  
            print(f"动态知识库聊天失败: {str(e)}")  
            return None  
  

    def _retrieve_from_dataset(self, query: str, dataset_id: str) -> str:  
        """从指定知识库检索相关信息"""  
        try:  
            # retrieval_data = {  
            #     "query": query,  
            #     "retrieval_model": {  
            #         "top_k": 5,  
            #         "score_threshold": 0.1
            #     }  
            # }  
            retrieval_data = {
                'query': query,
                'retrieval_model': {
                    'search_method': 'semantic_search',
                    'reranking_enable': False,
                    # 'reranking_mode': reranking_mode,
                    'weights': 0.5, # 语义占比，低一点有助于得到答案
                    'top_k': 5,
                    'score_threshold_enabled': False, # score_threshold_enabled
                    'score_threshold': 0.1,
                    'metadata_filtering_conditions': {}
        },
    }       
            from cdify.dify_client.retrieval import retrieval
            response = retrieval(dataset_id=dataset_id, data=retrieval_data)
            # ----- <class 'requests.models.Response'> <Response [200]>
            if response.status_code == 200:  
                result = response.json() # ----- <class 'dict'>
                from cdify.utils.parser_json import extract_and_concat_content
                result = extract_and_concat_content(result)
                print('-----', type(result))
                return result
            else:
                print(f"知识库检索失败: {response.status_code}")  
                print(response.text)
                return ""
                  
        except Exception as e:  
            print(f"检索知识库 {dataset_id} 失败: {str(e)}")  
            return ""
  
    def _handle_streaming_response(self, response, dataset_id: str):  
        """处理流式响应"""  
        conversation_id = None  
        full_answer = ""  
        try:  
            for line in response.iter_lines(decode_unicode=True):  
                if line and line.startswith('data: '):  
                    data_str = line[6:]  
                    if data_str.strip() and data_str != '[DONE]':  
                        try:  
                            data = json.loads(data_str)  
                              
                            if 'conversation_id' in data and conversation_id is None:  
                                conversation_id = data['conversation_id']  
                              
                            event_type = data.get('event')  
                            if event_type == 'message':  
                                answer_chunk = data.get('answer', '')  
                                if answer_chunk:  
                                    full_answer += answer_chunk  
                            elif event_type == 'message_end':  
                                break  
                                  
                        except json.JSONDecodeError:  
                            continue  
              
            return {  
                "conversation_id": conversation_id,  
                "answer": full_answer,  
                "streaming": True,  
                "dataset_used": dataset_id  
            }  
              
        except Exception as e:  
            print(f"流式响应处理失败: {str(e)}")  
            return None
