import requests
from flask import Blueprint, request
from cdify.utils.config import *
from cdify.utils.decorators import timed_request


emb_status = Blueprint('emb_status', __name__)


@emb_status.route(BASE_URL + '/document/status', methods=['POST'])  
@timed_request  
def docProcess():  
    data = request.get_data()  
    json_data = json.loads(data.decode("utf-8"))  
    dataset_id = json_data.get('kb_id', '')  
    batch = json_data.get('batch', '')  
    if not dataset_id or not batch: return {'status_code': -1, 'info': '参数缺失：需要kb_id和batch', 'data': ""}  

    api_url = f"{SERVER_BASE_URL}/datasets/{dataset_id}/documents/{batch}/indexing-status"
    # api_url = f"{SERVER_BASE_URL_CONSOLE}/datasets/{dataset_id}/batch/{batch}/indexing-status"
    try:  
        response = requests.get(api_url, headers=db_hearders)
        print("状态码:",  response.status_code)
        print("响应内容:", response.text)
        if response.status_code == 200:
            print(1)
            temp_return = {  
                'code': 0,
                'data': response.json(),  
                'info': 'request document status successful!'  
            }  
        else:  
            print(2)
            temp_return = {  
                'code': response.status_code,  
                'data': response.json() if response.text else {},  
                'info': f'API调用失败: {response.status_code}'  
            }  
        from cdify.api.tls_clean_response import wrap_check_text_processing_progress_response  
        return wrap_check_text_processing_progress_response(temp_return)  

    except Exception as e:  
        return {'code': -1, 'info': f'请求异常: {str(e)}', 'data': ""}



# 未测试

@emb_status.route(BASE_URL + '/document/pause', methods=['POST'])  
@timed_request  
def pauseDocument():  
    try:  
        data = request.get_data()  
        json_data = json.loads(data.decode("utf-8"))  
        dataset_id = json_data.get('kb_id', '')  
        document_id = json_data.get('document_id', '')  
          
        if not dataset_id or not document_id:  
            return {'status_code': -1, 'info': '参数缺失：需要kb_id和document_id', 'data': ""}  
          
        # 构建 Dify Console API URL  
        api_url = f"{SERVER_BASE_URL_CONSOLE}/datasets/{dataset_id}/documents/{document_id}/pause"  
          
        headers = {  
            'Authorization': f'Bearer {db_hearders_console}',  
            'Content-Type': 'application/json'  
        }  
          
        # 调用 Dify 暂停接口  
        response = requests.patch(api_url, headers=headers)  
          
        if response.status_code == 204:  # 成功返回 204  
            temp_return = {  
                'status_code': 0,  
                'data': {'result': 'success'},  
                'info': 'document paused successfully!'  
            }  
        else:  
            temp_return = {  
                'status_code': response.status_code,  
                'data': response.json() if response.text else {},  
                'info': f'暂停失败: {response.status_code} - {response.text}'  
            }  
              
        return temp_return  
          
    except Exception as e:  
        return {  
            'status_code': -1,  
            'info': f'请求异常: {str(e)}',  
            'data': ""  
        }
    

@emb_status.route(BASE_URL + '/document/resume', methods=['POST'])  
@timed_request  
def resumeDocument():  
    try:  
        data = request.get_data()  
        json_data = json.loads(data.decode("utf-8"))  
        dataset_id = json_data.get('kb_id', '')  
        document_id = json_data.get('document_id', '')  
          
        if not dataset_id or not document_id:  
            return {'status_code': -1, 'info': '参数缺失：需要kb_id和document_id', 'data': ""}  
          
        # 构建 Dify Console API URL  
        api_url = f"{SERVER_BASE_URL_CONSOLE}/datasets/{dataset_id}/documents/{document_id}/resume"  
          
        headers = {  
            'Authorization': f'Bearer {db_hearders_console}',  
            'Content-Type': 'application/json'  
        }  
          
        # 调用 Dify 恢复接口  
        response = requests.patch(api_url, headers=headers)  
          
        if response.status_code == 204:  # 成功返回 204  
            temp_return = {  
                'status_code': 0,  
                'data': {'result': 'success'},  
                'info': 'document resumed successfully!'  
            }  
        else:  
            temp_return = {  
                'status_code': response.status_code,  
                'data': response.json() if response.text else {},  
                'info': f'恢复失败: {response.status_code} - {response.text}'  
            }  
              
        return temp_return  
          
    except Exception as e:  
        return {  
            'status_code': -1,  
            'info': f'请求异常: {str(e)}',  
            'data': ""  
        }