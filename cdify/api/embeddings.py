from flask import Blueprint, request
from cdify.utils.config import *
from cdify.utils.decorators import timed_request

emb_status = Blueprint('emb_status', __name__)


@emb_status.route(BASE_URL + '/document/status', methods=['POST'])
@timed_request
def docProcess():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    dataset_id = json_data.get('kb_id', '')
    batch = json_data.get('batch', '')
    
    from cdify.dify_client.embeddings import docProcess
    response = docProcess(dataset_id, batch)
    if not dataset_id or not batch:
        return {'status_code': -1, 'info': '联系开发联调', 'data': "",}
    else:
        temp_return = {
            'status_code': 0,
            'data': json.loads(response.text),
            'info': 'request chat info successful!'
        }
        # return temp_return
    
        from cdify.api.tls_clean_response import wrap_check_text_processing_progress_response
        return wrap_check_text_processing_progress_response(temp_return)
