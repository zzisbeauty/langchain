import os
import sys
import json
import requests
from cdify.utils.config import *
from cdify.utils.loggers import logger



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
    
    # print("状态码:", response.status_code)
    # print("响应内容:", response.text)
    return response
