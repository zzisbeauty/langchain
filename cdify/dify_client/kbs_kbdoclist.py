import os
import sys
import json

import requests
from cdify.utils.config import *
from cdify.utils.loggers import logger



"""
curl --location --request GET 'http://10.0.15.21/v1/datasets/{dataset_id}/documents' \
--header 'Authorization: Bearer {api_key}'
"""
def get_db_doc_list(dataset_id):
    url = SERVER_BASE_URL + f'/datasets/{dataset_id}/documents'  
    all_documents = []  
    page = 1
    limit = 100
    while True:
        params = {'page': page,'limit': limit}  
        response = requests.get(url, headers=db_hearders, params=params)
        if response.status_code != 200:  
            raise Exception(f"API 请求失败: {response.status_code}")  
        data = response.json()  
        documents = data.get('data', [])  
        all_documents.extend(documents)
        # 检查是否还有更多数据  
        has_more = data.get('has_more', False)  
        if not has_more or len(documents) < limit:  
            break  
        page += 1
    return all_documents




# 获取所有 chunks
def get_db_doc_paragraphs_list(dataset_id, doc_id, page=1, limit=100):
    url = SERVER_BASE_URL + f'/datasets/{dataset_id}/documents/{doc_id}/segments'
    params = {
        'page': page,  
        'limit': limit  # 设置为最大值100  
    }
    response = requests.get(
        url, headers=db_hearders, 
        params=params # 分页参数
    )
    # print("状态码:", response.status_code)
    # print("响应内容:", json.loads(response.text))
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