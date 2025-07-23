# cdify/dify_client/model_service.py  
import requests  
from cdify.utils.config import *
# from cdify.utils.config import DIFY_API_BASE_URL, DIFY_API_KEY  


def get_models_by_type(model_type: str):  
    """ 通过HTTP API获取指定类型的模型列表 """  
    try:  
        # 使用Service API的v1端点  
        url = SERVER_BASE_URL + f'/workspaces/current/models/model-types/{model_type}'
        response = requests.get(url, headers=db_hearders)  
        if response.status_code == 200:  
            result = response.json()  
            return {  
                'success': True,  
                'data': result.get('data', [])  
            }  
        else:  
            return {  
                'success': False,  
                'error': f'HTTP {response.status_code}: {response.text}'  
            }  
              
    except requests.exceptions.RequestException as e:  
        return {'success': False, 'error': f'Request failed: {str(e)}'}  
    except Exception as e:  
        return {'success': False, 'error': f'Unexpected error: {str(e)}'}  
  



def set_default_model(model_type: str, provider: str, model: str):  
    """  选择 / 设置默认模型  """  
    try:
        # url = f"{DIFY_API_BASE_URL}/workspaces/current/default-model"
        url = SERVER_BASE_URL_CONSOLE + '/workspaces/current/default-model'
        data = {
            "model_settings": [{  
                "model_type": model_type,  
                "provider": provider,  
                "model": model
            }]  
        }
        response = requests.post(url, headers=db_hearders_console, json=data)
        if response.status_code == 200:  
            result = response.json()
            if result.get('result') == 'success':  
                return {'success': True}  
            else:  
                return {'success': False, 'error': 'API returned non-success result'}  
        else:  
            return {'success': False, 'error': f'HTTP {response.status_code}: {response.text}'}  

    except Exception as e:  
        return {'success': False, 'error': f'Error: {str(e)}'}
