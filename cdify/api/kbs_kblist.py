from flask import Blueprint, request
from cdify.utils.config import *
from cdify.utils.decorators import timed_request

 
kbs_kblist = Blueprint('kbs_kblist', __name__)


@kbs_kblist.route(BASE_URL + '/kb/list', methods=['GET'])
@timed_request # 此处为视图函数
def request_db_list():
    param = request.args.to_dict()
    page = param.get('page',1)
    limit = param.get('page_size',100)
    keyword = param.get('keywords','')
    tag_ids = param.get('tag_ids','')

    # parameters  check
    if tag_ids and not isinstance(tag_ids, list):
        return {
            'code': -1, 'data': "", 
            'message': 'Parameter must be array[string]',
        }

    from cdify.dify_client.kbs_kblist import requests_datasets_list
    response = requests_datasets_list(
        page=page,
        limit=limit,
        keyword=keyword,
        tag_ids=tag_ids
    )
    if not response: # info == 错误信息说明
        return {
            'code': -1, 'data': "", 
            'message': 'Query db list failed! 可能是网络超时等非程序错误导致的异常，可以从服务器网络服务检查入手',
        }
    temp_return = {
        'code': 0, 'data': response,
        'message': 'Query db list successful!'
    }
    # return temp_return

    # from cdify.api.clean_kbs_res_clean import wrap_dataset_info_response # 此方法已被注释
    # return wrap_dataset_info_response(temp_return)
    from cdify.api.tls_clean_kbs_res_clean import convert_dify_response_to_ragflow_format
    return convert_dify_response_to_ragflow_format(temp_return)
