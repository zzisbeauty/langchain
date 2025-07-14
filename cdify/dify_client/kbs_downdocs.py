




"""
curl --location --request GET 'https://api.dify.ai/v1/datasets/{dataset_id}/documents/{document_id}/upload-file' \  
--header 'Authorization: Bearer {api_key}' \  
--header 'Content-Type: application/json'
"""






import os
import sys
import json
from typing import Optional, Dict, Any  

import requests
from cdify.utils.config import *
from cdify.utils.loggers import logger



def download_document_from_dataset(  
    dataset_id: str,     
    document_id: str,    
    download_dir: str = "./cdify/datas/downloads-from-dify"    
) -> Dict[str, Any]:  
    """  
    从指定知识库下载单个文档
    """  
    headers = db_hearders  # 修正拼写错误  
      
    # 调用获取上传文件信息的接口  
    upload_file_url = SERVER_BASE_URL + f"/datasets/{dataset_id}/documents/{document_id}/upload-file"  
      
    try:  
        response = requests.get(upload_file_url, headers=headers)  
        response.raise_for_status()  
        file_info = response.json()  
  
        # 获取下载信息  
        download_url = file_info.get('download_url')  
        file_name = file_info.get('name', f'document_{document_id}')  
          
        if not download_url:  
            return {'code': -1, 'data': '', 'info': '未找到下载链接'}  
  
        # 处理相对路径URL  
        if download_url.startswith('/'):  
            download_url = SERVER_BASE_URL.replace('/v1', '') + download_url  
              
        # 确保下载目录存在  
        if not download_dir:  
            download_dir = "./cdify/datas/downloads-from-dify"  
            os.makedirs(download_dir, exist_ok=True)  
        try:  
            os.makedirs(download_dir, exist_ok=True)  
        except:  
            download_dir = "./cdify/datas/downloads-from-dify"  
            os.makedirs(download_dir, exist_ok=True)  
  
        # 下载文件  
        download_response = requests.get(download_url)  
        download_response.raise_for_status()  
          
        # 保存文件  
        file_path = os.path.join(download_dir, file_name)  
        with open(file_path, 'wb') as f:  
            f.write(download_response.content)  
              
        return {  
            'code': 0,  
            'data': {  
                'file_path': file_path,  
                'file_info': file_info,  
                'download_url': download_url  
            },  
            'message': f'文档已成功下载到: {file_path}'  
        }  
          
    except requests.exceptions.RequestException as e:  
        return {  
            'code': -1,  
            'data': '',  
            'info': f'API 请求失败: {str(e)}'  
        }  
    except Exception as e:  
        return {  
            'code': -1,  
            'data': '',  
            'info': f'下载失败: {str(e)}'  
        }
    


def batch_download_documents_from_dataset(  
    dataset_id: str,  
    download_dir: str = "./cdify/datas/downloads-from-dify"  
) -> Dict[str, Any]:  
    """  
    批量下载知识库中的所有文档  
    """  
    headers = db_hearders  
      
    # 获取文档列表  
    documents_url = SERVER_BASE_URL + f"/datasets/{dataset_id}/documents"  
      
    try:  
        response = requests.get(documents_url, headers=headers)  
        response.raise_for_status()  
        documents_data = response.json()  
          
        documents = documents_data.get('data', [])  
        if not documents:  
            return {  
                'code': -1,  
                'data': '',  
                'info': '知识库中没有找到文档'  
            }  
          
        # 批量下载结果  
        results = []  
        success_count = 0  
        failed_count = 0  
          
        for doc in documents:  
            doc_id = doc.get('id', '')  
            doc_name = doc.get('name', f'document_{doc_id}')  
              
            # 调用单个下载方法  
            download_result = download_document_from_dataset(  
                dataset_id=dataset_id,  
                document_id=doc_id,  
                download_dir=download_dir  
            )  
              
            if download_result['code'] == 0:  
                success_count += 1  
            else:  
                failed_count += 1  
                  
            results.append({  
                'document_id': doc_id,  
                'document_name': doc_name,  
                'status': 'success' if download_result['code'] == 0 else 'failed',  
                'result': download_result  
            })  
          
        return {  
            'code': 0,  
            'data': {  
                'total_documents': len(documents),  
                'success_count': success_count,  
                'failed_count': failed_count,  
                'results': results,  
                'download_dir': download_dir  
            },  
            'message': f'批量下载完成，成功: {success_count}，失败: {failed_count}'  
        }  
          
    except requests.exceptions.RequestException as e:  
        return {  
            'code': -1,  
            'data': '',  
            'info': f'获取文档列表失败: {str(e)}'  
        }  
    except Exception as e:  
        return {  
            'code': -1,  
            'data': '',  
            'info': f'批量下载失败: {str(e)}'  
        }