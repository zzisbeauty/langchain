
# 封装 create db 时需要进一步修改的参数
def _struct_parasm(
        indexing_technique,embedding_model_name,embedding_provider_name,
        reranking_enable,reranking_mode,reranking_provider_name,reranking_model_name,
        score_threshold_enabled,score_threshold,search_method,top_k,weights
    ):
    """ 特殊指定下，封装 db edit 参数 """
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
                # "keyword_setting":{ # vector 和 keywords 应该互补
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
    return params_data


# 过滤 api addParagraph 的响应结果
def filter_insert_response(response: dict) -> dict:
    """
    根据返回的 doc_form 类型筛选并简化返回结构
    支持 text_model 和 qa_model
    """
    if not response or "data" not in response or "data" not in response["data"]:
        return {"error": "Invalid response format"}

    doc_form = response["data"].get("doc_form")
    raw_items = response["data"]["data"]
    filtered_items = []

    for item in raw_items:
        base_item = {
            "id": item.get("id"),
            "content": item.get("content"),
            "document_id": item.get("document_id"),
            "keywords": item.get("keywords")
        }

        # QA模型多一个字段
        if doc_form == "qa_model":
            base_item["answer"] = item.get("answer")

        filtered_items.append(base_item)

    return {
        "data": filtered_items,
        "doc_form": doc_form,
        "info": response.get("info"),
        "status_code": response.get("status_code")
    }







# =========================================================
    """
    api: 适配 API getDbDocParasListnsertTypeFile2DB
    """
# =========================================================
def convert_dify_to_ragflow_structure4(dify_list, keywords=None, message="success"):
    """
    将 Dify 的段落列表格式转换为 Ragflow 风格返回。
    - keywords 可以是 str 或 list
    - 如果 keywords 为空或 None，不做过滤，返回所有段落
    - question_kwd 字段始终是空列表
    """
    # 统一 keywords 参数为列表
    if keywords is None:
        keywords_list = []
    elif isinstance(keywords, str):
        keywords_list = [keywords.strip()] if keywords.strip() else []
    elif isinstance(keywords, list):
        keywords_list = [kw.strip() for kw in keywords if kw.strip()]
    else:
        keywords_list = []

    chunks = []
    for item in dify_list:
        item_keywords = item.get("keywords", [])

        # 如果用户真的传了非空关键字过滤条件，就只保留命中的
        if keywords_list:
            if not any(kw in item_keywords for kw in keywords_list):
                continue

        # 拼接 content 和 answer
        content = item.get("content", "")
        answer = item.get("answer", "")
        content_with_weight = f"{content}\n{answer}" if answer else content

        # 构造 ragflow 风格的 chunk
        chunk = {
            "available_int": 1,
            "chunk_id": item.get("id", ""),
            "content_with_weight": content_with_weight,
            "doc_id": item.get("document_id", ""),
            "docnm_kwd": "",
            "image_id": "",
            "important_kwd": item_keywords,
            "positions": [],
            "question_kwd": []   # 一定为空
        }
        chunks.append(chunk)

    # 返回 ragflow 风格完整结构
    result = {
        "code": 0,
        "data": {
            "chunks": chunks,
            "doc": {},
            "total": len(chunks)
        },
        "message": message
    }
    return result


# =========================================================
    """
    api insertTypeFile2DB
    """
# =========================================================
import json

def wrap_insert_file_response(original_response: dict) -> dict:
    """
    接收整个原始响应，保留 info 和 status_code， 只替换处理过的 data 字段
    """
    raw_data_str = original_response.get("data")
    if not raw_data_str:
        # 没有 data 字段，就原样返回
        return original_response
    try:
        # 转义字符串反序列化
        parsed_data = json.loads(raw_data_str)
    except json.JSONDecodeError:
        # 如果解析失败，也原样返回
        return original_response

    document = parsed_data.get("document", {})
    batch = parsed_data.get("batch")

    # 过滤后的必要字段
    filtered_data = {
        "id": document.get("id"),
        "name": document.get("name"),
        # "size": document.get("size"),
        # "extension": document.get("extension"),
        "doc_form": document.get("doc_form"),
    }
    new_data = {
        "document": filtered_data,
        "batch": batch
    }
    # 返回结构和原始一致，只换掉 data
    return {
        **original_response,
        "data": new_data
    }


import json

def convert_dify_upload_response_to_ragflow_format(dify_response: dict) -> dict:
    DEFAULT_PARSER_CONFIG = {
        "pages": [[]]
    }

    # dify 的 data 是字符串
    dify_data_raw = dify_response.get("data", "{}")
    dify_data = json.loads(dify_data_raw)

    doc = dify_data.get("document", {})
    data_source_info = doc.get("data_source_info", {})
    data_source_detail = doc.get("data_source_detail_dict", {}).get("upload_file", {})

    ragflow_item = {
        "created_by": doc.get("created_by", ""),
        "id": doc.get("id", ""),
        "kb_id": data_source_info.get("upload_file_id", ""),
        "location": "",
        "name": doc.get("name", ""),
        "parser_config": DEFAULT_PARSER_CONFIG,
        "parser_id": "naive",
        "size": data_source_detail.get("size", 0),
        "thumbnail": "",
        "type": data_source_detail.get("extension", "")
    }

    return {
        "code": 0,
        "data": [ragflow_item],
        "message": "success"
    }






# =========================================================
    """
    api 获取 document list
    """
# =========================================================
def convert_dify_doc_list_response_to_ragflow_format(dify_response: dict) -> dict:
    DEFAULT_PARSER_CONFIG = {
        "pages": [None]
    }

    docs = []
    dify_data = dify_response.get("data", {})

    for kb_id, doc_list in dify_data.items():
        for item in doc_list:
            for doc_id, doc_info in item.items():
                name, doc_form = doc_info
                doc = {
                    "chunk_num": 0,
                    "create_date": "",
                    "create_time": 0,
                    "created_by": "",
                    "id": doc_id,
                    "kb_id": kb_id,
                    "location": "",
                    "meta_fields": {},
                    "name": name,
                    "parser_config": DEFAULT_PARSER_CONFIG,
                    "parser_id": "naive",
                    "process_begin_at": None,
                    "process_duation": 0,
                    "progress": 0,
                    "progress_msg": "",
                    "run": "",
                    "size": 0,
                    "source_type": "",
                    "status": "",
                    "thumbnail": "",
                    "token_num": 0,
                    "type": doc_form,
                    "update_date": "",
                    "update_time": 0
                }
                docs.append(doc)

    return {
        "code": 0,
        "data": {
            "docs": docs,
            "total": len(docs)
        },
        "message": "success"
    }














# =========================================================
    """
    api insertText2DB
    """
# =========================================================
def wrap_insert_text_response(original_response: dict) -> dict:
    """
    接收整个原始响应，保留 info 和 status_code，
    只替换处理过的 data 字段
    - 如果 data 是字符串，会自动转成 dict
    """
    raw_data = original_response.get("data")
    if not raw_data:
        return original_response

    # 如果 data 是字符串（比如 FILE 响应），先转成 dict
    if isinstance(raw_data, str):
        try:
            raw_data = json.loads(raw_data)
        except json.JSONDecodeError:
            # 不是有效JSON就原样返回
            return original_response

    document = raw_data.get("document", {})
    batch = raw_data.get("batch")
    if not document:
        return original_response

    # 保留的字段
    filtered_data = {
        "id": document.get("id"),
        "name": document.get("name"),
        "doc_form": document.get("doc_form")
    }
    new_data = {
        "document": filtered_data,
        "batch": batch
    }
    # 保留 info 和 status_code
    return {
        **original_response,
        "data": new_data
    }




# =========================================================
    """
    api createDb
    """
# =========================================================
def wrap_create_db_response(original_response: dict) -> dict:
    """
    创建知识库接口响应包装器
    - 保留必要字段
    - info / status_code 不动
    - data 字段裁剪
    """
    raw_data = original_response.get("data")
    if not raw_data or not isinstance(raw_data, dict):
        return original_response

    filtered_data = {
        "id": raw_data.get("id"),
        "name": raw_data.get("name"),
        "description": raw_data.get("description"),
        # "embedding_model": raw_data.get("embedding_model"),
        # "embedding_model_provider": raw_data.get("embedding_model_provider"),
        # "indexing_technique": raw_data.get("indexing_technique"),
        # "permission": raw_data.get("permission"),
        # "created_by": raw_data.get("created_by"),
        # "updated_by": raw_data.get("updated_by"),
        # "created_at": raw_data.get("created_at"),
        # "updated_at": raw_data.get("updated_at"),
        # "retrieval_model_dict": raw_data.get("retrieval_model_dict"),
        # "word_count": raw_data.get("word_count"),
        # "document_count": raw_data.get("document_count"),
    }

    new_response = original_response.copy()
    new_response["data"] = filtered_data
    return new_response







# =========================================================
    """
    统一处理知识库详情或列表响应，只保留关键字段。
    """
# =========================================================
def wrap_dataset_info_response(response: dict) -> dict:
    essential_keys = [
        "id", "name", "description", "doc_form", "data_source_type",
        "document_count", "word_count", "created_by", "created_at",
        "updated_by", "updated_at", "embedding_model", "embedding_model_provider"
    ]

    def filter_fields(item: dict) -> dict:
        return {k: item.get(k) for k in essential_keys}

    original_data = response.get("data")

    if isinstance(original_data, list):
        # 知识库列表情况
        filtered_data = [filter_fields(item) for item in original_data]
    elif isinstance(original_data, dict):
        # 单个知识库详情
        filtered_data = filter_fields(original_data)
    else:
        filtered_data = None  # 防止 data 异常结构

    return {
        "status_code": response.get("status_code", -1),
        "info": response.get("info", ""),
        "data": filtered_data
    }


def convert_dify_response_to_ragflow_format(dify_response: dict) -> dict:
    def convert_item(item: dict) -> dict:
        # 组装 embd_id
        embd_id = f"{item.get('embedding_model', '')}@{item.get('embedding_model_provider', '')}"
        return {
            "avatar": "",
            "chunk_num": 0,  # dify 无 chunk 字段，可设置为 0 或估算
            "description": item.get("description", ""),
            "doc_num": item.get("document_count", 0),
            "embd_id": embd_id,
            "id": item.get("id", ""),
            "language": "Chinese",  # dify 无语言字段，默认填一个
            "name": item.get("name", ""),
            "parser_id": "naive",  # dify 无 parser 字段，默认填一个
            "permission": item.get("permission", "only_me"),
            "token_num": item.get("word_count", 0),  # 直接使用 word_count 近似 token
            "update_time": item.get("updated_at", 0)
        }

    ragflow_kbs = [convert_item(item) for item in dify_response.get("data", [])]
    return {
        "code": 0,
        "data": {
            "kbs": ragflow_kbs,
            "total": len(ragflow_kbs)
        },
        "message": "success"
    }






# =========================================================
    """
    查询知识库详情信息
    """
# =========================================================

def convert_dify_detail_response_to_ragflow_format(dify_response: dict) -> dict:
    DEFAULT_PARSER_CONFIG = {
        "graphrag": {
            "community": True,
            "entity_types": [],
            "method": "",
            "resolution": True,
            "use_graphrag": True
        },
        "layout_recognize": ""
    }

    dify_data = dify_response.get("data", {})
    embd_id = f"{dify_data.get('embedding_model', '')}@{dify_data.get('embedding_model_provider', '')}"

    ragflow_data = {
        "auth_list": [],
        "avatar": "",
        "chunk_num": 0,
        "description": dify_data.get("description", ""),
        "doc_num": dify_data.get("document_count", 0),
        "embd_id": embd_id,
        "id": dify_data.get("id", ""),
        "language": "Chinese",
        "manager_list": [],
        "name": dify_data.get("name", ""),
        "pagerank": 0,
        "parser_config": DEFAULT_PARSER_CONFIG,
        "parser_id": "naive",
        "permission": dify_data.get("permission", "only_me"),
        "token_num": dify_data.get("word_count", 0)
    }

    return {
        "code": 0,
        "data": ragflow_data,
        "message": "success"
    }







# =========================================================
    """
    编辑知识库详情信息
    """
# =========================================================
# api editDbProperty
def wrap_edit_db_response(resp: dict) -> dict:
    """
    处理“编辑知识库”接口的响应，把 data 里的 json 字符串转 dict
    并保留必要字段
    """
    raw_data_str = resp.get("data", "{}")
    raw_data = json.loads(raw_data_str)

    retrieval_model = raw_data.get("retrieval_model_dict", {})

    filtered_data = {
        "id": raw_data.get("id"),
        "name": raw_data.get("name"),
        "description": raw_data.get("description"),
        "document_count": raw_data.get("document_count"),
        "word_count": raw_data.get("word_count"),
        "embedding_model": raw_data.get("embedding_model"),
        "indexing_technique": raw_data.get("indexing_technique"),
        "retrieval_model": {
            "search_method": retrieval_model.get("search_method"),
            "top_k": retrieval_model.get("top_k"),
            "score_threshold_enabled": retrieval_model.get("score_threshold_enabled"),
            "score_threshold": retrieval_model.get("score_threshold"),
        }
    }

    # 替换掉原来的data字段
    resp["data"] = filtered_data
    return resp



import json

def convert_dify_update_response_to_ragflow_format(dify_response: dict) -> dict:
    DEFAULT_PARSER_CONFIG = {
        "auto_keywords": 0,
        "auto_questions": 0,
        "graphrag": {
            "entity_types": [],
            "method": "",
            "resolution": True,
            "use_graphrag": True
        },
        "layout_recognize": "",
        "raptor": {
            "use_raptor": True
        }
    }

    # dify 返回里的 data 是一个 JSON string
    dify_data_raw = dify_response.get("data", "{}")
    dify_data = json.loads(dify_data_raw)

    # 拼接 embd_id
    embd_id = f"{dify_data.get('embedding_model', '')}@{dify_data.get('embedding_model_provider', '')}"

    # 取 retrieval_model_dict 的深层字段
    retrieval_model = dify_data.get("retrieval_model_dict", {})
    score_threshold = retrieval_model.get("score_threshold", 0)
    weights = retrieval_model.get("weights", {})
    vector_setting = weights.get("vector_setting", {})
    vector_weight = vector_setting.get("vector_weight", 0)

    # 构建 ragflow 的 data 部分
    ragflow_data = {
        "avatar": "",
        "chunk_num": 0,
        "create_date": "",  # 可以根据 created_at 格式化，如果要
        "create_time": dify_data.get("created_at", 0),
        "created_by": dify_data.get("created_by", ""),
        "description": dify_data.get("description", ""),
        "doc_num": dify_data.get("document_count", 0),
        "embd_id": embd_id,
        "id": dify_data.get("id", ""),
        "language": "Chinese",
        "name": dify_data.get("name", ""),
        "pagerank": 0,
        "parser_config": DEFAULT_PARSER_CONFIG,
        "parser_id": "naive",
        "permission": dify_data.get("permission", "only_me"),
        "similarity_threshold": score_threshold,
        "status": "",
        "tenant_id": "",
        "token_num": dify_data.get("word_count", 0),
        "update_date": "",
        "update_time": dify_data.get("updated_at", 0),
        "vector_similarity_weight": vector_weight
    }
    return {
        "code": 0,
        "data": ragflow_data,
        "message": "success"
    }



# =========================================================
    """
    dbRetrieval
    """
# =========================================================

def wrap_knowledge_search_response(response: dict) -> dict:
    """
    包装器：保留查询的 query 和每条命中记录的必要字段
    """
    raw_data = response.get("data", {})
    query_text = raw_data.get("query", {}).get("content", "")
    raw_records = raw_data.get("records", [])

    new_records = []
    for rec in raw_records:
        segment = rec.get("segment", {})
        document = segment.get("document", {})

        new_record = {
            "score": rec.get("score"),
            "content": segment.get("content"),
            "answer": segment.get("answer"),
            "document": {
                "id": document.get("id"),
                "name": document.get("name")
            }
        }
        new_records.append(new_record)

    # 替换处理后的 data 字段
    new_data = {
        "query": query_text,
        "records": new_records
    }

    # 构造新的响应
    return {
        **response,
        "data": new_data
    }





# =========================================================
    """
    docProcess
    """
# =========================================================
def wrap_check_text_processing_progress_response(resp: dict) -> dict:
    """
    包装器函数：处理「查询文本处理进度」接口响应
    只保留关键字段
    """
    if (
        "data" in resp
        and "data" in resp["data"]
        and isinstance(resp["data"]["data"], list)
    ):
        cleaned_list = []
        for item in resp["data"]["data"]:
            cleaned_item = {
                "id": item.get("id"),
                "indexing_status": item.get("indexing_status"),
                "processing_started_at": item.get("processing_started_at"),
                "parsing_completed_at": item.get("parsing_completed_at"),
                "splitting_completed_at": item.get("splitting_completed_at"),
                "cleaning_completed_at": item.get("cleaning_completed_at"),
                "completed_at": item.get("completed_at"),
                "total_segments": item.get("total_segments"),
                "completed_segments": item.get("completed_segments"),
                "error": item.get("error"),
            }
            cleaned_list.append(cleaned_item)

        # 替换掉原始 data
        resp["data"] = {"data": cleaned_list}

    return resp
