from __future__ import annotations

import os
from typing import Any, Literal, Optional
from pydantic import BaseModel, Field, SecretStr
from langchain_core.utils import secret_from_env



class LLMConfig(BaseModel):
    """LLM 配置"""

    # Provider 选择
    provider: Literal["openai", "anthropic", "mistralai", "groq", "xai"] = "openai"
    """LLM provider 名称"""

    # 模型配置
    model: str = "gpt-4o"
    """模型名称"""

    temperature: float = 0.0
    """采样温度"""

    max_tokens: Optional[int] = None
    """最大生成 token 数"""

    timeout: Optional[float] = None
    """请求超时时间(秒)"""

    max_retries: int = 2
    """最大重试次数"""

    # API 配置
    api_key: Optional[SecretStr] = Field(default=None)
    """API key,如果不提供则从环境变量读取"""

    base_url: Optional[str] = None
    """自定义 API base URL"""

    # 流式输出
    streaming: bool = False
    """是否启用流式输出"""

    stream_usage: bool = True
    """流式输出时是否包含 usage metadata"""

    # 这个字段是基于 local  vllm 的话，需要传入 vllm 的一些参数时，会用到
    extra_body: Optional[dict[str, Any]] = None
    """vLLM 或其他 OpenAI 兼容服务的自定义参数"""



class AgentConfig(BaseModel):
    """Agent 配置"""

    # LLM 配置
    llm: LLMConfig = Field(default_factory=LLMConfig)
    """LLM 配置对象"""

    # 搜索配置
    max_reflection_iterations: int = 3
    """反思循环的最大迭代次数"""

    tavily_api_key: Optional[SecretStr] = Field(
        default_factory=secret_from_env("TAVILY_API_KEY", default=None)
    )
    """Tavily 搜索 API key"""

    # 输出配置
    output_dir: str = "./output"
    """输出目录路径"""

    save_state: bool = True
    """是否保存状态 JSON"""


def load_config(config_path: Optional[str] = None) -> AgentConfig:
    """
    加载配置

    Args:
        config_path: 配置文件路径(可选,暂不支持从文件加载)

    Returns:
        AgentConfig 对象
    """
    # 目前直接返回默认配置,后续可扩展支持从文件加载
    return AgentConfig()
