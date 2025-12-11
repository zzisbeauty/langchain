""" 将 report_structure_node.py ReportStructureNode 改为 LangChain的LLMChain
"""

# from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from llms.bfishunifiedlangchainllm import vllm_model # 默认的 vllm model server

from langchain_core.prompts import PromptTemplate

from insightengine.text_processing import extract_clean_response

import json

# 报告结构输出Schema
output_schema_report_structure = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "content": {"type": "string"}
        }
    }
}

# 生成报告结构的系统提示词
SYSTEM_PROMPT_REPORT_STRUCTURE = f"""
你是一位专业的舆情分析师和报告架构师。给定一个查询，你需要规划一个全面、深入的舆情分析报告结构。

**报告规划要求：**
1. **段落数量**：设计5个核心段落，每个段落都要有足够的深度和广度
2. **内容丰富度**：每个段落应该包含多个子话题和分析维度，确保能挖掘出大量真实数据
3. **逻辑结构**：从宏观到微观、从现象到本质、从数据到洞察的递进式分析
4. **多维分析**：确保涵盖情感倾向、平台差异、时间演变、群体观点、深度原因等多个维度

**段落设计原则：**
- **背景与事件概述**：全面梳理事件起因、发展脉络、关键节点
- **舆情热度与传播分析**：数据统计、平台分布、传播路径、影响范围
- **公众情感与观点分析**：情感倾向、观点分布、争议焦点、价值观冲突
- **不同群体与平台差异**：年龄层、地域、职业、平台用户群体的观点差异
- **深层原因与社会影响**：根本原因、社会心理、文化背景、长远影响

**内容深度要求：**
每个段落的content字段应该详细描述该段落需要包含的具体内容：
- 至少3-5个子分析点
- 需要引用的数据类型（评论数、转发数、情感分布等）
- 需要体现的不同观点和声音
- 具体的分析角度和维度

请按照以下JSON模式定义格式化输出：

<OUTPUT JSON SCHEMA>
{json.dumps(output_schema_report_structure, indent=2, ensure_ascii=False).replace("{", "{{").replace("}", "}}")}
</OUTPUT JSON SCHEMA>

标题和内容属性将用于后续的深度数据挖掘和分析。确保输出是一个符合上述输出JSON模式定义的JSON对象。只返回JSON对象，不要有解释或额外文本。
"""


class ReprotStructureChain:
    """ 使用 LCEL 的报告结构生成；
    """

    def __init__(self,llm: ChatOpenAI):
        self.llm = llm
        self.chain = PromptTemplate.from_template(SYSTEM_PROMPT_REPORT_STRUCTURE) | self.llm

    
    def generate_sturcture(self, query: dict) -> list:
        """ 生成报告结构
        :param query: 用户输入或主题
        :return: list 每个元素包含 title 和 content
        """
        # 构造符合 output_schema_report_structure 的输入
        # 这里我们把 query 放入 title 或 content，占位生成

        # 调用 chain
        result = self.chain.invoke(query)

        # 解析结果
        try:
            structure = json.loads(result.content)
        except:
            structure = extract_clean_response(result.content)

        return structure if isinstance(structure, list) else []
