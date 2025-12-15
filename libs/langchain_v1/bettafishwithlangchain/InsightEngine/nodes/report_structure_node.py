import json
from typing import Any, Dict, List
from json.decoder import JSONDecodeError
from loguru import logger

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel

from base_node import StateMutationNode
from state.state import State
from prompts.prompts import SYSTEM_PROMPT_REPORT_STRUCTURE
from utils.text_processing import (
    remove_reasoning_from_output,
    clean_json_tags,
    extract_clean_response,
    fix_incomplete_json,
)

from llms.base import LLMClient

from langchain_core.runnables import Runnable


# class RunnableLLMClient(Runnable):
#     """把你现有的 LLMClient 封装成 LangChain v1 Runnable"""

#     def __init__(self, llm_client: LLMClient):
#         self.llm_client = llm_client

#     def invoke(self, input: dict, **kwargs) -> str:
#         """
#         LCEL 调用接口
#         input: dict, 包含 key 'query'
#         返回 str
#         """
#         query = input.get("query", "")
#         return self.llm_client.stream_invoke_to_string("", query)

class RunnableLLMClient(Runnable):
    """把你现有的 LLMClient 封装成 LangChain v1 Runnable"""

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def invoke(self, input, config=None, **kwargs) -> str:
        """
        LCEL 调用接口
        input: dict 或 ChatPromptValue
        返回 str
        """
        # 如果是 ChatPromptValue，从 messages 里取人类输入
        if isinstance(input, ChatPromptTemplate):
            # 假设最后一条 human 消息是用户 query
            human_messages = [m for m in input.messages if m.type == "human"]
            query = human_messages[-1].content if human_messages else ""
        elif isinstance(input, dict):
            query = input.get("query", "")
        else:
            query = str(input)

        # 调用你的原始 LLMClient
        return self.llm_client.invoke("", query)

class ReportStructureNode(StateMutationNode):
    """生成报告结构节点（LangChain v1 版本）"""

    def __init__(self, llm_client, query: str):
        super().__init__(llm_client, "ReportStructureNode")
        self.query = query

        # 1️⃣ 封装成 Runnable
        self.runnable = RunnableLLMClient(llm_client)

        # 2️⃣ Prompt
        escaped_prompt = SYSTEM_PROMPT_REPORT_STRUCTURE.replace("{", "{{").replace("}", "}}")
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", escaped_prompt),
                ("human", "{query}"),
            ]
        )

        # 3️⃣ LCEL chain
        self.chain = self.prompt | self.runnable

    def validate_input(self, input_data: Any) -> bool:
        return isinstance(self.query, str) and len(self.query.strip()) > 0

    def run(self, input_data: Any = None, **kwargs) -> List[Dict[str, str]]:
        try:
            logger.info(f"正在为查询生成报告结构: {self.query}")

            response = self.chain.invoke({"query": self.query})
            output = response  # 已经是 str

            processed_response = self.process_output(output)

            logger.info(f"成功生成 {len(processed_response)} 个段落结构")
            return processed_response

        except Exception as e:
            logger.exception(f"生成报告结构失败: {e}")
            raise

    def process_output(self, output: str) -> List[Dict[str, str]]:
        try:
            cleaned_output = remove_reasoning_from_output(output)
            cleaned_output = clean_json_tags(cleaned_output)

            logger.info(f"清理后的输出: {cleaned_output}")

            try:
                report_structure = json.loads(cleaned_output)
                logger.info("JSON 解析成功")
            except JSONDecodeError as e:
                logger.error(f"JSON 解析失败: {e}")
                report_structure = extract_clean_response(cleaned_output)
                if "error" in report_structure:
                    logger.error("JSON 解析失败，尝试修复...")
                    fixed_json = fix_incomplete_json(cleaned_output)
                    if fixed_json:
                        try:
                            report_structure = json.loads(fixed_json)
                            logger.info("JSON 修复成功")
                        except JSONDecodeError:
                            logger.error("JSON 修复失败")
                            return self._generate_default_structure()
                    else:
                        logger.error("无法修复 JSON，使用默认结构")
                        return self._generate_default_structure()

            if not isinstance(report_structure, list):
                if isinstance(report_structure, dict):
                    report_structure = [report_structure]
                else:
                    logger.error("报告结构格式无效，使用默认结构")
                    return self._generate_default_structure()

            validated_structure = []
            for i, paragraph in enumerate(report_structure):
                if not isinstance(paragraph, dict):
                    logger.warning(f"段落 {i+1} 不是字典，跳过")
                    continue
                title = paragraph.get("title", f"段落 {i+1}")
                content = paragraph.get("content", "")
                if not title or not content:
                    logger.warning(f"段落 {i+1} 缺少标题或内容，跳过")
                    continue
                validated_structure.append({"title": title, "content": content})

            if not validated_structure:
                logger.warning("没有有效段落，使用默认结构")
                return self._generate_default_structure()

            logger.info(f"成功验证 {len(validated_structure)} 个段落")
            return validated_structure

        except Exception as e:
            logger.exception(f"处理输出失败: {e}")
            return self._generate_default_structure()

    def _generate_default_structure(self) -> List[Dict[str, str]]:
        return [
            {"title": "研究概述", "content": "对查询主题进行总体概述和分析"},
            {"title": "深度分析", "content": "深入分析查询主题的各个方面"},
        ]

    def mutate_state(self, input_data: Any = None, state: State = None, **kwargs) -> State:
        if state is None:
            state = State()
        try:
            report_structure = self.run(input_data, **kwargs)
            state.query = self.query
            if not state.report_title:
                state.report_title = f"关于'{self.query}'的深度研究报告"

            for paragraph in report_structure:
                state.add_paragraph(title=paragraph["title"], content=paragraph["content"])

            logger.info(f"已将 {len(report_structure)} 个段落添加到状态中")
            return state
        except Exception as e:
            logger.exception(f"状态更新失败: {e}")
            raise