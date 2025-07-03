"""
参数转换，用来把 yjy 的参数转化为我本地服务参数
"""

# api /kb/list
def convert_old_to_new_list_params(old_params: dict) -> dict:
    """
    将旧的查询知识库列表参数转换为新的参数格式
    """
    param_map = {
        'page': 'page',
        'page_size': 'limit',
        'keywords': 'keyword'
    }
    
    new_params = {}

    for old_key, new_key in param_map.items():
        if old_key in old_params:
            new_params[new_key] = old_params[old_key]

    # 设置默认值（如果新字段不在 old_params 中）
    new_params.setdefault('page', 1)
    new_params.setdefault('limit', 100)
    new_params.setdefault('keyword', '')

    return new_params
