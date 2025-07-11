from flask import Blueprint, request
from cdify.utils.config import *
from cdify.utils.decorators import timed_request

 
deldoc = Blueprint('deldoc', __name__)


@deldoc.route(BASE_URL + '/document/rm', methods=['DELETE'])
@timed_request
def request_db_info_with_dbid():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    dataset_id = json_data.get('kb_id','')
    document_id =  json_data.get('doc_id','')

    from cdify.dify_client.document_del import docdelete
    response = docdelete(dataset_id, document_id)
    if 'false' in response:
        return {'code': -1, 'data': "", 'message': 'Delete document failed, 可能的原因是请求知识库信息失败, 从检查Agent网络开始',}
    return {'code': 0, 'data': "", 'message': 'Delete DB successful!'}
