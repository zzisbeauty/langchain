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
    response = requests.get(url, headers=db_hearders)

    # print("状态码:", response.status_code)
    # print(json.loads(response.text))
    return response



# get document chunks
def get_db_doc_paragraphs_list(dataset_id, doc_id):
    url = SERVER_BASE_URL + f'/datasets/{dataset_id}/documents/{doc_id}/segments'
    response = requests.get(url, headers=db_hearders)

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