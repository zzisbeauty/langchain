import langchain
import langchain_core

# compatible
# compatible

# from langchain_openai import 
from langchain_openai import ChatOpenAI


llm_compatible_model = ChatOpenAI(  
    base_url="http://192.168.1.6:1128/v1",
    model="/localmodels/Qwen3-4B-Thinking-2507",  
    temperature=0,  
    api_key="vllm-local"  # 可选，也可通过环境变量设置  
)


from langchain_core.messages import HumanMessage

message = HumanMessage(content="hello, 用中文回答")

# 同步调用
# response = llm_compatible_model.invoke([message])
# print(response.content)


# 异步调用
async def getAinvoke(message):
    """ 仅仅是定义协程异步方法 """
    response = await llm_compatible_model.ainvoke([message])

    return response

import asyncio

# 执行异步任务方式一：直接在事件循环中自动创建了任务； 即直接将异步方法在事件循环中创建任务并 await response
# response = asyncio.run(getAinvoke(message))
# print(response.content)

# 执行异步任务方式二： create_task；
async def createTask(message):
    task = asyncio.create_task(getAinvoke(message))
    response = await task
    return response

# 适配方式二，且仍然需要主动将 task 放在事件循环中
# 方式二的适用场景在于它本来就不是给单个调用设计的， 是给多个异步任务制定的，可以将多个异步任务手动放入到事件循环中中
# response = asyncio.run(createTask(message))
# print(response.content)




# 流式调用
# for chunk in llm_compatible_model.stream([message]):
#     print(chunk.content, end="")



# 批量调用
# response = llm_compatible_model.batch([[message], ['100字介绍太阳系']])
# print(response)



# 在 chain 中使用

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 创建 chain
prompt = ChatPromptTemplate.from_template("Tell me a joke about {topic}")
chain = prompt | llm_compatible_model | StrOutputParser()
# 调用 chain
response = chain.invoke({"topic":"ai"})
print(response)


# # 调用时传递额外参数  
# response = llm_compatible_model.invoke(  
#     [message],  
#     temperature=0.5,  
#     max_tokens=100  
# )
