from dify_client import CompletionClient

import json, sys, os
  

def find_project_root(current_path, marker='.git'):
    """ 从当前路径向上查找，直到找到包含 marker（如 .git）的目录 """
    while current_path != os.path.dirname(current_path):
        if os.path.exists(os.path.join(current_path, marker)):
            return current_path
        current_path = os.path.dirname(current_path)
    return current_path  # 最后返回根目录

project_root = find_project_root(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

from cdify.utils.config import *


# 初始化客户端
api_key = secret_key
completion_client = CompletionClient(api_key)


# 创建文本生成请求
def generate_text(query: str, user_id: str) -> str:
    """
    生成文本响应
    Args:
        query: 用户输入的查询文本
        user_id: 用户ID
    Returns:
        str: 生成的响应文本
    """
    try:
        response = completion_client.create_completion_message(
            inputs={"query": query},
            response_mode="blocking",
            user=user_id
        )
        response.raise_for_status()
        return response.json().get('answer')
    except Exception as e:
        print(f"生成文本时发生错误: {str(e)}")
        return None

# 使用示例
result = generate_text("今天天气怎么样？", "user_123")
print(result)