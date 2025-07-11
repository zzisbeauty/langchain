from flask import Blueprint, request
from cdify.utils.config import *
from cdify.utils.decorators import timed_request

 
kbs_kbdetail = Blueprint('kbs_kbdetail', __name__)


@kbs_kbdetail.route(BASE_URL + '/kb/detail', methods=['GET'])
@timed_request
def request_db_info_with_dbid():
    param = request.args.to_dict()
    dataset_id = param.get('kb_id','')
    if not dataset_id:
        return {
            'code': -1, 'data': "", 
            'message': '请提供要查询的 dataset_id',
        }

    from cdify.dify_client.kbs_kbdetail import request_dbinfo
    response = request_dbinfo(dataset_id=dataset_id)
    if not response: # info == 错误信息说明
        return {
            'code': -1, 'data': "", 
            'message': 'Query db info with dataset id failed!',
        }
    temp_return = {
        'code': 0, 'data': response, 
        'message': 'Query db info with dataset id successful!'
    }
    # return temp_return

    # from cdify.api.clean_kbs_res_clean import wrap_dataset_info_response # 此方法已被注释
    # return wrap_dataset_info_response(temp_return)
    from cdify.api.tls_clean_kbs_res_clean import convert_dify_detail_response_to_ragflow_format
    return convert_dify_detail_response_to_ragflow_format(temp_return)
