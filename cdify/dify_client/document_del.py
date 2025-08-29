import os
import sys

import requests
from cdify.utils.config import *
from cdify.utils.loggers import logger



# """
# curl --location --request DELETE 'http://10.0.15.21/v1/datasets/{dataset_id}/documents/{document_id}' \
# --header 'Authorization: Bearer {api_key}'
# """
# # 只删除一个，这个方法没有用
# def docdelete(dataset_id, document_id):
#     url = SERVER_BASE_URL + f'/datasets/{dataset_id}/documents/{document_id}'
#     try:
#         requests.delete(url, headers=db_hearders)
#         return f'delete document true'
#     except:
#         return f'delete document false' 

#     # print("状态码:",  response.status_code)
#     # print("响应内容:", response.text)
#     return response




def docdelete(dataset_id, doc_id):  
    """  
    删除文档（支持单个或批量）  
      
    Args:  
        dataset_id: 知识库ID  
        doc_id: 文档ID（字符串）或文档ID列表（list）  
      
    Returns:  
        str: 删除结果信息  
    """  
    # 内部转换：将单个字符串转换为列表  
    if isinstance(doc_id, str):  
        document_ids = [doc_id]  
    elif isinstance(doc_id, list):  
        document_ids = doc_id  
    else:  
        return 'delete document false - invalid doc_id type'  
      
    if not document_ids:  
        return 'delete document false - no documents provided'  
      
    success_count = 0  
    failed_count = 0  
    failed_docs = []  
      
    for document_id in document_ids:  
        url = SERVER_BASE_URL + f'/datasets/{dataset_id}/documents/{document_id}'  
        try:  
            response = requests.delete(url, headers=db_hearders)  
            if response.status_code == 204:  # Dify API删除成功返回204  
                success_count += 1  
            else:  
                failed_count += 1  
                failed_docs.append(document_id)  
        except Exception as e:  
            failed_count += 1  
            failed_docs.append(document_id)  
      
    if failed_count == 0:  
        return f'delete document true - all {success_count} documents deleted successfully'  
    elif success_count == 0:  
        return f'delete document false - all {failed_count} documents failed to delete'  
    else:  
        return f'delete document partial - {success_count} succeeded, {failed_count} failed: {failed_docs}'
