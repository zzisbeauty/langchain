"""
Prompt模块
定义Deep Search Agent各个阶段使用的系统提示词
"""

"""Prompts 模块"""

import sys, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))  # 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append('/workspaces/langchain')

# try:
#     from deep_search_agent.prompts.prompts import SYSTEM_PROMPT_FIRST_SEARCH
#     print("导入成功!")
# except Exception as e:
#     import traceback
#     print(f"错误类型: {type(e).__name__}")
#     print(f"错误信息: {str(e)}")
#     print("\n完整堆栈:")
#     traceback.print_exc()


from deep_search_agent.prompts.prompts import ( # type: ignore
    SYSTEM_PROMPT_REPORT_STRUCTURE,
    SYSTEM_PROMPT_FIRST_SEARCH,
    SYSTEM_PROMPT_FIRST_SUMMARY,
    SYSTEM_PROMPT_REFLECTION,
    SYSTEM_PROMPT_REFLECTION_SUMMARY,
    SYSTEM_PROMPT_REPORT_FORMATTING,
    output_schema_report_structure,
    output_schema_first_search,
    output_schema_first_summary,
    output_schema_reflection,
    output_schema_reflection_summary,
    input_schema_report_formatting
)

__all__ = [
    "SYSTEM_PROMPT_REPORT_STRUCTURE",
    "SYSTEM_PROMPT_FIRST_SEARCH",
    "SYSTEM_PROMPT_FIRST_SUMMARY",
    "SYSTEM_PROMPT_REFLECTION",
    "SYSTEM_PROMPT_REFLECTION_SUMMARY",
    "SYSTEM_PROMPT_REPORT_FORMATTING",
    "output_schema_report_structure",
    "output_schema_first_search",
    "output_schema_first_summary",
    "output_schema_reflection",
    "output_schema_reflection_summary",
    "input_schema_report_formatting"
]
