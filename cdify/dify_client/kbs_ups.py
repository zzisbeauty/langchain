import requests
from cdify.utils.config import *
from cdify.utils.loggers import logger
from dify_client import DifyClient



# def upload_file_with_metadata(db_id, file_name, file_path, data_json):
#     url = SERVER_BASE_URL + f'/datasets/{db_id}/document/create_by_file'
#     # 构造 multipart/form-data 请求
#     files = {
#         'data': (None, data_json, 'application/json'),
#         'file': open(file_path, 'rb')
#     }
#     response = requests.post(url, headers=db_hearders_upload_files, files=files)
#     print('Status Code:', response.status_code)
#     print('Response:', response.text)
#     return response


def upload_file_with_metadata(db_id, file_name, file_content, data_json):
    url = SERVER_BASE_URL + f'/datasets/{db_id}/document/create_by_file'  

    files = {    
        'data': (None, data_json, 'application/json'),    
        'file': (file_name, file_content, 'application/octet-stream')  # 直接使用二进制内容  
    }    

    response = requests.post(url, headers=db_hearders_upload_files, files=files)  
    # print('Status Code:', response.status_code)  
    print('Response:', response.text)  
    return response



def requests_create_dataset_with_txt(db_id, data):    
    url = SERVER_BASE_URL + f'/datasets/{db_id}/document/create-by-text'
    response = requests.post(url, headers=db_hearders, json=data)
    print("状态码:", response.status_code)
    print("响应内容:", response.text)
    return response
