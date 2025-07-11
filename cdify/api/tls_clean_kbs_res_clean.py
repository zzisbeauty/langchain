# =========================================================
""" 统一处理DIFY API 响应详情，只保留关键字段，以便和 1.0 api 对齐 response """
# =========================================================

import json


# def wrap_dataset_info_response(response: dict) -> dict:
#     essential_keys = [
#         "id", "name", "description", "doc_form", "data_source_type",
#         "document_count", "word_count", "created_by", "created_at",
#         "updated_by", "updated_at", "embedding_model", "embedding_model_provider"
#     ]

#     def filter_fields(item: dict) -> dict:
#         return {k: item.get(k) for k in essential_keys}

#     original_data = response.get("data")

#     if isinstance(original_data, list):
#         # 知识库列表情况
#         filtered_data = [filter_fields(item) for item in original_data]
#     elif isinstance(original_data, dict):
#         # 单个知识库详情
#         filtered_data = filter_fields(original_data)
#     else:
#         filtered_data = None  # 防止 data 异常结构

#     return {
#         "status_code": response.get("status_code", -1),
#         "info": response.get("info", ""),
#         "data": filtered_data
#     }


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



# 查询知识库详情信息
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




# 处理“编辑知识库”接口的响应，把 data 里的 json 字符串转 dict 并保留必要字段
def wrap_edit_db_response(resp: dict) -> dict:
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