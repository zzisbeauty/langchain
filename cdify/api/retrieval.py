from flask import Blueprint, request
from cdify.utils.config import *
from cdify.utils.generals import *
from cdify.utils.decorators import timed_request


retrieval = Blueprint('retrieval', __name__)



@retrieval.route(BASE_URL + '/chunk/retrieval_test', methods=['POST'])
@timed_request
def retrieval_db():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    dataset_id = json_data.get('kb_id', '')
    query = json_data.get('question', '')
    search_method = json_data.get('search_method', 'semantic_search') # 默认 semantic_search； 有 keyword_search、full_text_search、hybrid_search(混合检索)
    if not query or not dataset_id:
        return {'status_code': -1, 'data': "", 'info': '知识库ID or Query 参数信息为空'}
    
    reranking_enable = json_data.get('reranking_enable', False) # 如果检索模式为 semantic_search 模式或者 hybrid_search 则传值，说明用到向量时必有排序发生
    reranking_mode = {
        'reranking_provider_name' : json_data.get('reranking_provider_name', reranking_provider_name_config),
        'reranking_model_name' : json_data.get('reranking_provider_name', reranking_model_name_config)
    }

    weight =  json_data.get('vector_similarity_weight', 0.7)
    top_k = json_data.get('top_k', 5)
    score_threshold_enabled = json_data.get('score_threshold_enabled', False) # 默认保持 false，否则很难召回
    score_threshold = json_data.get('similarity_threshold', 0.1)

    params = {
        'query': query,
        'retrieval_model': {
            'search_method': search_method,
            'reranking_enable': reranking_enable,
            'reranking_mode': reranking_mode,
            'weights': weight,
            'top_k': top_k,
            'score_threshold_enabled': score_threshold_enabled, # score_threshold_enabled
            'score_threshold': score_threshold,
            'metadata_filtering_conditions': {}
        },
    }

    from cdify.dify_client.retrieval import retrieval
    response = retrieval(dataset_id=dataset_id, data=params)
    if response.status_code != 200:    
        return {'code': -1, 'data': "", 'message': '知识库检索失败 ！'}
    data_response = json.loads(response.text)
    temp_return = {'code': 0,'data': data_response, 'message': '知识库检索成功!'}
    # return temp_return

    from cdify.api.tls_clean_response import wrap_knowledge_search_response
    return wrap_knowledge_search_response(temp_return)