import os
import sys
import json, requests


sys.path.append(r'E:\langchain-core-0.3.64')
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.append(project_root)


from cdify.tools import *


def requests_datasets_list(
    page=1, 
    limit=100,
    keyword='',
    # tag_ids = '',
):
    """ 获取知识库列表 """
    url = SERVER_BASE_URL + f"/datasets?page={page}&limit={limit}&keyword={keyword}"
    response = requests.get(url, headers=db_hearders)

    # print(type(response))
    # print(json.loads(response.text)['data'])

    print("状态码:", response.status_code)
    print("响应内容:", response.text)

    try:
        return json.loads(response.text)['data'] # 防止请求超时等意外错误
    except:
        return ''



def request_dbinfo(dataset_id = ''):
    url = SERVER_BASE_URL + f'/datasets/{dataset_id}'
    response = requests.get(url, headers=db_hearders)

    # print("状态码:", response.status_code)
    # print("响应内容:", response.text)

    # 防止请求超时等意外错误
    try:
        return json.loads(response.text)
    except Exception as e:
        print(e)
        return ''



"""
curl --location --request DELETE 'http://10.0.15.21/v1' \
--header 'Authorization: Bearer {api_key}'
"""
def delete_db(dataset_id):
    url = SERVER_BASE_URL + f"/datasets/{dataset_id}"
    try:
        requests.delete(url, headers=db_hearders)
        return f'delete DB {dataset_id} true'
    except:
        return f'delete DB {dataset_id} false'    

    # print("状态码:", response.status_code)
    # print("响应内容:", response.text)
    return response
    


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



def get_db_doc_paragraphs_list(dataset_id, doc_id):
    url = SERVER_BASE_URL + f'/datasets/{dataset_id}/documents/{doc_id}/segments'
    response = requests.get(url, headers=db_hearders)
    print("状态码:", response.status_code)
    # print("响应内容:", response.text)
    print(json.loads(response.text))
    return response




if __name__ == "__main__":
    datasets = requests_datasets_list(page=1, limit=20)#['data']
    print("数据集列表:", json.dumps(datasets, indent=2, ensure_ascii=False))