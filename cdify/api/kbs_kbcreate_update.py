from flask import Blueprint, request
from cdify.utils.config import *
from cdify.utils.decorators import timed_request


from cdify.dify_client.kbs_kblist import requests_datasets_list
 
kbs_kernel = Blueprint('kbs_kbcreate_update', __name__)
"""
Blueprint 是一个“路由集合容器”

→ 定义了一个 Blueprint kbs_kernel
→ 所有数据库的核心操作如下（/kb/update、/kb/create）都添加到这个 kbs_kernel 中
→ 注册这个 kbs_kernel 到 app 上，相当于把所有接口一次性装上
"""



# 封装 create db 时需要进一步修改的参数
def _struct_parasm(
        indexing_technique,embedding_model_name,embedding_provider_name,
        reranking_enable,reranking_mode,reranking_provider_name,reranking_model_name,
        score_threshold_enabled,score_threshold,search_method,top_k,weights
    ):
    """ 特殊指定下，封装 db edit 参数 """
    params_data = {
        'indexing_technique': indexing_technique,
        "embedding_model":embedding_model_name,
        "embedding_model_provider": embedding_provider_name,

        'retrieval_model': {
            'reranking_enable': reranking_enable,
            "reranking_mode":reranking_mode,
            "reranking_model":{
                'reranking_provider_name': reranking_provider_name,
                'reranking_model_name':  reranking_model_name
            },

            'score_threshold_enabled': score_threshold_enabled,
            'score_threshold': score_threshold,
            'search_method': search_method,
            'top_k': top_k,

            'weights': {
                "keyword_setting":{ # vector 和 keywords 应该互补
                    "keyword_weight": 1-weights
                },
                "vector_setting":{
                    'embedding_model_name': embedding_model_name,
                    'embedding_provider_name': embedding_provider_name,
                    "vector_weight": weights
                }
            }
        }
    }
    return params_data




@kbs_kernel.route(BASE_URL + '/kb/update', methods=['PATCH'])
@timed_request
def editRetrievalProperty():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    dataset_id = json_data.get('kb_id','')
    if not dataset_id:
        return {'code': -1, 'data': "", 'message': f'请输入要编辑的知识库ID',}

    # 首先检查 kbs list
    already_dbs = requests_datasets_list()
    if dataset_id not in [i['id'] for i in already_dbs]:
        return {'code': -1, 'data': "", 'message': f'当前知识库ID {dataset_id} 不存在'}

    # base params
    name = json_data.get('name', '')
    descripe = json_data.get('description','')

    # database 属性编辑
    indexing_technique = json_data.get('indexing_technique','high_quality') # economy;

    # embedding_available = True # 这个参数多余
    embedding_provider_name = json_data.get('embedding_provider_name', embedding_model_provider_config) # my
    embedding_model_name = json_data.get('embedding_model_name', embedding_model_config)

    # 基本检索参数编辑
    search_method = json_data.get('search_method', 'hybrid_search') # 默认混合检索 # keyword_search # semantic_search  # full_text_search  # hybrid_search
    weights = json_data.get('weights', 0.8)  # 语义检索权重
    # if search_method == 'hybrid_search':
    if weights > 1 or weights < 0:
        weights = 0.8
    weights = round(weights, 1)

    # rerank 相关参数
    reranking_mode = "weight_score",
    reranking_enable  = json_data.get('reranking_enable', False) # 此参数目前 True or False 无差别； 需要源码检查此参数 ？？？
    reranking_model_name  = json_data.get('reranking_model_name',reranking_model_name_config)
    reranking_provider_name  = json_data.get('reranking_provider_name', reranking_provider_name_config)
    if reranking_enable:
        if not reranking_model_name:
            return {'code': -1, 'data': "", 'message': '如果开启rerank，必须配置 rerank model',}

    # recall / retrieval 相关参数
    top_k = json_data.get('top_k', 10)
    score_threshold_enabled  = json_data.get('score_threshold_enabled', False) # 开启召回阈值，默认关闭，否则模型很难召回
    score_threshold = json_data.get('score_threshold', 0.25) # 0.25 有助于保证召回
    if score_threshold_enabled:
        if score_threshold > 1 or score_threshold < 0:
            # logger.warning(f'score_threshold 必须在 0~1 之间，当前 score_threshold 设置为： {score_threshold},已经将 score_threshold 恢复为默认值 0.8')
            json_data['score_threshold'] = 0.8

    params_data = {
        'name': name, 'description': descripe,
        'indexing_technique': indexing_technique,
        "embedding_model":embedding_model_name, "embedding_model_provider": embedding_provider_name,
        'retrieval_model': {
            'reranking_enable': reranking_enable,
            "reranking_mode":reranking_mode,
            "reranking_model":{
                'reranking_provider_name': reranking_provider_name,
                'reranking_model_name':  reranking_model_name
            },
            'score_threshold_enabled': score_threshold_enabled,
            'score_threshold': score_threshold,
            'search_method': search_method,
            'top_k': top_k,
            'weights': {
                "keyword_setting":{
                    "keyword_weight": 1-weights
                },
                "vector_setting":{
                    'embedding_model_name': embedding_model_name,
                    'embedding_provider_name': embedding_provider_name,
                    "vector_weight": weights
                }
            }
        }
    }
    if not name:
        params_data.pop('name')
    if not descripe:
        params_data.pop('description')

    from cdify.dify_client.kbs_kbcreate_edit import edit_db
    response = edit_db(dataset_id=dataset_id, data=params_data)
    if response.status_code != 200:
        return {'code': -1, 'data': "", 'message': 'Edit DB failed',}
    temp_return = {'code': 0,'data': response.text,'message': 'Edit DB successful!'}
    # return temp_return

    # from cdify.api.clean_kbs_res_clean import wrap_edit_db_response
    # return wrap_edit_db_response(temp_return)
    from cdify.api.tls_clean_kbs_res_clean import convert_dify_update_response_to_ragflow_format
    return convert_dify_update_response_to_ragflow_format(temp_return)




@kbs_kernel.route(BASE_URL + '/kb/create', methods=['POST'])
@timed_request
def create_db_api():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    name = json_data.get('name', '')
    if not name:
        return {'code': -1, 'data': "", 'message': '创建DB必须指定名称'}

    already_dbs = requests_datasets_list()
    if name in [i['name'] for i in already_dbs]:
        return {'code': -1, 'data': "", 'message': '知识库名称重复，请求改名称再进行创建'}

    description = json_data.get('description', '')
    if not description:
        # logger.warning(f"建议对知识库做出简洁但是有效具体的描述，有助于提升后期根据用户问题完成结果召回的效果。")
        ...

    # 需要指定这个默认值时，传参时不要出现 indexing_technique 参数
    indexing_technique = json_data.get('indexing_technique', 'high_quality')
    if indexing_technique not in ['high_quality', 'economy']:
        # logger.warning(f"创建DB时向量索引方案必须在 [high_quality, economy] 中选择。恢复 indexing_technique 默认值: high_quality")
        indexing_technique = "high_quality"

    # 特殊参数，就是自动 init 无法完成指定参数的成功设置
    search_method = json_data.get('search_method', 'semantic_search') # 这里创建时，生成的 db，这个值无论如何指定，都是 semantic_search , 需要调用编辑接口主动修改： # hybrid_search # semantic_search # full_text_search
    if search_method not in ['semantic_search', 'hybrid_search', 'full_text_search']:
        return {
            'code': -1, 'data': "", 
            'message': "检索方案设置有误，检索设置必须属于 ['semantic_search', 'hybrid_search', 'full_text_search'] 中的一个"
        }

    score_threshold_enabled = json_data.get('score_threshold_enabled', True) # 这个值无论如何设置，都是 True，需要后面调用编辑接口主动修改
    # print(type(score_threshold_enabled), score_threshold_enabled)

    embedding_model = json_data.get('embedding_model', embedding_model_config)
    embedding_provider_name = json_data.get('embedding_provider_name', embedding_model_provider_config)
    
    reranking_enable = json_data.get('reranking_enable', False)
    # # 当 rerank enable == True 时，以下参数必须配置，反之可为空
    reranking_model_name = json_data.get('reranking_model_name', reranking_model_name_config)
    reranking_provider_name = json_data.get('reranking_provider_name', reranking_provider_name_config)

    score_threshold = json_data.get('score_threshold', 0.75)
    top_k = json_data.get('top_k', 3)
    weights = json_data.get('weights', 0.8)
    # # if search_method == 'hybrid_search':
    if weights > 1 or weights < 0:
        weights = 0.8
    weights = round(weights, 1)

    # logger.info("====================================== create db log")
    paras_data = {
        "name": name,
        "description": description,
        "indexing_technique": indexing_technique,  # 索引方案，默认 high_quality ， 可选 economy

        "provider": json_data.get('provider', 'vendor'), # 默认本地上传文件作为知识 provider， 未来有必要时，放开  # external 外部知识库接口； 当前参数只能为 vendor
        # 当 provider 参数是 external 时，下方两个参数必须； 未来再完善 provider value = external 的作用，因此下方两个参数暂时取消
        # "external_knowledge_id" : json_data.get('external_knowledge_id', ''), # 外部知识库 ID
        # "external_knowledge_api_id" : json_data.get('external_knowledge_api_id', ''), # 外部知识库 API ID

        # # 验证一下不指定 model 时，知识库是否会强行指定 embedding model。结论：会。这里的过程需要再明确细节。
        "embedding_model": embedding_model,
        # 'embedding_provider_name' : embedding_provider_name, # this key is false ?  source my
        'embedding_model_provider': embedding_provider_name, # is true

        # 检索与召回参数配置
        "retrieval_model":{
            'search_method' : search_method, 

            'reranking_enable' : reranking_enable,
            # "reranking_model": {
            #     'reranking_model_name' : reranking_model_name,
            #     'reranking_provider_name' : reranking_provider_name,
            # },
            
            'top_k' : top_k,
            'score_threshold_enabled' : score_threshold_enabled,
            'score_threshold' : score_threshold,
            'weights': {
                "weight_type": "customized", 
                "vector_setting":{
                    "vector_weight":weights,
                    "embedding_provider_name": embedding_provider_name,  
                    "embedding_model_name": embedding_model  
                },
                "keyword_setting":{  
                    "keyword_weight": 1.0 - weights  # 必须提供，两个权重之和通常为1.0  
                }  
            } # if search_method == 'hybrid_search' else None
        }
    }

    from cdify.dify_client.kbs_kbcreate_edit import create_db_old, create_db_new
    response = create_db_old(data=paras_data)
    # response = create_db_new(db_name=name)

    if response.status_code != 200:
        return {'code': -1, 'data': "", 'message': '创建 DB 失败，联系开发确认参数具体问题'}
    else:
        from cdify.api.tls_clean_response import wrap_create_db_response
        data = json.loads(response.text)
        # 如果创建的 DB 不是默认值，就直接做一些修改；因为在参数中指定默认值，但是创建的 DB 属性总是不是默认值，主要是这两个参数比较奇怪
        # 1. score_threshold_enabled 主动设置为 False 时，但是创建出来的都是 True，即这个值无论如何在创建阶段都是 True
        # 2. search_method 主动设置为 hybrid_search 时， 但是这个值在创建阶段无论如何都是 semantic_search
        # 此时就要接口内部直接调用 db edit api，来创建如何用户要求的 db
        if not score_threshold_enabled or (search_method !='semantic_search'):
            """
            1. 如果检测到 rerank 模型，那么 rerank enable 可以是 True；也可以是 False
            2. 如果没有检测到 rerank 模型，那么必须是 False
            """
            # if ...
            # else ...

            # 目前是没有 rarank ，因此必须为 false
            params_data = _struct_parasm( # 构造参数
                indexing_technique=indexing_technique,
                embedding_model_name=embedding_model, 
                embedding_provider_name=embedding_provider_name,

                reranking_enable=reranking_enable, 
                # reranking_enable=False, 
                reranking_mode='weight_score',
                reranking_provider_name=reranking_provider_name ,
                reranking_model_name=reranking_model_name,

                score_threshold_enabled=score_threshold_enabled,
                score_threshold=score_threshold,
                search_method=search_method,
                top_k=top_k,
                weights=weights
            )
    
            from cdify.dify_client.kbs_kbcreate_edit import edit_db
            response_with_xz = edit_db(dataset_id=data['id'], data=params_data)
            if response_with_xz.status_code != 200:
                return {'code': -1, 'data': "", 'message': 'DB创建成功，但是在创建成功后，对DB进行修正时发生或错，请联系开发联调',}
            temp_return = {'code': 0,'data': json.loads(response_with_xz.text),  'message': '按照参数完成DB修正后，完成DB创建！'}
            return wrap_create_db_response(temp_return)
        else:
            temp_return = {'code': 0, 'data': data, 'message': '均已按照默认值完成DB创建，知识库创建成功!'}
            # return temp_return
            return wrap_create_db_response(temp_return)