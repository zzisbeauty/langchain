from typing import Optional
from langchain_core.language_models import BaseChatModel
from langchain.chat_models import init_chat_model

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))  # 添加项目根目录到 Python 路径


from config import AgentConfig, load_config


class DeepSearchAgent:
    """Deep Search Agent 主类"""

    def __init__(self, config: Optional[AgentConfig] = None):
        """
        初始化 Deep Search Agent

        Args:
            config: 配置对象,如果不提供则自动加载
        """
        # 加载配置
        self.config = config or load_config()

        # 初始化 LLM 客户端
        self.llm_client = self._initialize_llm()

        # 初始化节点(后续实现)
        # self._initialize_nodes()

        # 状态(后续实现)
        # self.state = State()

        # 确保输出目录存在
        import os
        os.makedirs(self.config.output_dir, exist_ok=True)

        print(f"Deep Search Agent 已初始化")
        print(f"使用 LLM: {self.llm_client._llm_type}")
        print(f"模型: {self.config.llm.model}")

    def _initialize_llm(self) -> BaseChatModel:
        """
        初始化 LLM 客户端

        使用 LangChain 的 init_chat_model 工厂函数来创建 chat model

        Returns:
            BaseChatModel 实例
        """
        llm_config = self.config.llm

        # 准备 kwargs
        kwargs = {
            "temperature": llm_config.temperature,
            "max_tokens": llm_config.max_tokens,
            "timeout": llm_config.timeout,
            "max_retries": llm_config.max_retries,
        }

        # 添加 API key(如果提供)
        if llm_config.api_key:
            kwargs["api_key"] = llm_config.api_key.get_secret_value()

        # 添加 base_url(如果提供)
        if llm_config.base_url:
            kwargs["base_url"] = llm_config.base_url

        # 添加流式配置
        if llm_config.streaming:
            kwargs["streaming"] = True
            if llm_config.stream_usage:
                kwargs["stream_usage"] = True



        # 在 kwargs 中添加，这个是基于 local vllm 进行服务部署的话，需要向参数配置中添加额外的 vllm 的需要的参数的话，就这样子配置并传入 vllm 需要的参数
        if llm_config.extra_body:
            kwargs["extra_body"] = llm_config.extra_body



        # 使用 init_chat_model 创建模型
        llm = init_chat_model(
            model=llm_config.model,
            model_provider=llm_config.provider,
            **kwargs
        )

        return llm



# """ 测试创建模型实例

# from deep_search_agent.config import AgentConfig, LLMConfig
# from deep_search_agent.agent import DeepSearchAgent
from config import AgentConfig, LLMConfig
from pydantic import BaseModel, Field, SecretStr


# 方式 1: 使用默认配置
# agent = DeepSearchAgent()

# 方式 2: 自定义配置
config = AgentConfig(
    llm=LLMConfig(
        # 这里的参数是足够使用 openai 默认的参数
        provider="openai",
        # model="gpt-4o-mini",
        temperature=0.0,
        max_tokens=4096,

        # 需要明确使用 local  vllm 相关服务的时候，这些参数是需要指定的
        base_url="http://192.168.1.6:1128/v1",  # 您的 vLLM 服务地址
        api_key=SecretStr("EMPTY"), # 包装成 SecretStr  ,  # vLLM 通常不需要真实的 API key
        model="/localmodels/Qwen3-4B-Thinking-2507",  #local vllm model name
        # extra_body={  # 这里的参数非必须
        #     "use_beam_search": True,
        #     "best_of": 4
        # }
    ),
    max_reflection_iterations=5,
    output_dir="./my_output"
)
agent = DeepSearchAgent(config=config)

# """
