import langchain_openai
from langchain_openai import ChatOpenAI
from  typing import Optional


class UnifiedLangChainLLM:
    def __init__(
            self,
            api_key: str = "vllm-key",
            model_name:str = "/localmodels/Qwen3-4B-Thinking-2507",
            base_url: Optional[str] = "http://192.168.1.6:1128/v1",
            timeout: float = 1800
        ):
        self.llm = ChatOpenAI(
            api_key=api_key,
            base_url=base_url,
            model=model_name,
            timeout=timeout
        )

    def invoke(self, system_prompt:str, user_prompt:str, add_timestamp:bool = True) -> str:
        from langchain_core.messages import SystemMessage, HumanMessage
        if add_timestamp: # InsightEngine/MediaEngine/QueryEngine | else  ReportEngine 无需在 user_prompt 中添加时间戳
            from datetime import datetime
            current_time = datetime.now().strftime("%Y年%m月%d日%H时%M分")
            time_prefix = f"今天的实际时间是{current_time}"  
            user_prompt = f"{time_prefix}\n{user_prompt}" if user_prompt else time_prefix 
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]

        response = self.llm.invoke(messages)
        return response.content


# base vllm model client
vllm_model = UnifiedLangChainLLM()