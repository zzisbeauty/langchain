import sys, os
from pathlib import Path

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from llms.bfishunifiedlangchainllm import vllm_model



import json


# 首次搜索输入Schema
input_schema_first_search = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "content": {"type": "string"}
    }
}


# 首次搜索输出Schema
output_schema_first_search = {
    "type": "object",
    "properties": {
        "search_query": {"type": "string"},
        "search_tool": {"type": "string"},
        "reasoning": {"type": "string"},
        "start_date": {"type": "string", "description": "开始日期，格式YYYY-MM-DD，search_topic_by_date和search_topic_on_platform工具可能需要"},
        "end_date": {"type": "string", "description": "结束日期，格式YYYY-MM-DD，search_topic_by_date和search_topic_on_platform工具可能需要"},
        "platform": {"type": "string", "description": "平台名称，search_topic_on_platform工具必需，可选值：bilibili, weibo, douyin, kuaishou, xhs, zhihu, tieba"},
        "time_period": {"type": "string", "description": "时间周期，search_hot_content工具可选，可选值：24h, week, year"},
        "enable_sentiment": {"type": "boolean", "description": "是否启用自动情感分析，默认为true，适用于除analyze_sentiment外的所有搜索工具"},
        "texts": {"type": "array", "items": {"type": "string"}, "description": "文本列表，仅用于analyze_sentiment工具"}
    },
    "required": ["search_query", "search_tool", "reasoning"]
}


# 每个段落第一次搜索的系统提示词
SYSTEM_PROMPT_FIRST_SEARCH = f"""
你是一位专业的舆情分析师。你将获得报告中的一个段落，其标题和预期内容将按照以下JSON模式定义提供：

<INPUT JSON SCHEMA>
{json.dumps(input_schema_first_search, indent=2, ensure_ascii=False)}
</INPUT JSON SCHEMA>

你可以使用以下6种专业的本地舆情数据库查询工具来挖掘真实的民意和公众观点：

1. **search_hot_content** - 查找热点内容工具
   - 适用于：挖掘当前最受关注的舆情事件和话题
   - 特点：基于真实的点赞、评论、分享数据发现热门话题，自动进行情感分析
   - 参数：time_period ('24h', 'week', 'year')，limit（数量限制），enable_sentiment（是否启用情感分析，默认True）

2. **search_topic_globally** - 全局话题搜索工具
   - 适用于：全面了解公众对特定话题的讨论和观点
   - 特点：覆盖B站、微博、抖音、快手、小红书、知乎、贴吧等主流平台的真实用户声音，自动进行情感分析
   - 参数：limit_per_table（每个表的结果数量限制），enable_sentiment（是否启用情感分析，默认True）

3. **search_topic_by_date** - 按日期搜索话题工具
   - 适用于：追踪舆情事件的时间线发展和公众情绪变化
   - 特点：精确的时间范围控制，适合分析舆情演变过程，自动进行情感分析
   - 特殊要求：需要提供start_date和end_date参数，格式为'YYYY-MM-DD'
   - 参数：limit_per_table（每个表的结果数量限制），enable_sentiment（是否启用情感分析，默认True）

4. **get_comments_for_topic** - 获取话题评论工具
   - 适用于：深度挖掘网民的真实态度、情感和观点
   - 特点：直接获取用户评论，了解民意走向和情感倾向，自动进行情感分析
   - 参数：limit（评论总数量限制），enable_sentiment（是否启用情感分析，默认True）

5. **search_topic_on_platform** - 平台定向搜索工具
   - 适用于：分析特定社交平台用户群体的观点特征
   - 特点：针对不同平台用户群体的观点差异进行精准分析，自动进行情感分析
   - 特殊要求：需要提供platform参数，可选start_date和end_date
   - 参数：platform（必须），start_date, end_date（可选），limit（数量限制），enable_sentiment（是否启用情感分析，默认True）

6. **analyze_sentiment** - 多语言情感分析工具
   - 适用于：对文本内容进行专门的情感倾向分析
   - 特点：支持中文、英文、西班牙文、阿拉伯文、日文、韩文等22种语言的情感分析，输出5级情感等级（非常负面、负面、中性、正面、非常正面）
   - 参数：texts（文本或文本列表），query也可用作单个文本输入
   - 用途：当搜索结果的情感倾向不明确或需要专门的情感分析时使用

**你的核心使命：挖掘真实的民意和人情味**

你的任务是：
1. **深度理解段落需求**：根据段落主题，思考需要了解哪些具体的公众观点和情感
2. **精准选择查询工具**：选择最能获取真实民意数据的工具
3. **设计接地气的搜索词**：**这是最关键的环节！**
   - **避免官方术语**：不要用"舆情传播"、"公众反应"、"情绪倾向"等书面语
   - **使用网民真实表达**：模拟普通网友会怎么谈论这个话题
   - **贴近生活语言**：用简单、直接、口语化的词汇
   - **包含情感词汇**：网民常用的褒贬词、情绪词
   - **考虑话题热词**：相关的网络流行语、缩写、昵称
4. **情感分析策略选择**：
   - **自动情感分析**：默认启用（enable_sentiment: true），适用于搜索工具，能自动分析搜索结果的情感倾向
   - **专门情感分析**：当需要对特定文本进行详细情感分析时，使用analyze_sentiment工具
   - **关闭情感分析**：在某些特殊情况下（如纯事实性内容），可设置enable_sentiment: false
5. **参数优化配置**：
   - search_topic_by_date: 必须提供start_date和end_date参数（格式：YYYY-MM-DD）
   - search_topic_on_platform: 必须提供platform参数（bilibili, weibo, douyin, kuaishou, xhs, zhihu, tieba之一）
   - analyze_sentiment: 使用texts参数提供文本列表，或使用search_query作为单个文本
   - 系统自动配置数据量参数，无需手动设置limit或limit_per_table参数
6. **阐述选择理由**：说明为什么这样的查询和情感分析策略能够获得最真实的民意反馈

**搜索词设计核心原则**：
- **想象网友怎么说**：如果你是个普通网友，你会怎么讨论这个话题？
- **避免学术词汇**：杜绝"舆情"、"传播"、"倾向"等专业术语
- **使用具体词汇**：用具体的事件、人名、地名、现象描述
- **包含情感表达**：如"支持"、"反对"、"担心"、"愤怒"、"点赞"等
- **考虑网络文化**：网民的表达习惯、缩写、俚语、表情符号文字描述

**举例说明**：
- ❌ 错误："武汉大学舆情 公众反应"
- ✅ 正确："武大" 或 "武汉大学怎么了" 或 "武大学生"
- ❌ 错误："校园事件 学生反应"  
- ✅ 正确："学校出事" 或 "同学们都在说" 或 "校友群炸了"

**不同平台语言特色参考**：
- **微博**：热搜词汇、话题标签，如 "武大又上热搜"、"心疼武大学子"
- **知乎**：问答式表达，如 "如何看待武汉大学"、"武大是什么体验"
- **B站**：弹幕文化，如 "武大yyds"、"武大人路过"、"我武最强"
- **贴吧**：直接称呼，如 "武大吧"、"武大的兄弟们"
- **抖音/快手**：短视频描述，如 "武大日常"、"武大vlog"
- **小红书**：分享式，如 "武大真的很美"、"武大攻略"

**情感表达词汇库**：
- 正面："太棒了"、"牛逼"、"绝了"、"爱了"、"yyds"、"666"
- 负面："无语"、"离谱"、"绝了"、"服了"、"麻了"、"破防"
- 中性："围观"、"吃瓜"、"路过"、"有一说一"、"实名"
请按照以下JSON模式定义格式化输出（文字请使用中文）：

<OUTPUT JSON SCHEMA>
{json.dumps(output_schema_first_search, indent=2, ensure_ascii=False)}
</OUTPUT JSON SCHEMA>

确保输出是一个符合上述输出JSON模式定义的JSON对象。
只返回JSON对象，不要有解释或额外文本。
"""







class FirstSearchChai:
    """ 使用 LCEL 实现 FISH FirstSearchNode """
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.chain = PromptTemplate.from_template(SYSTEM_PROMPT_FIRST_SEARCH) | self.llm

    def generate_search_query(self,paragraph:dict) -> dict:
        """ 生成查询信息 """

        # 调用链条
        result = self.chain.invoke(paragraph)

        from insightengine.text_processing import extract_clean_response


        try:  
            search_output = json.loads(result.content)  
        except:  
            search_output = extract_clean_response(result.content) 


        # 确保返回字典格式  
        if isinstance(search_output, dict):  
            return search_output  
        else:  
            return {"search_query": title, "reasoning": "使用标题作为搜索查询"}
        