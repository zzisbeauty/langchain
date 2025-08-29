from flask import Blueprint, request
from cdify.utils.config import *
from cdify.utils.decorators import timed_request


from cdify.dify_client.kbs_kblist import requests_datasets_list
 
kbs_kernel = Blueprint('kbs_kbcreate_update', __name__)


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
    # reranking_model_name  = json_data.get('reranking_model_name',reranking_model_name_config)
    # reranking_provider_name  = json_data.get('reranking_provider_name', reranking_provider_name_config)
    reranking_model_name = ''
    reranking_provider_name = ''

    # recall / retrieval 相关参数
    top_k = json_data.get('top_k', 10)
    score_threshold_enabled  = json_data.get('score_threshold_enabled', False) # 开启召回阈值，默认关闭，否则模型很难召回
    score_threshold = json_data.get('score_threshold', 0.25) # 0.25 低一些有助于保证召回
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
                'reranking_model_name':  reranking_model_name,
                'reranking_provider_name': reranking_provider_name,
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
    from cdify.api.tls_clean_kbs_res_clean import convert_dify_update_response_to_ragflow_format
    return convert_dify_update_response_to_ragflow_format(temp_return)




@kbs_kernel.route(BASE_URL + '/kb/create', methods=['POST'])
@timed_request
def create_db_api():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    name = json_data.get('name', '')
    if not name: return {'code': -1, 'data': "", 'message': '创建DB必须指定名称'};
    already_dbs = requests_datasets_list()
    if name in [i['name'] for i in already_dbs]: return {'code': -1, 'data': "", 'message': '知识库名称重复，请求改名称再进行创建'};
    description = json_data.get('description', '')
    if not description: ...; # logger.warning(f"建议对知识库做出简洁但是有效具体的描述，有助于提升后期根据用户问题完成结果召回的效果。")

    # 索引设置 - [high_quality, economy]
    indexing_technique = json_data.get('indexing_technique', 'high_quality')
    if indexing_technique != 'high_quality': indexing_technique = "high_quality";

    # 检索模式
    # semantic_search # keyword_search # full_text_search # hybrid_search
    # 当没有 rerank 模型时, 前三种检索方式可以使用； 最后一种混合检索需要 rerank 模式
    # 这又涉及到 rerank 方案的指定，重排序模式（Reranking Mode）
    # 1. reranking_model: 使用外部 rerank 模型; 2. weighted_score: 使用权重分数组合（如果需要重排序且以这种方案重排序，这个值需要有值）
    # 重排序存在的意义：
    # 1. weight_socre 它通过数学加权的方式组合不同检索方法的分数，需要有多种检索结果才有意义；因此当检索是混合检索时，这种重排序方案是有意义的；
    # 2. rerank model 直接进行重排序，很直观；
    # 因此总结：
    # 1. 单一的检索方案是不需要设置 rerank 的， reranking_enable 是 True or False 都不重要
    # 2. 单一检索方法时 reranking_enable 无意义：重排序主要用于混合检索结果的优化
    # 3. reranking_enable 为 false 时重排序不起作用：这是重排序功能的开关
    search_method = json_data.get('search_method', 'semantic_search')
    if search_method not in ['semantic_search', 'hybrid_search', 'full_text_search', 'keyword_search']:
        return {'code': -1, 'data': "", 
                'message': "检索方案设置有误，检索设置必须属于 ['semantic_search', 'hybrid_search', 'full_text_search','keyword_search'] 中的一个"}

    embedding_model = json_data.get('embedding_model', embedding_model_config)
    embedding_provider_name = json_data.get('embedding_provider_name', embedding_model_provider_config)
    reranking_enable = json_data.get('reranking_enable', False)
    # # 当 rerank enable == True 时，以下参数必须配置，如果没有 rerank，这些值设置为空
    # reranking_model_name = json_data.get('reranking_model_name', reranking_model_name_config)
    # reranking_provider_name = json_data.get('reranking_provider_name', reranking_provider_name_config)
    reranking_model_name = ''
    reranking_provider_name = ''

    # 开始检索后，
    # 1. high_quality 模式： 向量数据库会计算 source 和 target 之间的向量得分
    # 2. economy 模式：使用 calculate_keyword_score 计算关键词 TF-IDF 分数
    ...

    # 需要重排序时重排序会用到的参数
    weights = json_data.get('weights', 0.8)
    weights = round(weights, 1)
    # # if search_method == 'hybrid_search':
    if weights > 1 or weights < 0:
        weights = 0.8

    # 检索的得分控制以及，检索后的召回； # todo 这个值无论如何设置，都是 True，需要后面调用编辑接口主动修改; 
    #  # 是否对检索结果应用分数阈值过滤； 当设置为 true 时：启用分数阈值过滤，只返回分数高于 score_threshold 值的文档
    score_threshold_enabled = json_data.get('score_threshold_enabled', True)
    score_threshold = json_data.get('score_threshold', 0.3) # 不适宜太高
    top_k = json_data.get('top_k', 3)
    

    # paras_data = { # 验证（一）
    #     # base model
    #     "name": name,
    #     "description": description,
    #     "indexing_technique": indexing_technique,

    #     # todo provider 参数的作用未来需要明确， # 因此目前 provider 参数固定为 vendor
    #     "provider": json_data.get('provider', 'vendor'), # 默认本地上传文件作为知识 provider， 未来有必要时，放开  # external 外部知识库接口； 当前参数只能为 vendor
    #     # 当 provider 参数是 external 时，下方两个参数必须； 未来再完善 provider value = external 的作用，因此下方两个参数暂时取消
    #     # "external_knowledge_id" : json_data.get('external_knowledge_id', ''), # 外部知识库 ID
    #     # "external_knowledge_api_id" : json_data.get('external_knowledge_api_id', ''), # 外部知识库 API ID

    #     # # 验证一下不指定 model 时，知识库是否会强行指定 embedding model。结论：会。这里的过程需要再明确细节。
    #     "embedding_model": embedding_model,
    #     # 'embedding_provider_name' : embedding_provider_name, # this key is false ?  source my
    #     'embedding_model_provider': embedding_provider_name, # is true

    #     # 检索与召回参数配置，且这里需要说明的是：
    #     # 只要 retrieval_model 包含 reranking_model 字段且该字段有 reranking_provider_name，系统就会调用验证函数
    #     # api/controllers/service_api/dataset/dataset.py
    #     # 这个验证逻辑不会检查 reranking_enable 的值，而是直接验证模型配置的有效性： api/services/dataset_service.py
    #     # 因此这个 rerank 没有的时候就直接设置为空；
    #     # 或者将整个 retrievel model 取消，但这是不推荐的；
    #     "retrieval_model":{
    #         'search_method' : search_method, 
    #         'reranking_enable' : False,
    #         "reranking_model": {
    #             'reranking_model_name' : reranking_model_name,
    #             'reranking_provider_name' : reranking_provider_name,
    #         },

    #         'top_k' : top_k,
    #         'score_threshold_enabled' : score_threshold_enabled,
    #         'score_threshold' : score_threshold,
    #         'weights': { # weights 参数只在特定的重排序模式下才有意义
    #             "weight_type": "customized", 
    #             "vector_setting":{
    #                 "vector_weight":weights,
    #                 "embedding_provider_name": embedding_provider_name,
    #                 "embedding_model_name": embedding_model  
    #             },
    #             "keyword_setting":{  
    #                 "keyword_weight": 1.0 - weights  # 必须提供，两个权重之和通常为1.0  
    #             }  
    #         } # if search_method == 'hybrid_search' else None
    #     }
    # }

    paras_data = { # 验证（二）
        # base model
        "name": name,
        "description": description,
        "indexing_technique": indexing_technique,

        # todo provider 参数的作用未来需要明确， # 因此目前 provider 参数固定为 vendor
        "provider": json_data.get('provider', 'vendor'), # 默认本地上传文件作为知识 provider， 未来有必要时，放开  # external 外部知识库接口； 当前参数只能为 vendor
        # 当 provider 参数是 external 时，下方两个参数必须； 未来再完善 provider value = external 的作用，因此下方两个参数暂时取消
        # "external_knowledge_id" : json_data.get('external_knowledge_id', ''), # 外部知识库 ID
        # "external_knowledge_api_id" : json_data.get('external_knowledge_api_id', ''), # 外部知识库 API ID

        # # 验证一下不指定 model 时，知识库是否会强行指定 embedding model。结论：会。这里的过程需要再明确细节。
        "embedding_model": embedding_model,
        # 'embedding_provider_name' : embedding_provider_name, # this key is false ?  source my
        'embedding_model_provider': embedding_provider_name, # is true

        # 检索与召回参数配置，且这里需要说明的是：
        # 只要 retrieval_model 包含 reranking_model 字段且该字段有 reranking_provider_name，系统就会调用验证函数
        # api/controllers/service_api/dataset/dataset.py
        # 这个验证逻辑不会检查 reranking_enable 的值，而是直接验证模型配置的有效性： api/services/dataset_service.py
        # 因此这个 rerank 没有的时候就直接设置为空；
        # 或者将整个 retrievel model 取消，但这是不推荐的；
        "retrieval_model":{
            'search_method' : search_method,
            'reranking_enable' : False,
            'reranking_mode':'',
            "reranking_model": {
                
                'reranking_model_name' : reranking_model_name,
                'reranking_provider_name' : reranking_provider_name,
            },
            'weights': { # weights 参数只在特定的重排序模式下才有意义
                "weight_type": "customized", 
                "vector_setting":{
                    "vector_weight":weights,
                    "embedding_provider_name": embedding_provider_name,
                    "embedding_model_name": embedding_model  
                },
                "keyword_setting":{  
                    "keyword_weight": 1.0 - weights  # 必须提供，两个权重之和通常为1.0  
                }  
            }, # if search_method == 'hybrid_search' else None
            
            'score_threshold_enabled' : score_threshold_enabled,
            'score_threshold' : score_threshold,
            'top_k' : top_k
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
            temp_return = {'code': 0,'data': json.loads(response_with_xz.text), 'params':params_data, 'message': '按照参数完成DB修正后，完成DB创建！'}
            return wrap_create_db_response(temp_return)
        else:
            temp_return = {'code': 0, 'data': data, 'params': paras_data, 'message': '均已按照默认值完成DB创建，知识库创建成功!'}
            # return temp_return
            return wrap_create_db_response(temp_return)
