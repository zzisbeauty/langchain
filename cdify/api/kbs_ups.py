from flask import Blueprint, request, jsonify
from cdify.utils.config import *
from cdify.utils.generals import *
from cdify.utils.decorators import timed_request
from werkzeug.utils import secure_filename

kbs_kbup = Blueprint('kbs_kbup', __name__)

# # 只支持本地文件的方案
# @kbs_kbup.route(BASE_URL + '/document/upload', methods=['POST'])
# @timed_request
# def insert_type2db():
#     data = request.get_data()
#     json_data = json.loads(data.decode("utf-8"))
#     dataset_id = json_data.get('kb_id','')
#     file_path = json_data.get('file','')
#     file_name = json_data.get('file_name','')
#     if not dataset_id:
#         return  {'code': -1, 'data': "", 'message': '请指定知识库ID'}
#     try:
#         _ = open(file_path,'rb').close()
#     except:
#         return  {'code': -1, 'data': "", 'message': '文件读取失败，检查文件路径'}
#     if not file_name:
#         file_name = get_filename(file_path=file_path)

#     mode = json_data.get('mode','custom')  # automatic
#     separator = json_data.get('separator', '\n')
#     max_tokens = json_data.get('max_tokens', 1000)
#     remove_urls_emails = json_data.get('remove_urls_emails', True)
#     indexing_technique = json_data.get('indexing_technique', 'high_quality')
#     doc_form = json_data.get('doc_form', 'text_model')  # 此模式为默认； 还有 qa_model 模式
#     # if doc_form == 'qa_model':
#     doc_language = json_data.get('doc_language', 'Chinese')

#     data_json = {
#         "indexing_technique": indexing_technique,
#         'doc_form': doc_form,
#         'doc_language': doc_language,
#         "process_rule": {
#             "rules": {
#                 "pre_processing_rules": [
#                     {"id": "remove_extra_spaces", "enabled": True},
#                     {"id": "remove_urls_emails", "enabled": remove_urls_emails}
#                 ],
#                 "segmentation": {
#                     "separator": separator,
#                     "max_tokens": max_tokens
#                 }
#             },
#             "mode": mode
#         }
#     }
#     data_json = json.dumps(data_json)
#     from cdify.dify_client.kbs_ups import upload_file_with_metadata
#     response = upload_file_with_metadata(db_id=dataset_id, file_name=file_name, file_path=file_path, data_json=data_json)
#     if response.status_code != 200:
#         return {'status_code': -1, 'data': "",  'info': '导入数据失败，请检查参数或和开发联调'}
#     temp_return = {'status_code': 0, 'data': response.text,  'info': f'导入FILE数据到知识库 {dataset_id} 成功!'}
#     # return temp_return

#     # from cdify.api.clean_response import wrap_insert_file_response
#     # return wrap_insert_file_response(temp_return)
#     from cdify.api.tls_clean_response import convert_dify_upload_response_to_ragflow_format
#     return convert_dify_upload_response_to_ragflow_format(temp_return)

import os
import json
import tempfile
from werkzeug.utils import secure_filename


@kbs_kbup.route(BASE_URL + '/document/upload', methods=['POST'])
@timed_request
def insert_type2db():
    try:
        dataset_id = request.form.get('kb_id')
        if not dataset_id:
            return jsonify({'code': -1, 'message': '缺少 kb_id'}), 400
        if 'file' not in request.files:
            return jsonify({'code': -1, 'message': '缺少 file 字段'}), 400        
        
        # 确定上传的文件名
        file_obj = request.files['file']
        file_name = file_obj.filename
        print('--------------------------------------------------',file_name)
        if not os.path.splitext(file_name)[1] and file_obj.filename:  
            original_ext = os.path.splitext(file_obj.filename)[1]  
            file_name = file_name + original_ext  
        # print(f"处理后的文件名: {file_name}")  

        # # 保存文件到临时目录
        # filename = secure_filename(file_name)
        # temp_dir = tempfile.gettempdir()
        # temp_file_path = os.path.join(temp_dir, filename)
        # file_obj.save(temp_file_path)
        file_content = file_obj.read()

        # 其他参数
        mode = request.form.get('mode', 'custom')
        separator = request.form.get('separator', '\n')
        max_tokens = int(request.form.get('max_tokens', 1000))
        remove_urls_emails = request.form.get('remove_urls_emails', 'true').lower() == 'true'
        indexing_technique = request.form.get('indexing_technique', 'high_quality')
        doc_form = request.form.get('doc_form', 'text_model')
        doc_language = request.form.get('doc_language', 'Chinese')

        # 构造 data_json
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
        data_json_str = json.dumps(data_json, ensure_ascii=False)

        from cdify.dify_client.kbs_ups import upload_file_with_metadata
        response = upload_file_with_metadata(
            db_id=dataset_id, 
            file_name=file_name,
            # file_path=temp_file_path, # 不做文件的临时存储
            file_path=file_content, # 直接传输内容
            data_json=data_json_str
        )
        if response.status_code != 200:
            return jsonify({'status_code': -1, 'data': "", 'info': '导入数据失败，请检查参数'}), 500

        temp_return = {'status_code': 0,'data': response.text,'info': f'导入FILE数据到知识库 {dataset_id} 成功!'}
        # return temp_return
        from cdify.api.tls_clean_response import convert_dify_upload_response_to_ragflow_format
        return convert_dify_upload_response_to_ragflow_format(temp_return)

    except Exception as e:
        print(f"❌ 请求处理失败: {str(e)}")
        return jsonify({'code': -1, 'message': f'服务器内部错误: {str(e)}'}), 500











@kbs_kbup.route(BASE_URL + '/txt/input', methods=['POST'])
@timed_request
def insert_txt2db():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    indexing_technique = json_data.get('indexing_technique', "high_quality") # "economy" or "high_quality" 索引方式，建议保持默认值；
    top_k = json_data.get('top_k', 3) # 召回数量，精确场景下，不大于 2；其他低精度场景建议 3~5 个；有 rerank 模型时可以大一些
    search_method = json_data.get('search_method', "hybrid_search") # 默认为混合检索  # semantic_search 语义检索  # full_text_search 全文检索
    weighted_score = json_data.get('weighted_score', 0.7) # 混合检索需要配置语义检索权重 
    score_threshold = json_data.get('score_threshold', 0.8)
    # base params
    file_name = json_data.get('file_name','')
    text = json_data.get('text','')
    dataset_id = json_data.get('kb_id','')

    # /////////////////// test parameters
    # json_data['dataset_id'] = 'd6142a1d-ff1b-470c-84b8-9b6f570f95d9' # test
    # file_name = "鲁迅杂文-《且介亭杂文》-long-16-58", # test
    # text = text_demo_long  # test
    if not file_name or not text or not dataset_id:
        return {'code': -1, 'data': "", 'message': '当前【文件名】【文本信息】【数据库ID】存在空，请检查性'}

    mode = json_data.get('mode','custom') # custom 参数将会触发一系列的文档清洗解析参数设置； automatic 根据默认参数执行嵌入和索引
    
    # 索引内容的形式 ，默认为文本形式的内容嵌入； 此类数据默认采用经济模式进行索引构建 ， 默认 text_model，还有如下两种
    # # qa_model ： text_model 模式还可以进一步转变为文本片段创建 Q-A 内容并完成嵌入，同时支持language setting，那么此时就要选择此模式
    # # hierarchical_model ： 结构化模式内容的嵌入
    doc_form = json_data.get('doc_form','text_model')  # qa_model
    # doc_form = json_data.get('doc_form','qa_model')
    doc_language = json_data.get('doc_language', 'Chinese') # 当要被清洗的数据要被整理成 qa 时，需要指定该参数， 非 qa_model 时，此参数无效

    # # 无论何种 doc_form，都需要如下通用分割模式参数
    remove_extra_spaces = json_data.get('remove_extra_spaces', True)
    remove_urls_emails = json_data.get('remove_urls_emails', True)
    separator = json_data.get('separator', '\n')  # 分隔符
    max_tokens = json_data.get('max_tokens', 1000) # 每段最大 token 数
    chunk_overlap = json_data.get('chunk_overlap', 300)

    # 另外当 doc_form == hierarchical_model 时，分为如下两种情况
    parent_mode = json_data.get('parent_mode', "full-doc") #  情况 1 此时无需额外参数配置
    # parent_mode = json_data.get('parent_mode', "paragraph") # 情况 2 此时需要如下额外参数
    separator_sub = json_data.get('separator_sub', "\n")
    max_tokens_sub = json_data.get('max_tokens_sub', 500) # 需要保证小于 max_tokens
    if (doc_form == "hierarchical_model") and (max_tokens_sub >= max_tokens):
        # logger.error(f"当前待索引内容形式为 {doc_form}, 此时 max_tokens_sub 禁止大于 max_tokens，请调整")
        max_tokens_sub = max_tokens
    if doc_form == "qa_model":
        # logger.info(f'当前采用 QA 模式，如果计算资源低，此模式相对耗时且会显著增加 token 消耗！')
        ...
    
    def readme():
        """
        # 补充 doc_form 为 hierarchical_model 进行清洗与数据前处理时，结构化文本处理方式的基础选择标准：
        # 1. paragraph 模式按段落划分为父块：
        #    将整个文档作为一个整体进行召回（不切分）
        #    适合需要 “整篇理解” 的文档，如法律合同、报告; FAQ、政策文件，整体性强的文档
        # 2. full-doc 整篇当父块，
        #    适合需要整体检索的场景; full-doc 在检索时不会分割内容，但索引方式仍支持子块； 文档每一段落作为父级分段
        #    每个段落为一个召回单位; 更细粒度的召回，适合知识点分布较广的文档; 结构松散、信息点分散的资料，例如日报、聊天记录
        """

    embedding_model = json_data.get('embedding_model', embedding_model_config)
    embedding_model_provider = json_data.get('embedding_model_provider', embedding_model_provider_config)
    reranking_enable = json_data.get('reranking_enable', False) # 依赖配置 rerank 模型；如果是高精度场景，召回数量应设置小一点，rerank 可以不配置，如果是 True，必须配置 rerank model
    # reranking_model_name = json_data.get('reranking_model_name', reranking_model_name_config)
    reranking_model_name = ""
    # reranking_provider_name = json_data.get('reranking_provider_name', reranking_provider_name_config)
    reranking_provider_name = ""

    # ==== 检索与召回 config
    score_threshold_enabled = json_data.get('score_threshold_enabled', False) # 是否开启语义召回分数限制，默认值为 False；如果对于召回精度要求不严格，可不用调整
    if score_threshold_enabled:
        if score_threshold > 1 or score_threshold < 0:
            # logger.warning(f'score_threshold 必须在 0~1 之间，当前 score_threshold 设置为： {score_threshold},已经将 score_threshold 恢复为默认值 0.8')
            json_data['score_threshold'] = 0.8

    # ==== base params to dify client
    params_data = {
        "name": file_name,
        "text": text,
        "doc_form": doc_form,
        "doc_language": doc_language,
        "indexing_technique": indexing_technique,
        "embedding_model" :embedding_model,
        "embedding_model_provider": embedding_model_provider,
    }

    # ==== 配置嵌入之前的核心参数信息 to dify' client kernel params
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
    
    from cdify.dify_client.kbs_ups import requests_create_dataset_with_txt
    response = requests_create_dataset_with_txt(dataset_id, params_data)
    if response.status_code != 200:
        return {'code': -1, 'data': "",  'message': '导入数据失败，请检查参数合理性'}
    temp_return = {'code': 0, 'data': response.text, 'message': f'导入TXT数据到知识库 {dataset_id} 成功!'}
    # return temp_return

    from cdify.api.tls_clean_response import wrap_insert_text_response
    return wrap_insert_text_response(temp_return)
