""" nodes 的 Docstring
Agent 功能载体： node.py 模块，做 search 工作
"""

# import json
# from typing import Any, Dict
# from pydantic import BaseModel, Field
# from langchain_core.runnables import RunnableSerializable
# from langchain_core.language_models import BaseChatModel
# from langchain_core.messages import SystemMessage, HumanMessage


import json
from typing import Any, Dict, Optional, cast
from json import JSONDecodeError

from pydantic import BaseModel, Field, ConfigDict
from langchain_core.runnables import RunnableSerializable
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.runnables.config import RunnableConfig

# import sys, os
# from pathlib import Path
# sys.path.insert(0, str(Path(__file__).parent.parent))  # 添加项目根目录到 Python 路径
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# sys.path.append('/workspaces/langchain')

from .prompts.prompts import SYSTEM_PROMPT_FIRST_SEARCH



class SearchQueryOutput(BaseModel):
    """ 搜索查询输出模型 """
    search_query: str = Field(description="生成的搜索查询")
    reasoning: str = Field(description="生成该查询的推理过程")


class FirstSearchNode(RunnableSerializable[Dict[str, str], SearchQueryOutput]):
    """ 为段落生成首次搜索查询的节点 """

    llm_client: BaseChatModel = Field(description="LLM 客户端")
    """ LLM 客户端 - 使用 Field 定义为 Pydantic 字段 """

    system_prompt: str = Field(default=SYSTEM_PROMPT_FIRST_SEARCH)
    """ 系统提示词 """

    model_config = ConfigDict(
        arbitrary_types_allowed=True,  # 允许 BaseChatModel 等非标准类型
    )

    def validate_input(self, input_data: Any) -> bool:
        """ 验证输入数据 - 保留原有方法 """
        if isinstance(input_data, str):
            try:
                data = json.loads(input_data)
                return "title" in data and "content" in data
            except JSONDecodeError:
                return False
        elif isinstance(input_data, dict):
            return "title" in input_data and "content" in input_data
        return False

    def process_output(self, output: SearchQueryOutput) -> Dict[str, str]:
        """ 处理输出为字典格式 - 保留原有方法签名

        Args:
            output: SearchQueryOutput 对象

        Returns:
            包含 search_query 和 reasoning 的字典
        """
        return {
            "search_query": output.search_query,
            "reasoning": output.reasoning
        }

    def invoke(
        self,
        input_data: Dict[str, str],
        config: Optional[RunnableConfig] = None,
        **kwargs: Any
    ) -> SearchQueryOutput:
        """ 调用 LLM 生成搜索查询 - 对应原来的 run 方法

        Args:
            input_data: 包含 title 和 content 的字典
            config: Runnable 配置
            **kwargs: 额外参数

        Returns:
            SearchQueryOutput 对象
        """
        try:
            # 验证输入
            if not self.validate_input(input_data):
                raise ValueError("输入数据格式错误,需要包含 title 和 content 字段")

            # 准备输入数据
            if isinstance(input_data, str):
                message = input_data
            else:
                message = json.dumps(input_data, ensure_ascii=False)

            # 构造消息
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=message)
            ]

            # 使用 with_structured_output 调用 LLM - with_structured_output() 方法是 LangChain 中用于将 LLM 的输出自动解析为结构化格式的核心功能
            structured_llm = self.llm_client.with_structured_output(SearchQueryOutput)
            result = structured_llm.invoke(messages, config=config)
            # 添加类型断言或转换
            if isinstance(result, dict):
                return SearchQueryOutput(**result)
            return cast(SearchQueryOutput, result)
            return result
        except Exception as e:
            # 返回默认查询 - 保留原有错误处理逻辑
            return SearchQueryOutput(
                search_query="相关主题研究",
                reasoning=f"由于解析失败,使用默认搜索查询: {str(e)}"
            )

    def run(self, input_data: Any, **kwargs: Any) -> Dict[str, str]:
        """ 保留原有的 run 方法接口,返回字典

        Args:
            input_data: 包含 title 和 content 的字符串或字典
            **kwargs: 额外参数

        Returns:
            包含 search_query 和 reasoning 的字典
        """
        result = self.invoke(input_data, **kwargs)
        return self.process_output(result)



import json
from typing import Any, Dict, Optional, cast
from json import JSONDecodeError

from pydantic import BaseModel, Field, ConfigDict
from langchain_core.runnables import RunnableSerializable
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.runnables.config import RunnableConfig

# 从 prompts 包导入
from .prompts.prompts import SYSTEM_PROMPT_FIRST_SUMMARY


class ParagraphSummaryOutput(BaseModel):
    """段落总结输出模型"""
    paragraph_latest_state: str = Field(description="段落的最新总结内容")


class FirstSummaryNode(RunnableSerializable[Dict[str, Any], str]):
    """根据搜索结果生成段落首次总结的节点"""

    llm_client: BaseChatModel = Field(description="LLM 客户端")
    system_prompt: str = Field(default=SYSTEM_PROMPT_FIRST_SUMMARY)

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    def validate_input(self, input_data: Any) -> bool:
        """验证输入数据 - 保留原有方法"""
        if isinstance(input_data, str):
            try:
                data = json.loads(input_data)
                required_fields = ["title", "content", "search_query", "search_results"]
                return all(field in data for field in required_fields)
            except JSONDecodeError:
                return False
        elif isinstance(input_data, dict):
            required_fields = ["title", "content", "search_query", "search_results"]
            return all(field in input_data for field in required_fields)
        return False

    def invoke(
        self,
        input_data: Dict[str, Any],
        config: Optional[RunnableConfig] = None,
        **kwargs: Any
    ) -> str:
        """
        调用 LLM 生成段落总结 - 对应原来的 run 方法

        Args:
            input_data: 包含 title、content、search_query 和 search_results 的字典
            config: Runnable 配置
            **kwargs: 额外参数

        Returns:
            段落总结内容(字符串)
        """
        try:
            # 验证输入
            if not self.validate_input(input_data):
                raise ValueError("输入数据格式错误,需要包含 title、content、search_query 和 search_results 字段")

            # 准备输入数据
            if isinstance(input_data, str):
                message = input_data
            else:
                message = json.dumps(input_data, ensure_ascii=False)

            # 构造消息
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=message)
            ]

            # 尝试使用 structured output
            try:
                structured_llm = self.llm_client.with_structured_output(ParagraphSummaryOutput)
                result = structured_llm.invoke(messages, config=config)

                # 类型转换
                if isinstance(result, dict):
                    return result.get("paragraph_latest_state", "")
                return cast(ParagraphSummaryOutput, result).paragraph_latest_state

            except Exception:
                response = self.llm_client.invoke(messages, config=config)

                # 处理 content 的不同类型
                content = response.content
                if isinstance(content, str):
                    text = content
                elif isinstance(content, list):
                    # 提取文本内容块
                    text_parts = []
                    for block in content:
                        if isinstance(block, str):
                            text_parts.append(block)
                        elif isinstance(block, dict) and block.get("type") == "text":
                            text_parts.append(block.get("text", ""))
                    text = "".join(text_parts)
                else:
                    text = str(content)

                return self._extract_summary_from_text(text)

        except Exception as e:
            # 返回默认总结
            return f"段落总结生成失败: {str(e)}"

    def _extract_summary_from_text(self, text: str) -> str:
        """
        从文本中提取总结内容

        Args:
            text: LLM 原始输出文本

        Returns:
            提取的总结内容
        """
        try:
            # 尝试解析为 JSON
            try:
                result = json.loads(text)
                if isinstance(result, dict):
                    paragraph_content = result.get("paragraph_latest_state", "")
                    if paragraph_content:
                        return paragraph_content
            except JSONDecodeError:
                pass

            # 如果不是 JSON 或解析失败,返回原始文本
            return text.strip()

        except Exception:
            return "段落总结生成失败"

    def run(self, input_data: Any, **kwargs: Any) -> str:
        """
        保留原有的 run 方法接口,返回字符串

        Args:
            input_data: 包含 title、content、search_query 和 search_results 的字符串或字典
            **kwargs: 额外参数

        Returns:
            段落总结内容(字符串)
        """
        return self.invoke(input_data, **kwargs)

    def process_output(self, output: str) -> str:
        """
        保留原有的 process_output 方法 - 用于兼容性

        Args:
            output: LLM 原始输出

        Returns:
            处理后的总结内容
        """
        return self._extract_summary_from_text(output)




import json
from typing import Any, Dict, Optional, cast
from json import JSONDecodeError

from pydantic import BaseModel, Field, ConfigDict
from langchain_core.runnables import RunnableSerializable
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.runnables.config import RunnableConfig
from .prompts.prompts import SYSTEM_PROMPT_REFLECTION


class ReflectionQueryOutput(BaseModel):
    """反思搜索查询输出模型"""
    search_query: str = Field(description="生成的搜索查询")
    reasoning: str = Field(description="生成该查询的推理过程")


class ReflectionNode(RunnableSerializable[Dict[str, str], ReflectionQueryOutput]):
    """反思段落并生成新搜索查询的节点"""

    llm_client: BaseChatModel = Field(description="LLM 客户端")
    """LLM 客户端 - 使用 Field 定义为 Pydantic 字段"""

    system_prompt: str = Field(default=SYSTEM_PROMPT_REFLECTION)
    """系统提示词"""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    def validate_input(self, input_data: Any) -> bool:
        """验证输入数据 - 保留原有方法"""
        if isinstance(input_data, str):
            try:
                data = json.loads(input_data)
                required_fields = ["title", "content", "paragraph_latest_state"]
                return all(field in data for field in required_fields)
            except JSONDecodeError:
                return False
        elif isinstance(input_data, dict):
            required_fields = ["title", "content", "paragraph_latest_state"]
            return all(field in input_data for field in required_fields)
        return False

    def process_output(self, output: ReflectionQueryOutput) -> Dict[str, str]:
        """ 处理输出为字典格式 - 保留原有方法签名

        Args:
            output: ReflectionQueryOutput 对象

        Returns:
            包含 search_query 和 reasoning 的字典
        """
        return {
            "search_query": output.search_query,
            "reasoning": output.reasoning
        }

    def invoke(
        self,
        input_data: Dict[str, str],
        config: Optional[RunnableConfig] = None,
        **kwargs: Any
    ) -> ReflectionQueryOutput:
        """ 调用 LLM 进行反思并生成搜索查询 - 对应原来的 run 方法

        Args:
            input_data: 包含 title、content 和 paragraph_latest_state 的字典
            config: Runnable 配置
            **kwargs: 额外参数

        Returns:
            ReflectionQueryOutput 对象
        """
        try:
            # 验证输入
            if not self.validate_input(input_data):
                raise ValueError("输入数据格式错误,需要包含 title、content 和 paragraph_latest_state 字段")

            # 准备输入数据
            if isinstance(input_data, str):
                message = input_data
            else:
                message = json.dumps(input_data, ensure_ascii=False)

            # 构造消息
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=message)
            ]

            # 使用 with_structured_output 调用 LLM
            structured_llm = self.llm_client.with_structured_output(ReflectionQueryOutput)
            result = structured_llm.invoke(messages, config=config)

            # 类型转换
            if isinstance(result, dict):
                return ReflectionQueryOutput(**result)
            return cast(ReflectionQueryOutput, result)

        except Exception as e:
            # 返回默认查询 - 保留原有错误处理逻辑
            return ReflectionQueryOutput(
                search_query="深度研究补充信息",
                reasoning=f"由于解析失败,使用默认反思搜索查询: {str(e)}"
            )

    def run(self, input_data: Any, **kwargs: Any) -> Dict[str, str]:
        """ 保留原有的 run 方法接口,返回字典

        Args:
            input_data: 包含 title、content 和 paragraph_latest_state 的字符串或字典
            **kwargs: 额外参数

        Returns:
            包含 search_query 和 reasoning 的字典
        """
        result = self.invoke(input_data, **kwargs)
        return self.process_output(result)


import json
from typing import Any, Dict, Optional, cast
from json import JSONDecodeError

from pydantic import BaseModel, Field, ConfigDict
from langchain_core.runnables import RunnableSerializable
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.runnables.config import RunnableConfig

# 从 prompts 包导入
from .prompts.prompts import SYSTEM_PROMPT_REFLECTION_SUMMARY


class ReflectionSummaryOutput(BaseModel):
    """反思总结输出模型"""
    updated_paragraph_latest_state: str = Field(description="更新后的段落总结内容")


class ReflectionSummaryNode(RunnableSerializable[Dict[str, Any], str]):
    """根据反思搜索结果更新段落总结的节点"""

    llm_client: BaseChatModel = Field(description="LLM 客户端")
    system_prompt: str = Field(default=SYSTEM_PROMPT_REFLECTION_SUMMARY)

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    def validate_input(self, input_data: Any) -> bool:
        """ 验证输入数据 - 保留原有方法 """
        if isinstance(input_data, str):
            try:
                data = json.loads(input_data)
                required_fields = ["title", "content", "search_query", "search_results", "paragraph_latest_state"]
                return all(field in data for field in required_fields)
            except JSONDecodeError:
                return False
        elif isinstance(input_data, dict):
            required_fields = ["title", "content", "search_query", "search_results", "paragraph_latest_state"]
            return all(field in input_data for field in required_fields)
        return False

    def invoke(
        self,
        input_data: Dict[str, Any],
        config: Optional[RunnableConfig] = None,
        **kwargs: Any
    ) -> str:
        """ 调用 LLM 生成反思总结 - 对应原来的 run 方法

        Args:
            input_data: 包含 title、content、search_query、search_results 和 paragraph_latest_state 的字典
            config: Runnable 配置
            **kwargs: 额外参数

        Returns:
            更新后的段落总结内容(字符串)
        """
        try:
            # 验证输入
            if not self.validate_input(input_data):
                raise ValueError("输入数据格式错误,需要包含 title、content、search_query、search_results 和 paragraph_latest_state 字段")

            # 准备输入数据
            if isinstance(input_data, str):
                message = input_data
            else:
                message = json.dumps(input_data, ensure_ascii=False)

            # 构造消息
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=message)
            ]

            # 尝试使用 structured output
            try:
                structured_llm = self.llm_client.with_structured_output(ReflectionSummaryOutput)
                result = structured_llm.invoke(messages, config=config)

                # 类型转换
                if isinstance(result, dict):
                    return result.get("updated_paragraph_latest_state", "")
                return cast(ReflectionSummaryOutput, result).updated_paragraph_latest_state

            except Exception:
                # 如果 structured output 失败,回退到普通调用
                response = self.llm_client.invoke(messages, config=config)
                return self._extract_summary_from_text(response.content)

        except Exception as e:
            # 返回默认总结
            return f"反思总结生成失败: {str(e)}"

    def _extract_summary_from_text(self, content: Any) -> str:
        """ 从文本中提取总结内容

        Args:
            content: LLM 原始输出内容 (可能是字符串或内容块列表)

        Returns:
            提取的总结内容
        """
        try:
            # 处理 content 的不同类型
            if isinstance(content, str):
                text = content
            elif isinstance(content, list):
                # 提取文本内容块
                text_parts = []
                for block in content:
                    if isinstance(block, str):
                        text_parts.append(block)
                    elif isinstance(block, dict) and block.get("type") == "text":
                        text_parts.append(block.get("text", ""))
                text = "".join(text_parts)
            else:
                text = str(content)

            # 尝试解析为 JSON
            try:
                result = json.loads(text)
                if isinstance(result, dict):
                    updated_content = result.get("updated_paragraph_latest_state", "")
                    if updated_content:
                        return updated_content
            except JSONDecodeError:
                pass

            # 如果不是 JSON 或解析失败,返回原始文本
            return text.strip()

        except Exception:
            return "反思总结生成失败"

    def run(self, input_data: Any, **kwargs: Any) -> str:
        """ 保留原有的 run 方法接口,返回字符串

        Args:
            input_data: 包含完整反思信息的字符串或字典
            **kwargs: 额外参数

        Returns:
            更新后的段落总结内容(字符串)
        """
        return self.invoke(input_data, **kwargs)

    def process_output(self, output: str) -> str:
        """ 保留原有的 process_output 方法 - 用于兼容性

        Args:
            output: LLM 原始输出

        Returns:
            处理后的总结内容
        """
        return self._extract_summary_from_text(output)



class ReportFormattingNode:
    ...
    # todo 
