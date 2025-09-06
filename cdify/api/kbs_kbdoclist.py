from flask import Blueprint, request
from cdify.utils.config import *
from cdify.utils.decorators import timed_request

 
kbs_kbdoclist = Blueprint('kbs_kbdoclist', __name__)


@kbs_kbdoclist.route(BASE_URL + '/document/list', methods=['GET'])  
@timed_request  
def get_db_doc_list_api():  
    param = request.args.to_dict()  
    dataset_id = param.get('kb_id','')  
    page_no = param.get('pageNo', 1)    
    page_size = param.get('pageSize', 20)    
    try:  
        page = int(page_no)  
        limit = int(page_size)  
    except (ValueError, TypeError):  
        page = 1  
        limit = 20  
    from cdify.dify_client.kbs_kbdoclist import get_db_doc_list  
    try:    
        all_docs = get_db_doc_list(dataset_id, page, limit)    
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



# 进一步获取 doc 的 chunk result
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
        dataset_id, doc_id=document_id, page=page, limit=limit  # 分页参数
    )
    if response.status_code != 200:
        return {'code': -1, 'data': "", 'message': '获取知识库 Doc List Failed  - 1！'}
    from cdify.api.tls_clean_response import convert_dify_to_ragflow_structure4
    try:
        parasLits = json.loads(response.text)['data']
        print('检索到的所有文档切片')
        print(parasLits[:2])
        print('--------')
        return convert_dify_to_ragflow_structure4(parasLits,keywords)
    except Exception as e:
        print(e)
        return {'code': -1, 'data': "",  'message': '获取知识库 Doc List Failed - 2！'}





"""
# 请求参数格式
{  
    "kb_id": "dataset_123",  
    "doc_id": "document_456",   
    "segment_id": "segment_789",  
    "segment": {  
        "content": "更新后的文档内容",  
        "answer": "更新后的答案内容",  
        "keywords": ["关键词1", "关键词2"],  
        "enabled": true,  
        "regenerate_child_chunks": false  
    }  
}

content: 文本内容/问题内容（必填）
answer: 答案内容，Q&A模式时传值（可选）
keywords: 关键词列表（可选）
enabled: 是否启用该片段（可选）
regenerate_child_chunks: 是否重新生成子分块（可选）

# model response
{  
    "code": 0,  
    "data": {  
        "id": "segment_id",  
        "position": 1,  
        "document_id": "document_id",  
        "content": "更新后的内容",  
        "answer": "更新后的答案",  
        "word_count": 25,  
        "tokens": 0,  
        "keywords": ["关键词"],  
        "enabled": true,  
        "status": "completed"  
    },  
    "message": "更新文档片段成功！"  
}
"""
@kbs_kbdoclist.route(BASE_URL + '/segment/update', methods=['POST'])  
@timed_request  
def update_document_segment_api():  
    data = request.get_data()  
    json_data = json.loads(data.decode("utf-8"))  
      
    dataset_id = json_data.get('kb_id', '')  
    document_id = json_data.get('doc_id', '')  
    segment_id = json_data.get('segment_id', '')  
    segment_data = json_data.get('segment', {})  

    if not all([dataset_id, document_id, segment_id]):  
        return {'code': -1, 'data': "", 'message': '参数没有传递完整，请补全参数！'}  

    from cdify.dify_client.kbs_kbdoclist import update_document_segment  
    try:  
        response = update_document_segment(dataset_id, document_id, segment_id, segment_data)  
        if response.status_code == 200:  
            result_data = response.json()  
            return {'code': 0, 'data': result_data, 'message': '更新文档片段成功！'}  
        else:  
            return {'code': -1, 'data': "", 'message': f'更新文档片段失败: {response.status_code}'}  
    except Exception as e:  
        return {'code': -1, 'data': "", 'message': f'更新文档片段异常: {str(e)}'}



"""
# 参数说明
kb_id: 知识库ID（必填）
doc_id: 文档ID（必填）
metadata: 元数据过滤条件，可选值为 all、only、without（可选，默认为 all）

# 响应示例
{  
    "code": 0,  
    "data": {  
        "id": "f46ae30c-5c11-471b-96d0-464f5f32a7b2",  
        "position": 1,  
        "data_source_type": "upload_file",  
        "name": "文档名称",  
        "created_from": "api",  
        "created_by": "user_id",  
        "created_at": 1681623639,  
        "tokens": 1024,  
        "indexing_status": "completed",  
        "enabled": true,  
        "segment_count": 5,  
        "hit_count": 10,  
        "doc_form": "text_model",  
        "doc_language": "Chinese"  
    },  
    "message": "获取文档详情成功！"  
}
"""
@kbs_kbdoclist.route(BASE_URL + '/document/detail', methods=['GET'])  
@timed_request  
def get_document_detail_api():  
    param = request.args.to_dict()  
    dataset_id = param.get('kb_id', '')  
    document_id = param.get('doc_id', '')  
    metadata = param.get('metadata', 'all')  # 支持metadata过滤  
      
    if not dataset_id or not document_id:  
        return {'code': -1, 'data': "", 'message': '参数没有传递完整，请补全参数！'}  
      
    from cdify.dify_client.kbs_kbdoclist import get_document_by_id  
    try:  
        response = get_document_by_id(dataset_id, document_id)  
        if response.status_code == 200:  
            document_data = response.json()  
            return {'code': 0, 'data': document_data, 'message': '获取文档详情成功！'}  
        elif response.status_code == 404:  
            return {'code': -1, 'data': "", 'message': '文档不存在'}  
        else:  
            return {'code': -1, 'data': "", 'message': f'获取文档详情失败: {response.status_code}'}  
    except Exception as e:  
        return {'code': -1, 'data': "", 'message': f'获取文档详情异常: {str(e)}'}



# =================== 以下接口非水务需要接口 ==========================


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
