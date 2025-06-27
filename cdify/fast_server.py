import os
import sys
import json, requests
from flask import Flask, request, jsonify

# sys.path.append("/home/langchain-core-0.3.64")
sys.path.append(r"E:\langchain-core-0.3.64")
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.append(project_root)

from cdify.tools import *
from cdify.loggers import logger

app = Flask(__name__)

@timed_request
@app.route(BASE_URL + '/hello', methods=['GET'])
def healthy_check():
    from cdify.api.healthy import say_hello
    response = say_hello()
    if response.status_code != 200: # info == 错误信息说明
        return {'status_code': -1, 'data': "", 'info': 'Healthy check failed!',}
    return {
        'status_code': 0, 
        'data': '',  
        'info': 'Healthy check successful!'
    }



@app.route(BASE_URL + '/dbList', methods=['GET'])
def request_db_list():
    

    param = request.args.to_dict()
    page = param.get('page',1)
    limit = param.get('limit',100)
    keyword = param.get('keyword','')
    # tag_ids = param.get('tag_ids')
    
    # parameters  check
    # if tag_ids and not isinstance(tag_ids, list):
    #     return {'status_code': -1, 'data': "Parameter must be array[string]", 'info': 'Parameter must be array[string]',}

    # logger.info("====================================== query db list log")

    from cdify.api.dbs.db_list import requests_datasets_list
    response = requests_datasets_list(
        page=page,
        limit=limit, 
        keyword=keyword, 
        # tag_ids=tag_ids
    )
    
    if not response: # info == 错误信息说明
        return {'status_code': -1, 'data': "", 'info': 'Query db list failed! 可能是网络超时等非程序导致的错误，请注意检查',}
    return {
        'status_code': 0, 
        'data': response, 
        'info': 'Query db list successful!'
    }


@app.route(BASE_URL + '/dbInfo', methods=['GET'])
def request_db_info_with_dbid():
    param = request.args.to_dict()
    dataset_id = param.get('dataset_id','')
    if not dataset_id:
        return {'status_code': -1, 'data': "", 'info': '请提供要查询的 dataset_id',}
    
    from cdify.api.dbs.db_list import request_dbinfo
    response = request_dbinfo(dataset_id=dataset_id)

    if not response: # info == 错误信息说明
        return {'status_code': -1, 'data': "", 'info': 'Query db info with dataset id failed! 可能是网络超时等非程序导致的错误，请注意检查',}
    return {
        'status_code': 0, 
        'data': response, 
        'info': 'Query db info with dataset id successful!'
    }




""" 采用只用 db name 进行数据库创建的工作 """
@timed_request
@app.route(BASE_URL + '/createDb', methods=['POST'])
def create_db_api():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))

    # for each parameter and parameters check
    name = json_data.get('name', '')
    if not name:
        return {'status_code': -1, 'data': "", 'info': '创建DB必须指定名称'}
    
    # 验证知识库 name 唯一性
    from cdify.api.dbs.db_list import requests_datasets_list
    already_dbs = requests_datasets_list() # db list
    if name in [i['name'] for i in already_dbs]:
        return {'status_code': -1, 'data': "", 'info': '知识库名称重复，请求改名称再进行创建'}

    description = json_data.get('description', '')
    if not description:
        logger.warning(f"建议对知识库做出简洁但是有效具体的描述，有助于提升后期根据用户问题完成结果召回的效果。")

    # 需要指定这个默认值时，传参时不要出现 indexing_technique 参数
    indexing_technique = json_data.get('indexing_technique', 'high_quality')
    if indexing_technique not in ['high_quality','economy']:
        logger.warning(f"创建DB时向量索引方案必须在 [high_quality, economy] 中选择。恢复 indexing_technique 默认值: high_quality")
        indexing_technique = "high_quality"
    
    # logger.info("====================================== create db log")

    # # 验证一下不指定 model 时，知识库是否会强行指定 embedding model。结论：会。这里的过程需要再明确细节。
    embedding_model = json_data.get('embedding_model', embedding_model_config)
    embedding_provider_name = json_data.get('embedding_provider_name', embedding_model_provider_config)
    reranking_model_name = json_data.get('reranking_model_name', reranking_model_name_config)
    reranking_provider_name = json_data.get('reranking_provider_name', reranking_provider_name_config)
    
    paras_data = {
        "name": name,
        "description": description,
        "indexing_technique": indexing_technique,  # 索引方案，默认 high_quality ， 可选 economy

        # "provider": json_data.get('provider', 'vendor'), # 默认本地上传文件作为知识 provider， 未来有必要时，放开 # external 外部知识库接口； 当前参数只能为 vendor
        "provider": "vendor",
        # 当 provider 参数是 external 时，下方两个参数必须； 未来再完善 provider value = external 的作用，因此下方两个参数暂时取消
        # "external_knowledge_id" : json_data.get('external_knowledge_id', ''), # 外部知识库 ID
        # "external_knowledge_api_id" : json_data.get('external_knowledge_api_id', ''), # 外部知识库 API ID

        "embedding_model": embedding_model,
        'embedding_provider_name' : embedding_provider_name,

        # 检索与召回参数配置
        "retrieval_model":{
            'search_method' : json_data.get('search_method', 'semantic_search'),# hybrid_search # semantic_search # full_text_search

            'reranking_enable' : json_data.get('reranking_enable', False),
            # 当 rerank enable == True 时，以下参数必须配置，不可为空
            'reranking_model_name' : reranking_model_name,
            'reranking_provider_name' : reranking_provider_name,

            # 召回参数
            'top_k' : json_data.get('top_k', 3),
            'score_threshold_enabled' : json_data.get('score_threshold_enabled', True),
            'score_threshold' : json_data.get('score_threshold', 0.75),
        }
    }

    # from cdify.api.dbs.create_db import create_db_old
    # response = create_db_old(data=paras_data)
    from cdify.api.dbs.create_db import create_db_new
    response = create_db_new(db_name=name)

    if response.status_code != 200:
        return {'status_code': -1, 'data': "", 'info': '创建 DB 失败，需联调检查参数配置情况'}
    return {
        'status_code': 0, 
        'data': json.loads(response.text), 
        'info': '知识库创建成功!'
    }


@timed_request
@app.route(BASE_URL + '/deleteDb', methods=['DELETE'])
def delete_db():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    dataset_id = json_data.get('dataset_id','')
    if not dataset_id:
        return {'status_code': -1, 'data': "请提供要执行删除的 dataset_id", 'info': '请提供要执行删除的 dataset_id',}

    # 验证存在这个知识库
    from cdify.api.dbs.db_list import requests_datasets_list
    already_dbs = requests_datasets_list() # db list
    if dataset_id not in [i['id'] for i in already_dbs]:
        return {'status_code': -1, 'data': "", 'info': f'当前需要被删除的知识库ID {dataset_id} 不存在'}

    from cdify.api.dbs.db_list import delete_db
    response = delete_db(dataset_id=dataset_id)
    if 'false' in response:
        return {'status_code': -1, 'data': response, 'info': 'Delete DB failed,可能的原因是请求知识库信息失败, 从检查Agent网络开始',}
    return {
        'status_code': 0, 
        'data': response, 
        'info': 'Delete DB successful!'
    }





# =====================================================================================================





""" 混合检索，此方法会少一个参数，导致文件无法正常上传，找不到是少了哪个参数
会报错: 1 validation error for KnowledgeConfig retrieval_model.weights.
keyword_setting.keyword_weight Input should be a valid number [type=float_type, input_value=None, input_type=NoneType] 
For further information visit https://errors.pydantic.dev/2.9/v/float_type
"""
@timed_request
@app.route(BASE_URL + '/editDbProperty', methods=['PATCH'])
def editRetrievalProperty():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    
    # parameters check

    dataset_id = json_data.get('dataset_id','')
    if not dataset_id:
        return {'status_code': -1, 'data': "", 'info': f'请输入要编辑的知识库ID',}

    from cdify.api.dbs.db_list import requests_datasets_list
    already_dbs = requests_datasets_list() # db list
    if dataset_id not in [i['id'] for i in already_dbs]:
        return {'status_code': -1, 'data': "", 'info': f'当前知识库ID {dataset_id} 不存在'}

    # database 属性编辑
    indexing_technique = json_data.get('indexing_technique','high_quality') # economy
    # embedding_available = True # 这个参数好像多余
    embedding_provider_name = json_data.get('embedding_provider_name', embedding_model_provider_config)  # zhipuai
    embedding_model_name = json_data.get('embedding_model_name', embedding_model_config)

    # 基本检索参数编辑
    search_method = json_data.get('search_method', 'hybrid_search') # 默认混合检索 # keyword_search # semantic_search  # full_text_search  # hybrid_search
    weights = json_data.get('weights', 0.8) # 语义检索权重
    if search_method == 'hybrid_search':
        if weights > 1 or weights < 0:
            return {'status_code': -1, 'data': "", 'info': '如果检索方案为 hybrid_search，那么，语义检索权重必须在:0~1之间',}
        weights = round(weights, 1)
    
    # rerank 相关参数
    reranking_enable  = json_data.get('reranking_enable', False) # 此参数目前 True or False 无差别； 需要源码检查此参数 ？？？
    reranking_mode = "weight_score",
    reranking_model_name  = json_data.get('reranking_model_name',reranking_model_name_config)
    reranking_provider_name  = json_data.get('reranking_provider_name', reranking_provider_name_config)
    
    # if reranking_enable:
    #     if not reranking_model_name:
    #         return {'status_code': -1, 'data': "如果开启 rerank ， 必须配置 rerank model", 'info': '如果开启rerank，必须配置 rerank model',}

    # recall 相关参数
    top_k = json_data.get('top_k', 10)
    score_threshold_enabled  = json_data.get('score_threshold_enabled', False) # 开启召回阈值，默认关闭，否则模型很难召回
    score_threshold = json_data.get('score_threshold', 0.85)
    if score_threshold_enabled:
        if score_threshold > 1 or score_threshold < 0:
            logger.warning(f'score_threshold 必须在 0~1 之间，当前 score_threshold 设置为： {score_threshold},已经将 score_threshold 恢复为默认值 0.8')
            json_data['score_threshold'] = 0.8

    params_data = {
        # base params
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
                # "keyword_setting":{ # 暂时不清楚这个参数哪里来的
                #     "keyword_weight":0.8
                # }
                "vector_setting":{
                    'embedding_model_name': embedding_model_name,
                    'embedding_provider_name': embedding_provider_name,
                    "vector_weight": weights
                }
            }
        }
    }

    from cdify.api.dbs.edit_db_retrieval import edit_db
    response = edit_db(dataset_id=dataset_id, data=params_data)
    if response.status_code != 200:
        return {'status_code': -1, 'data': "", 'info': 'Edit DB failed',}
    return {
        'status_code': 0,
        'data': response.text,
        'info': 'Edit DB successful!'
    }



@timed_request
@app.route(BASE_URL + '/insertTypeFile2DB', methods=['POST'])
def insert_type2db():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))

    dataset_id = json_data.get('dataset_id','')
    if not dataset_id:
        return  {'status_code': -1, 'data': "", 'info': '请指定知识库ID'}
    
    file_path = json_data.get('file_path','')
    try:
        f_bytes_obj = open(file_path,'rb')
        f_bytes_obj.close()
    except:
        return  {'status_code': -1, 'data': "", 'info': '文件读取失败，检查文件路径'}
    
    file_name = get_filename(file_path=file_path)
    indexing_technique = json_data.get('indexing_technique','high_quality')
    mode = json_data.get('mode','custom')  # automatic
    separator = json_data.get('separator', '\n') # ###  
    max_tokens = json_data.get('max_tokens', 1000)
    remove_urls_emails = json_data.get('remove_urls_emails', True)
    doc_form = json_data.get('doc_form ', 'text_model') # 此模式为默认
    # doc_form = json_data.get('doc_form ', 'qa_model')
    doc_language = json_data.get('doc_language', 'English')
    if doc_form == 'qa_model' and doc_language == 'English':
        logger.warning(f'当前以QA模式处理，默认为：{doc_language}，如需中文，请指定参数 doc_language = "Chinese"')

    # metadata 参数，需转成 JSON 字符串
    data_json = {
        "indexing_technique": indexing_technique,
        'doc_form': doc_form,
        'doc_language': doc_language,
        "process_rule": {
            "rules": {
                "pre_processing_rules": [
                    {"id": "remove_extra_spaces", "enabled": True},
                    {"id": "remove_urls_emails", "enabled": remove_urls_emails}
                ],
                "segmentation": {
                    "separator": separator,
                    "max_tokens": max_tokens
                }
            },
            "mode": mode
        }
    }

    from cdify.api.dbs.add_type_2_db import upload_file_with_metadata
    data_json = json.dumps(data_json)
    response = upload_file_with_metadata(db_id=dataset_id, file_name=file_name, file_path=file_path, data_json=data_json)
    print('insert file over ......................................')
    if response.status_code != 200:
        return {'status_code': -1, 'data': "", 'info': '导入数据失败，请检查参数'}
    return {
        'status_code': 0, 
        'data': response.text, 
        'info': f'导入FILE数据到知识库 {dataset_id} 成功!'
    }





from cdify.test_unit._test import *


@timed_request
@app.route(BASE_URL + '/insertText2DB', methods=['POST'])
def insert_txt2db():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))

    # parameters check
    
    # ==== base server config and test process parameters
    file_name = json_data.get('file_name','')
    text = json_data.get('text','')
    dataset_id = json_data.get('dataset_id','')
    
    # test parameters
    # json_data['dataset_id'] = 'd6142a1d-ff1b-470c-84b8-9b6f570f95d9' # test
    file_name = "鲁迅杂文-《且介亭杂文》-long-16-58", # test
    text = text_demo_long  # test

    if not file_name or not text or not dataset_id:
        return {'status_code': -1, 'data': "当前【文件名】【文本信息】【数据库ID】存在空，请检查", 'info': '当前【文件名】【文本信息】【数据库ID】存在空，请检查性'}

    # ==== 嵌入之前的文本清洗和前处理工作模式
    mode = json_data.get('mode','custom') # custom 参数将会触发一系列的文档清洗解析参数设置； automatic 根据默认参数执行嵌入和索引

    # ==== 要被清洗的数据是何种形式存入 DB
    doc_form = json_data.get('doc_form','text_model') # 索引内容的形式 ，默认为文本形式的内容嵌入； 此类数据默认采用经济模式进行索引构建
    doc_form = json_data.get('doc_form','qa_model') # 索引内容的形式 ，默认为文本形式的内容嵌入； 此类数据默认采用经济模式进行索引构建
    # qa_model ： text_model 模式还可以进一步转变为文本片段创建 Q-A 内容并完成嵌入，同时支持language setting，那么此时就要选择此模式
    # hierarchical_model ： 结构化模式内容的嵌入
    # doc_language = json_data.get('doc_language', 'Chinese') # 当要被清洗的数据要被整理成 qa 时，需要指定该参数， 非 qa_model 时，此参数无效

    # 无论何种 doc_form，都需要如下通用分割模式参数
    remove_extra_spaces = json_data.get('remove_extra_spaces', True) # 是否去除多余空格
    remove_urls_emails = json_data.get('remove_urls_emails', True) # 是否去除 URL 和 Email； 默认为 True，特殊情况下需保留此信息，改为 False
    separator = json_data.get('separator', '\n')  # 分隔符
    max_tokens = json_data.get('max_tokens', 1000) # 每段最大token数
    chunk_overlap = json_data.get('chunk_overlap', 300)
    # 另外当 doc_form == hierarchical_model 时，分为如下两种情况
    parent_mode = json_data.get('parent_mode', "full-doc") #  情况 1 此时无需额外参数配置
    # parent_mode = json_data.get('parent_mode', "paragraph") # 情况 2 此时需要如下额外参数
    separator_sub = json_data.get('separator_sub', "\n")
    max_tokens_sub = json_data.get('max_tokens_sub', 500) # 需要保证小于 max_tokens
    if (doc_form == "hierarchical_model") and (max_tokens_sub >= max_tokens):
        # logger.error(f"当前待索引内容形式为 {doc_form}, 此时 max_tokens_sub 禁止大于 max_tokens，请调整")
        return {
            'status_code': -1, 
            'data': "",
            'info': f"当前待索引内容形式为 {doc_form}, 此时 max_tokens_sub 禁止大于 max_tokens，请调整"
        }
    if doc_form == "qa_model":
        logger.info(f'当前采用 QA 模式，如果计算资源低，此模式相对耗时且会显著增加 token 消耗！')
    # 补充 doc_form 为 hierarchical_model 进行清洗与数据前处理时，结构化文本处理方式的基础选择标准：
    # 1. paragraph 模式按段落划分为父块：
    #    将整个文档作为一个整体进行召回（不切分）
    #    适合需要 “整篇理解” 的文档，如法律合同、报告; FAQ、政策文件，整体性强的文档
    # 2. full-doc 整篇当父块，
    #    适合需要整体检索的场景; full-doc 在检索时不会分割内容，但索引方式仍支持子块； 文档每一段落作为父级分段
    #    每个段落为一个召回单位; 更细粒度的召回，适合知识点分布较广的文档; 结构松散、信息点分散的资料，例如日报、聊天记录

    # ==== embedding settings
    embedding_model = json_data.get('embedding_model', embedding_model_config)
    embedding_model_provider = json_data.get('embedding_model_provider', embedding_model_provider_config)
    reranking_enable = json_data.get('reranking_enable', False) # 依赖配置 rerank 模型；如果是高精度场景，召回数量应设置小一点，rerank 可以不配置，如果是 True，必须配置 rerank model
    reranking_model_name = json_data.get('reranking_model_name', reranking_model_name_config)
    reranking_provider_name = json_data.get('reranking_provider_name', reranking_provider_name_config)

    # ==== 整个 indexing 工作模式 MODE 以及其他相关 config
    indexing_technique = json_data.get('indexing_technique', "high_quality") # "economy" or "high_quality" 索引方式，建议保持默认值；

    # ==== 检索与召回 config
    search_method = json_data.get('search_method', "hybrid_search") # 默认为混合检索  # semantic_search 语义检索  # full_text_search 全文检索
    weighted_score = json_data.get('weighted_score', 0.7) # 混合检索需要配置语义检索权重 
    score_threshold = json_data.get('score_threshold', 0.8)
    score_threshold_enabled = json_data.get('score_threshold_enabled', False) # 是否开启语义召回分数限制，默认值为 False；如果对于召回精度要求不严格，可不用调整
    if score_threshold_enabled:
        if score_threshold > 1 or score_threshold < 0:
            logger.warning(f'score_threshold 必须在 0~1 之间，当前 score_threshold 设置为： {score_threshold},已经将 score_threshold 恢复为默认值 0.8')
            json_data['score_threshold'] = 0.8
    top_k = json_data.get('top_k', 2) # 召回数量，精确场景下，不大于 2；其他低精度场景建议 3~5 个；

    # 基础参数check完毕后，展开参数构建
    # ==== 文件相关基本参数
    params_data = {
        "name": file_name,
        "text": text,
        "doc_form": doc_form,
        # "doc_language": doc_language,
        # 嵌入相关参数
        "embedding_model" :embedding_model,
        "embedding_model_provider": embedding_model_provider,
        # 索引相关参数
        "indexing_technique": indexing_technique,
    }

    # ==== 配置嵌入之前的核心参数信息
    if mode == "automatic":
        process_rule = {"mode": mode,}
        params_data["process_rule"] = process_rule
    else:
        process_rule = {
            "mode": mode,
            "rules":{
                "pre_processing_rules":[ # 基础配置
                    {"id":"remove_extra_spaces", "enabled": remove_extra_spaces},
                    {"id":"remove_urls_emails", "enabled": remove_urls_emails},
                ],
                "segmentation":{ # 基础配置
                    "separator":separator,
                    "max_tokens": max_tokens,
                    "chunk_overlap": chunk_overlap
                },
                "chunk_overlap":chunk_overlap,
                "parent_mode": parent_mode,
                "subchunk_segmentation":{
                    "separator": separator_sub,
                    "max_tokens": max_tokens_sub,
                }
            },
        }
        params_data["process_rule"] = process_rule

    # ==== 检索及检索模型配置
    retrieval_model = {}
    if search_method == "hybrid_search": # hybrid_search 混合检索配置
        retrieval_model = {
            "search_method": search_method, "top_k": top_k, "weighted_score": weighted_score,  # 基础参数
            "score_threshold_enabled": score_threshold_enabled, "score_threshold": score_threshold, # 语义控制参数
        }
    if search_method == "semantic_search": # semantic_search 纯向量检索
        retrieval_model = {
            "search_method": search_method, "top_k": top_k, # "weighted_score": weighted_score, # 相比于混合检索：少了这个权重参数； # 基础参数
            "score_threshold_enabled": score_threshold_enabled, "score_threshold": score_threshold, # 语义控制参数
        }
    if search_method == 'full_text_search': # full_text_search 全文检索； 根据关键字检索；仅包含如下核心参数
        retrieval_model = {
            "search_method": search_method, "top_k": top_k, # 基础参数
        }
    retrieval_rerank_model_config_uni = {
        "reranking_enable": reranking_enable,
        "reranking_model": {"reranking_provider_name": reranking_provider_name, "reranking_model_name": reranking_model_name}
    }
    retrieval_model.update(retrieval_rerank_model_config_uni)
    params_data["retrieval_model"] = retrieval_model
    
    # logger.info("====================================== insert text data 2 db log")

    """ 通过临时重要文本数据创建数据，并导入知识库 """
    from cdify.api.dbs.add_txt_2_db import requests_create_dataset_with_txt
    response = requests_create_dataset_with_txt(dataset_id, params_data)
    if response.status_code != 200:
        return {'status_code': -1, 'data': "", 'info': '导入数据失败，请检查参数合理性'}
    return {
        'status_code': 0, 
        'data': response.text, 
        'info': f'导入TXT数据到知识库 {dataset_id} 成功!'
    }





"""
curl --location --request GET 'http://10.0.15.21/v1/datasets/{dataset_id}/documents' \
--header 'Authorization: Bearer {api_key}'
"""

@timed_request
@app.route(BASE_URL + '/getDbDocList', methods=['GET'])
def get_db_doc_list_api():
    param = request.args.to_dict()
    dataset_id = param.get('dataset_id','')
    from cdify.api.dbs.db_list import get_db_doc_list
    response = get_db_doc_list(dataset_id)
    if response.status_code != 200:
        return {'status_code': -1, 'data': "", 'info': '获取知识库 Doc List Failed ！'}
    docs = json.loads(response.text)['data']
    docs_dict = {}
    docs_dict[dataset_id] = []
    for doc in docs:
        docid = doc['id']
        docname = doc['name']
        docform = doc['doc_form']
        docs_dict[dataset_id].append({docid: [docname, docform]})
    return {
        'status_code': 0, 
        'data': docs_dict,
        'info': f'获取知识库 Doc List Success ！!'
    }



"""
curl --location --request GET 'http://10.0.15.21/v1/datasets/{dataset_id}/documents/{document_id}/segments' \
--header 'Authorization: Bearer {api_key}' \
--header 'Content-Type: application/json'
"""
@timed_request
@app.route(BASE_URL + '/getDbDocParasList', methods=['GET'])
def get_db_doc_paragraphs_list():
    ''' 获取文档 DOC ID '''
    param = request.args.to_dict()
    dataset_id = param.get('dataset_id','')
    document_id = param.get('document_id', '')
    from cdify.api.dbs.db_list import get_db_doc_paragraphs_list
    response = get_db_doc_paragraphs_list(dataset_id,doc_id=document_id)
    if response.status_code != 200:
        return {'status_code': -1, 'data': "", 'info': '获取知识库 Doc List Failed ！'}
    parasLits = json.loads(response.text)['data']
    result = {}
    result[dataset_id + ' | ' + document_id] = [] # key: db_id | doc_id
    for para in parasLits:
        para_content = para['content']
        para_tags = para['keywords']
        para_id = para['id']
        result[dataset_id + ' | ' + document_id].append([para_content, para_tags, para_id])
    return {
        'status_code': 0, 
        'data': result,
        'info': f'获取知识库 DocID 的分段列表 Success ！!'
    }



@timed_request
@app.route(BASE_URL + '/delParagraphs', methods=['DELETE'])
def del_paragraph():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    dataset_id = json_data.get('dataset_id','')
    doc_id = json_data.get('doc_id','')
    para_id = json_data.get('para_id','')
    from cdify.api.dbs.doc_actions import del_para_in_doc
    response = del_para_in_doc(dataset_id=dataset_id,doc_id=doc_id,seg_id=para_id)
    if 'false' in response:
        return {'status_code': -1, 'data': response, 'info': 'Delete Paragraph failed',}
    return {
        'status_code': 0, 
        'data': response, 
        'info': 'Delete Paragraph successful!'
    }



"""
curl --location --request POST 'http://10.0.15.21/v1/datasets/{dataset_id}/documents/{document_id}/update-by-text' \
--header 'Authorization: Bearer {api_key}' \
--header 'Content-Type: application/json' \
--data-raw '{"name": "name","text": "text"}'
"""

# @timed_request
# @app.route(BASE_URL + '/updateDocWithText', methods=['POST'])
# def update_doc_with_text():
#     data = request.get_data()
#     json_data = json.loads(data.decode("utf-8"))
#     dataset_id = json_data.get('dataset_id','')
#     doc_id = json_data.get('doc_id','')
#     para_id = json_data.get('para_id','')
#     from cdify.api.dbs.doc_actions import del_para_in_doc
#     response = del_para_in_doc(dataset_id=dataset_id,doc_id=doc_id,seg_id=para_id)
#     # if 'false' in response


@timed_request
@app.route(BASE_URL + '/addParagraph', methods=['POST'])
def add_paragraph():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    dataset_id = json_data.get('dataset_id', '')
    doc_id = json_data.get('doc_id', '')
    keywords = json_data.get('keywords', []) # 关键字信息，非必填
    content = json_data.get('content', '')
    if not content:
        return {'status_code': -1, 'data': response, 'info': '请输入要更新的内容',}
    
    # 验证指定 doc_id 是什么类型并完整封装 params 参数
    
    from cdify.api.dbs.db_list import get_db_doc_list
    response = get_db_doc_list(dataset_id=dataset_id)
    docs = json.loads(response.text)['data']
    target_doc_type = ''
    for doc in docs:
        if doc_id == doc['id']:
            target_doc_type = doc['doc_form']
            break
    
    answer = json_data.get('answer', '')
    if target_doc_type == 'qa_model' and not answer:
        return {'status_code': -1, 'data': response, 'info': '当前待add paragraph 的 doc 是 Q-A 文档，必须传入 anser 答案信息 !',}

    temp_data = []
    temp_data.append({
        'content': content,
        'answer': answer,
        'keywords': keywords
    })

    params = {}
    params['data'] = {'segments': temp_data}
    from cdify.api.dbs.doc_actions import add_content_2_doc
    response = add_content_2_doc(dataset_id,doc_id,params['data'])
    if response.status_code != 200:    
        return {'status_code': -1, 'data': "", 'info': '向知识库的文档添加文本段落失败 ！'}

    try:
        data_response = json.loads(response.text)
        return {
            'status_code': 0, 
            'data': data_response, 
            'info': '向知识库的文档添加文本段落成功!'
        }
    except Exception as e:
        return {'status_code': -1, 'data': "", 'info': '向知识库的文档添加文本段落失败, 由于API响应结果 json 序列化失败导致 ！'}


    


    


# =========================================================================================================



"""
curl --location --request POST 'http://10.0.15.21/v1/datasets/{dataset_id}/retrieve' \
--header 'Authorization: Bearer {api_key}'\
--header 'Content-Type: application/json'\
--data-raw '{
  "query": "test",
  "retrieval_model": {
      "search_method": "keyword_search",
      "reranking_enable": false,
      "reranking_mode": null,
      "reranking_model": {
          "reranking_provider_name": "",
          "reranking_model_name": ""
      },
      "weights": null,
      "top_k": 1,
      "score_threshold_enabled": false,
      "score_threshold": null,
      "metadata_filtering_conditions": {
          "logical_operator": "and",
          "conditions": [
              {
                  "name": "document_name",
                  "comparison_operator": "contains",
                  "value": "test"
              }
          ]
      }
  }
}'
"""
@timed_request
@app.route(BASE_URL + '/dbRetrieval', methods=['POST'])
def retrieval_db():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    dataset_id = json_data.get('dataset_id', '')
    query = json_data.get('query', '')
    if not query or not dataset_id:
        return {'status_code': -1, 'data': "", 'info': '知识库ID or Query 参数信息为空'}
    
    search_method = json_data.get('search_method', 'semantic_search') # 默认语义检索， 还有 keyword_search、full_text_search、hybrid_search  混合检索
    reranking_enable = json_data.get('reranking_enable', False) # 如果检索模式为 semantic_search 模式或者 hybrid_search 则传值，说明用到向量时必有排序发生
    # print(reranking_enable)
    reranking_mode = {
        'reranking_provider_name' : json_data.get('reranking_provider_name', reranking_provider_name_config),
        'reranking_model_name' : json_data.get('reranking_provider_name', reranking_model_name_config)
    }
    weight =  json_data.get('weight', 0.7)
    top_k = json_data.get('top_k', 5)
    score_threshold_enabled = json_data.get('score_threshold_enabled', True) # 默认保持 false，否则很难召回
    score_threshold = json_data.get('score_threshold', 0.1)
    metadata_filtering_conditions = {}

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
            'metadata_filtering_conditions': metadata_filtering_conditions
        },

    }

    from cdify.api.dbs.doc_actions import retrieval
    response = retrieval(dataset_id, params)
    if response.status_code != 200:    
        return {'status_code': -1, 'data': "", 'info': '知识库检索失败 ！'}
    
    data_response = json.loads(response.text)
    return {
        'status_code': 0, 
        'data': data_response, 
        'info': '知识库检索失败!'
    }







@timed_request
@app.route(BASE_URL + '/chat', methods=['POST'])
def start_chat():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))

    # params check
    user_id = json_data.get('user_id', '') # hanwei-cdify
    if not user_id:
        return {'status_code': -1, 'info': 'No user_id provided', 'data': "No user_id provided",}
    
    conversation_id = json_data.get('conversation_id','')
    # todo 这里需要新增对话轮次的判断，保证 conversation id 的信息是有效的
    # json_data['conversation_id'] = ...
    
    query = json_data.get('query', '')
    # todo 这里需要修正，新增一下判断轮次后，对话默认信息的设定
    query = "你好。你是谁？" if not query else ...
    # json_data['query'] = ...

    # logger.info("====================================== chat 2 db log")

    """ 发送聊天请求 with conversation_id """
    from cdify.api.chat.chat import start_chat
    response = start_chat(data_new=json_data)

    if response.status_code != 200:
        return {'status_code': -1, 'data': "request chat failed", 'info': '可能是服务器或网络异常，请检查网络或者服务器GPU模型是否正常运行！'}

    response = json.loads(response.text)  # chat server 完整返回的所有字段请参考 tools.py 中的 chat_return_all_columns
    message_id = response.get('message_id')
    conversation_id = response.get('conversation_id')
    try:
        answer = json.loads(response.get('answer'))    
    except json.JSONDecodeError:
        ...
    return {
        'status_code': 0,
        'data': {
            'conversation_id': conversation_id,
            'message_id': message_id,
            'answer': answer
        },
        'info': 'request chat info successful!'
    }







if __name__ == '__main__':
    # logger.info("日志系统初始化成功！ Server Running...")

    app.run(debug=True, host='0.0.0.0', port=5611)
    # app.run(debug=True, host='0.0.0.0', port=2569)
