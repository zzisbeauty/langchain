from flask import Blueprint, request
from cdify.utils.config import *
from cdify.utils.decorators import timed_request

 
kbs_kbrm = Blueprint('kbs_kbrm', __name__)


@kbs_kbrm.route(BASE_URL + '/kb/rm', methods=['DELETE'])
@timed_request
def delete_db():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    dataset_id = json_data.get('kb_id','')
    if not dataset_id:
        return {'code': -1, 'data': "", 
                'message': '请提供要执行删除的 dataset_id',}

    from cdify.dify_client.kbs_kblist import requests_datasets_list
    already_dbs = requests_datasets_list() # db list
    if dataset_id not in [i['id'] for i in already_dbs]:
        return {'code': -1, 'data': "", 
                'message': f'当前需要被删除的知识库ID {dataset_id} 不存在'}

    from cdify.dify_client.kbs_kbdel import delete_db
    response = delete_db(dataset_id=dataset_id)
    if 'false' in response:
        return {'code': -1, 'data': "", 'message': 'Delete DB failed,可能的原因是请求知识库信息失败, 从检查Agent网络开始',}
    return {
        'code': 0, 'data': "", 'message': 'Delete DB successful!'
    }
