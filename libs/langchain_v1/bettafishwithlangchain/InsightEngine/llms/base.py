
from loguru import logger

from typing  import Any, Dict, Optional, Iterator, Generator
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage



import os



try:
    from retry_helper import with_retry, LLM_RETRY_CONFIG
except ImportError:
    import time
    from datetime import datetime
    def with_retry(config=None):
        """ 带参数装饰器：可以指定重试次数和重试间隔 """
        def decorator(func):
            def wrapper(*args, **kwargs):
                retries = config.get("retries", 3) if config else 1
                delay = config.get("delay", 1) if config else 0
                for attempt in range(1, retries + 1):
                    try:
                        print(f"[Attempt {attempt}] Calling {func.__name__}...")
                        return func(*args, **kwargs)  # 业务函数参数透传
                    except Exception as e:
                        print(f"Error: {e}, retrying in {delay}s...")
                        time.sleep(delay)
                return None  # 如果重试失败，返回 None
            return wrapper
        return decorator

    LLM_RETRY_CONFIG = {
        "retries": 3,      # 最大重试次数
        "delay": 1,        # 每次重试的间隔秒数
    }



class LLMClient:
    def __init__(
            self,
            api_key: str = "vllm-key",
            model_name:str = "/localmodels/Qwen3-4B-Thinking-2507",
            base_url: Optional[str] = "http://192.168.1.4:1128/v1",
            # timeout_fallback: float = 1800,
            provider: str = "vllm"
        ):

        self.base_url = base_url
        self.api_key = api_key
        self.model_name = model_name
        self.provider = provider
        
        timeout_fallback = os.getenv("LLM_REQUEST_TIMEOUT") or os.getenv("INSIGHT_ENGINE_REQUEST_TIMEOUT") or "1800"
        try:
            self.timeout = float(timeout_fallback)
        except ValueError:
            self.timeout = 1800.0

        # 构建 OpenAI 客户端用
        client_kwargs: Dict[str, Any] = {
            "api_key": api_key,
            "max_retries": 0,
        }
        if base_url:
            client_kwargs["base_url"] = base_url

        if provider == "openai":
            from openai import OpenAI
            self.client = OpenAI(**client_kwargs)


        self.client = ChatOpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            model=self.model_name,
            timeout=self.timeout
        )


    @with_retry(LLM_RETRY_CONFIG)
    def invoke(self, system_prompt: str, user_prompt: str, **kwargs) -> str:
        current_time = datetime.now().strftime("%Y年%m月%d日%H时%M分")
        time_prefix = f"今天的实际时间是{current_time}"
        user_prompt = f"{time_prefix}\n{user_prompt}" if user_prompt else time_prefix

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]

        allowed_keys = {"temperature", "top_p", "presence_penalty", "frequency_penalty", "stream"}
        allowed_keys = {"temperature", "top_p", "presence_penalty", "frequency_penalty"}
        extra_params = {key: value for key, value in kwargs.items() if key in allowed_keys and value is not None}
        
        timeout = kwargs.pop("timeout", self.timeout)  

        response = self.client.invoke(
            messages,
            timeout,
            **extra_params
        )

        # 返回响应内容  
        if hasattr(response, 'content'):  
            return self.validate_response(response.content)  
        return ""


    def stream_invoke(
            self,
            system_prompt:str,
            user_prompt:str,
            **kwargs
        ) -> Generator[str,None,None]:
        """ 流式调用LLM，逐步返回响应内容
        Args:
            system_prompt: 系统提示词
            user_prompt: 用户提示词
            **kwargs: 额外参数（temperature, top_p等）
        Yields:
            响应文本块（str）
        """
        current_time = datetime.now().strftime("%Y年%m月%d日%H时%M分")
        time_prefix = f"今天的实际时间是{current_time}"
        if user_prompt:
            user_prompt = f"{time_prefix}\n{user_prompt}"
        else:
            user_prompt = time_prefix

        messages = [
            SystemMessage(system_prompt),
            HumanMessage(user_prompt)
        ]

        allowed_keys = {"temperature", "top_p", "presence_penalty", "frequency_penalty"}
        extra_params = {key: value for key, value in kwargs.items()   
                   if key in allowed_keys and value is not None}  

        timeout = kwargs.pop("timeout", self.timeout)  
        try:
            # 使用 ChatOpenAI 的 stream 方法  
            for chunk in self.client.stream(messages, timeout=timeout, **extra_params):  
                if hasattr(chunk, 'content') and chunk.content:  
                    yield chunk.content  
        except Exception as e:
            logger.error(f"流式请求失败: {str(e)}")  
            raise e

    @staticmethod
    def validate_response(response: Optional[str]) -> str:
        if response is None:
            return ""
        return response.strip()

    def get_model_info(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "model": self.model_name,
            "api_base": self.base_url or "default",
        }



# base vllm model client
# vllm_model = LLMClient()