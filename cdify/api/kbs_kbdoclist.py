from flask import Blueprint, request
from cdify.utils.config import *
from cdify.utils.decorators import timed_request

 
kbs_kbdoclist = Blueprint('kbs_kbdoclist', __name__)


@kbs_kbdoclist.route(BASE_URL + '/document/list', methods=['GET'])
@timed_request
def get_db_doc_list_api():
    param = request.args.to_dict()
    dataset_id = param.get('kb_id','')

    from cdify.dify_client.kbs_kbdoclist import get_db_doc_list
    try:  
        all_docs = get_db_doc_list(dataset_id)  
        docs_dict = {}  
        docs_dict[dataset_id] = []  
        for doc in all_docs:  
            docid = doc['id']  
            docname = doc['name']  
            docform = doc['doc_form']  
            docs_dict[dataset_id].append({docid: [docname, docform]})  
          
        temp_return = {'code': 0, 'data': docs_dict, 'message': f'获取知识库 Doc List Success !'}  
          
        from cdify.api.tls_clean_response import convert_dify_doc_list_response_to_ragflow_format  
        return convert_dify_doc_list_response_to_ragflow_format(temp_return)  
          
    except Exception as e:  
        return {'code': -1, 'data': "", 'message': f'获取知识库 Doc List Failed: {str(e)}'}  




# 进一步获取 doc 的 chunk result # 简单分页模式
@kbs_kbdoclist.route(BASE_URL + '/chunk/list', methods=['GET'])
@timed_request
def get_db_doc_paragraphs_list():
    param = request.args.to_dict()
    dataset_id = param.get('kb_id','')
    document_id = param.get('doc_id', '')
    keywords = param.get('keywords', '')
    page = param.get('page', 1)
    limit = param.get('size', 100)
    if not dataset_id or not document_id:
        return {'code': -1, 'data': "", 'message': '参数没有传递完整，请补全参数！'}
    
    from cdify.dify_client.kbs_kbdoclist import get_db_doc_paragraphs_list
    response = get_db_doc_paragraphs_list(
        dataset_id, doc_id=document_id, 
        page=page, limit=limit  # 分页参数
    )
    if response.status_code != 200:
        return {'code': -1, 'data': "", 'message': '获取知识库 Doc List Failed ！'}

    from cdify.api.tls_clean_response import convert_dify_to_ragflow_structure4
    try:
        parasLits = json.loads(response.text)['data']
        return convert_dify_to_ragflow_structure4(parasLits,keywords)
    except:
        return {'code': -1, 'data': "",  'message': '获取知识库 Doc List Failed ！'}




# 进一步控制 doc chunks status 的  api - del chunk
@kbs_kbdoclist.route(BASE_URL + '/chunk/paragraph/rm', methods=['DELETE'])
@timed_request
def del_paragraph():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    dataset_id = json_data.get('kb_id','')
    doc_id = json_data.get('doc_id','')
    para_id = json_data.get('para_id','')

    from cdify.dify_client.kbs_kbdoclist import del_para_in_doc
    response = del_para_in_doc(dataset_id=dataset_id,doc_id=doc_id,seg_id=para_id)
    if 'false' in response:
        return {'code': -1, 'data': "", 'message': 'Delete Paragraph failed',}
    return {'code': 0, 'data': "", 'message': 'Delete Paragraph successful!'}





# 进一步控制 doc chunks status 的  api - add chunk
@kbs_kbdoclist.route(BASE_URL + '/chunk/paragraph/add', methods=['POST'])
@timed_request
def add_paragraph():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    dataset_id = json_data.get('kb_id', '')
    doc_id = json_data.get('doc_id', '')
    keywords = json_data.get('keywords', [])
    content = json_data.get('content', '')
    if not content:
        return {'code': -1, 'data': "", 'message': '请输入要更新的内容',}
    
    from cdify.dify_client.kbs_kbdoclist import get_db_doc_list
    response = get_db_doc_list(dataset_id=dataset_id)
    docs = json.loads(response.text)['data']
    target_doc_type = ''
    for doc in docs:
        if doc_id == doc['id']:
            target_doc_type = doc['doc_form']
            break
    
    answer = json_data.get('answer', '')
    if target_doc_type == 'qa_model' and not answer:
        return {'code': -1, 'data': "", 'message': '当前待add paragraph 的 doc 是 Q-A 文档，必须传入 anser 答案信息 !',}

    temp_data = []
    temp_data.append({'content': content, 'answer': answer, 'keywords': keywords})

    params = {}
    params['data'] = {'segments': temp_data}

    from cdify.dify_client.kbs_kbdoclist import add_content_2_doc
    response = add_content_2_doc(dataset_id,doc_id,params['data'])
    if response.status_code != 200:    
        return {'code': -1, 'data': "",  'message': '向知识库的文档添加文本段落失败 ！'}
    try:
        data_response = json.loads(response.text)
        from cdify.api.tls_clean_response import filter_insert_response
        temp_return = {'code': 0, 'data': data_response, 'message': '向知识库的文档添加文本段落成功!'}
        return filter_insert_response(temp_return)
    except Exception as e:
        return {'code': -1, 'data': "", 'message': '向知识库的文档添加文本段落失败, 由于API响应结果 json 序列化失败导致 ！'}