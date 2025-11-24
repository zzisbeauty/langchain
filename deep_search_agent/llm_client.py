# import sys, os
# from pathlib import Path
# sys.path.insert(0, str(Path(__file__).parent.parent))  # 添加项目根目录到 Python 路径
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# sys.path.append('/workspaces/langchain')


from config import AgentConfig, LLMConfig
from pydantic import BaseModel, Field, SecretStr
from deep_search_agent.agent import DeepSearchAgent # type: ignore
from deep_search_agent.config import AgentConfig, LLMConfig # type: ignore


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
llm_client = agent.llm_client
