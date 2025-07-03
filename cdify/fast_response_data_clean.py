
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




# 适配 API getDbDocParasList
def transform_response_data(response: dict) -> dict:
    new_response = response.copy()
    data = response.get("data")
    if not data:
        # data 为空或 None，直接返回原结构
        return new_response
    new_data = {}
    for key, val in data.items():
        # val 应该是一个列表，里面元素是三元组列表
        if not isinstance(val, list):
            new_data[key] = val
            continue

        converted_list = []
        for item in val:
            if isinstance(item, list) and len(item) == 3:
                content, keywords, para_id = item
                converted_list.append({
                    "content": content,
                    "keywords": keywords,
                    "para_id": para_id
                })
        new_data[key] = converted_list

    new_response["data"] = new_data
    return new_response





# api insertTypeFile2DB

import json

def wrap_insert_file_response(original_response: dict) -> dict:
    """
    接收整个原始响应，保留 info 和 status_code，
    只替换处理过的 data 字段
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


# api insertText2DB
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



# api createDb
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



#  api dbList \ dbInfo 
# def wrap_db_list_response(resp: dict) -> dict:
#     """
#     处理“查询DB列表”的接口响应，只保留最关键信息
#     """
#     raw_list = resp.get("data", [])
#     new_list = []

#     for db in raw_list:
#         retrieval_model = db.get("retrieval_model_dict", {})
#         new_list.append({
#             "id": db.get("id"),
#             "name": db.get("name"),
#             "description": db.get("description"),
#             "document_count": db.get("document_count"),
#             "word_count": db.get("word_count"),
#             "embedding_model": db.get("embedding_model"),
#             "indexing_technique": db.get("indexing_technique"),
#             "retrieval_model": {
#                 "search_method": retrieval_model.get("search_method"),
#                 "top_k": retrieval_model.get("top_k"),
#                 "score_threshold_enabled": retrieval_model.get("score_threshold_enabled"),
#                 "score_threshold": retrieval_model.get("score_threshold"),
#             }
#         })

#     # 替换掉原来的 data
#     resp["data"] = new_list
#     return resp

def wrap_dataset_info_response(response: dict) -> dict:
    """
    统一处理知识库详情或列表响应，只保留关键字段。
    """
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



# api  dbRetrieval
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



# API docProcess
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
