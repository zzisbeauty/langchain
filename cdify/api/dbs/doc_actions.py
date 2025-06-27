import os
import sys
import json, requests


sys.path.append(r'E:\langchain-core-0.3.64')
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.append(project_root)


from cdify.tools import *



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
        # print(e)
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
        # print(e)
        return ''




"""
curl --location --request POST 'http://10.0.15.21/v1/datasets/{dataset_id}/retrieve' \
--header 'Authorization: Bearer {api_key}'\
--header 'Content-Type: application/json'\
--data-raw '{
  "query": "test",
  "retrieval_model": {
      "search_method": "keyword_search",
      "reranking_enable": false,
      "reranking_mode": null,
      "reranking_model": {
          "reranking_provider_name": "",
          "reranking_model_name": ""
      },
      "weights": null,
      "top_k": 1,
      "score_threshold_enabled": false,
      "score_threshold": null,
      "metadata_filtering_conditions": {
          "logical_operator": "and",
          "conditions": [
              {
                "name": "document_name",
                "comparison_operator": "contains",
                "value": "test"
              }
          ]
      }
  }
}'
"""
def retrieval(dataset_id, data):
    url = SERVER_BASE_URL + f'/datasets/{dataset_id}/retrieve'
    response = requests.post(url, headers=db_hearders, json=data)
    print("状态码:", response.status_code)
    print("响应内容:", response.text)
    return response
