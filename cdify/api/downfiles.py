from flask import Blueprint, request
from cdify.utils.config import *
from cdify.utils.decorators import timed_request


downloadfiles = Blueprint('downloadfiles', __name__)


@downloadfiles.route(BASE_URL + '/document/get', methods=['GET'])
@timed_request
def get_down_url():
    """ 获取知识库中的文件下载地址 """
    param = request.args.to_dict()
    dataset_id = param.get('kb_id',"")
    document_id = param.get('document_id',"")
    download_dir = param.get('download_dir',"")

    from cdify.dify_client.kbs_downdocs import download_document_from_dataset
    response = download_document_from_dataset(dataset_id,document_id,download_dir)
    return response



@downloadfiles.route(BASE_URL + '/documents/batch-download', methods=['GET'])  
@timed_request
def batch_download():
    """批量下载知识库中的所有文档"""  
    param = request.args.to_dict()  
    dataset_id = param.get('kb_id', "")  
    download_dir = param.get('download_dir', "")  
    if not dataset_id:  
        return {'code': -1, 'data': '', 'info': '缺少必要参数: kb_id'} 

    from cdify.dify_client.kbs_downdocs import batch_download_documents_from_dataset  
    response = batch_download_documents_from_dataset(dataset_id, download_dir)  
    return response
