# # ===================== function - kernel - 1
# from flask import request  
# from flask_restful import Resource  
# from controllers.console import api  
# from controllers.console.datasets.error import DocumentIndexingError  
# from controllers.console.setup import setup_required  
# from controllers.console.wraps import account_initialization_required, cloud_edition_billing_rate_limit_check, cloud_edition_billing_resource_check  
# from libs.login import login_required, current_user  
# from services.dataset_service import DatasetService, DocumentService  
# from werkzeug.exceptions import Forbidden, NotFound  
# import services.errors.document  
# import services.errors.account  


# class DocumentStatusApi(Resource):  
#     @setup_required  
#     @login_required  
#     @account_initialization_required  
#     @cloud_edition_billing_resource_check("vector_space")  
#     @cloud_edition_billing_rate_limit_check("knowledge")  
#     def patch(self, dataset_id, action):  
#         """  
#         启停文档接口  
#         支持的操作：enable（启用）、disable（禁用）、archive（归档）、un_archive（取消归档）  
#         """
#         dataset_id = str(dataset_id)  
#         dataset = DatasetService.get_dataset(dataset_id)  
#         if dataset is None:  
#             raise NotFound("Dataset not found.")  
  
#         # 权限检查：用户必须是 admin、owner 或 editor 角色  
#         if not current_user.is_dataset_editor:  
#             raise Forbidden()  
  
#         # 检查用户模型设置  
#         DatasetService.check_dataset_model_setting(dataset)  
  
#         # 检查用户权限  
#         DatasetService.check_dataset_permission(dataset, current_user)  
  
#         # 从请求参数中获取文档ID列表  
#         document_ids = request.args.getlist("document_id")  
  
#         try:  
#             # 批量更新文档状态  
#             DocumentService.batch_update_document_status(dataset, document_ids, action, current_user)  
#         except services.errors.document.DocumentIndexingError as e:  
#             raise DocumentIndexingError(str(e))  
#         except ValueError as e:  
#             raise DocumentIndexingError(str(e))  
#         except NotFound as e:  
#             raise NotFound(str(e))  
  
#         return {"result": "success"}, 200  
  

# # # 注册API路由  
# # api.add_resource(DocumentStatusApi, "/datasets/<uuid:dataset_id>/documents/status/<string:action>/batch")


# # ===================== function - kernel - 2

# # cdify/dify_client/document_toggle.py  
# from services.dataset_service import DatasetService, DocumentService  
# from models.dataset import Dataset  
# from libs.login import current_user  
# import services.errors.document  
  
# def doc_toggle_status(dataset_id: str, document_id: str, action: str):  
#     """  
#     文档启停核心逻辑  
#     基于现有的 DocumentService.batch_update_document_status 实现  
#     """  
#     try:  
#         # 获取数据集  
#         dataset = DatasetService.get_dataset(dataset_id)  
#         if dataset is None:  
#             return "false: Dataset not found"  
          
#         # 检查权限（如果需要）  
#         # DatasetService.check_dataset_permission(dataset, current_user)  
          
#         # 调用批量更新文档状态的核心逻辑  
#         DocumentService.batch_update_document_status(  
#             dataset=dataset,   
#             document_ids=[document_id],   
#             action=action,   
#             user=current_user  # 或者传入适当的用户对象  
#         )  
          
#         return "success"  
          
#     except services.errors.document.DocumentIndexingError as e:  
#         return f"false: {str(e)}"  
#     except ValueError as e:  
#         return f"false: {str(e)}"  
#     except Exception as e:  
#         return f"false: Unexpected error - {str(e)}"
    

# ===================== function - kernel - 3

# cdify/dify_client/document_toggle.py  
import requests  
import json   
  
from cdify.utils.config import *
from cdify.utils.loggers import logger


# 测试
def doc_toggle_status(dataset_id: str, document_id: str, action: str):  
    """ 通过HTTP API调用Dify服务实现文档启停 """  
    try:  
        # 根据API文档，文档状态更新接口  
        url = SERVER_BASE_URL_CONSOLE + f"/datasets/{dataset_id}/documents/status/{action}/batch"
        data = {'document_id': document_id}
        response = requests.patch(url, headers=db_hearders_console, params=data) 
        if response.status_code == 200:
            result = response.json()
            if result.get('result') == 'success':  
                return {'success': True}
            else:
                return {'success': False, 'error': 'API returned non-success result'}  
        else:  
            return {'success': False, 'error': f'HTTP {response.status_code}: {response.text}'}  

    except requests.exceptions.RequestException as e:  
        return {'success': False, 'error': f'Request failed: {str(e)}'}  
    except Exception as e:  
        return {'success': False, 'error': f'Unexpected error: {str(e)}'}



# 正式 - 必须模拟一次登录，来获取最新的控制台后台 token
import requests

# 1. 登录获取 Token
def get_console_token(email, password):
    url = SERVER_URL + "/console/api/workspaces/token"
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception("登录失败", response.text)

# 2. 启用文档
def enable_document(token, dataset_id, document_id):
    url = SERVER_URL + f"/console/api/datasets/{dataset_id}/documents/status/enable/batch"
    params = {"document_id": document_id}
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.patch(url, headers=headers, params=params)
    if response.status_code == 200:
        print("文档启用成功")
    else:
        print("启用失败", response.status_code, response.text)

# 使用示例
# token = get_console_token("admin@example.com", "your_password")
# enable_document(token, "33f96db6-5515-4da1-ac2c-a56659e7d746", "39ea732d-f58e-4944-bc68-087ac81e3489")
