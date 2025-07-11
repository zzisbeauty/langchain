from flask import Blueprint, request
from cdify.utils.config import *
from cdify.utils.decorators import timed_request


downloadfiles = Blueprint('downloadfiles', __name__)


@downloadfiles.route(BASE_URL + '/downDBFiles', methods=['GET'])
@timed_request
def get_down_url():
    """ 获取知识库中的文件下载地址 """
    param = request.args.to_dict()
    dataset_id = param.get('kb_id',"")
    document_id = param.get('document_id',"")

    from cdify.api.dbs.files_in_db import requests_dataset_files_url
    response = requests_dataset_files_url(dataset_id,document_id)
    
    return response
    