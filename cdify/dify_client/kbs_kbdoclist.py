import os
import sys
import json

import requests
from cdify.utils.config import *
from cdify.utils.loggers import logger


# 获取知识库中的所有 doc list
def get_db_doc_list(dataset_id, page=1, limit=20):  
    url = SERVER_BASE_URL + f'/datasets/{dataset_id}/documents'    
    params = {'page': page, 'limit': limit}    
    response = requests.get(url, headers=db_hearders, params=params)  
    if response.status_code != 200:    
        raise Exception(f"API 请求失败: {response.status_code}")    
        # return ''
    data = response.json()
    print(data)
    documents = data.get('data', [])    
    return documents


# 获取所有 doc chunks
def get_db_doc_paragraphs_list(dataset_id, doc_id, page=1, limit=100):
    url = SERVER_BASE_URL + f'/datasets/{dataset_id}/documents/{doc_id}/segments'
    params = {
        'page': page,  
        'limit': limit  # 设置为最大值100
    }
    response = requests.get(
        url, headers=db_hearders, params=params # 分页参数
    )
    # print("状态码:", response.status_code)
    # print("响应内容:", json.loads(response.text))
    return response




def get_document_by_id(dataset_id, document_id):  
    """ 通过文档ID获取文档详情  
    Args:  
        dataset_id: 知识库ID  
        document_id: 文档ID  
    Returns:  
        response: API响应  
    """  
    url = SERVER_BASE_URL + f'/datasets/{dataset_id}/documents/{document_id}'  
    response = requests.get(url, headers=db_hearders)  
    return response






def update_document_segment(dataset_id, document_id, segment_id, segment_data):  
    """ 更新文档片段  
    Args:  
        dataset_id: 知识库ID  
        document_id: 文档ID  
        segment_id: 片段ID  
        segment_data: 片段数据  
    Returns:  
        response: API响应  
    """  
    url = SERVER_BASE_URL + f'/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}'  
    data = {"segment": segment_data}  
    response = requests.post(url, headers=db_hearders, json=data)  
    return response


"""
curl --location --request DELETE 'http://10.0.15.21/v1/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}' \
--header 'Authorization: Bearer {api_key}' \
--header 'Content-Type: application/json'
"""
def del_para_in_doc(dataset_id, doc_id, seg_id):
    url = SERVER_BASE_URL + f'/datasets/{dataset_id}/documents/{doc_id}/segments/{seg_id}'
    try:
        requests.delete(url, headers=db_hearders)
        return f'delete db {dataset_id} doc {doc_id}, para_id {seg_id} true'
    except Exception as e:
        return f'delete db {dataset_id} doc {doc_id}, para_id {seg_id} false'
    

"""
curl --location --request POST 'http://10.0.15.21/v1/datasets/{dataset_id}/documents/{document_id}/segments' \
--header 'Authorization: Bearer {api_key}' \
--header 'Content-Type: application/json' \
--data-raw '{"segments": [{"content": "1","answer": "1","keywords": ["a"]}]}'
"""
def add_content_2_doc(dataset_id, document_id, data):
    url = SERVER_BASE_URL + f'/datasets/{dataset_id}/documents/{document_id}/segments'
    try:
        response = requests.post(url, headers=db_hearders, json=data)
        # print("状态码:", response.status_code)
        # print("响应内容:", response.text)
        return response
    except Exception as e:
        return ''