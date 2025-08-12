import json


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



# clean get kb ---> doc ---> chunk list api reponse
def convert_dify_to_ragflow_structure4(dify_list, keywords=None, message="success"):
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
        "data": {"chunks": chunks, "doc": {}, "total": len(chunks)},
        "message": message
    }
    return result



# clean api '/document/upload' reponse
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
    return {**original_response, "data": new_data}


def convert_dify_upload_response_to_ragflow_format(dify_response: dict) -> dict:
    DEFAULT_PARSER_CONFIG = {
        "pages": [[]]
    }

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
        "type": data_source_detail.get("extension", ""),
        "batch": dify_data.get('batch')
    }

    return {"code": 0, "data": [ragflow_item], "message": "success"}


# clean insert text 2 db  api response
def wrap_insert_text_response(original_response: dict) -> dict:
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




# clean get document list api response
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



# unical create DB  api response params
def wrap_create_db_response(original_response: dict) -> dict:
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



# clean retrieval response
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
    return {**response, "data": new_data}


# clean get file embedding status api response
def wrap_check_text_processing_progress_response(resp: dict) -> dict:
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
