"""测试 FirstSearchNode 的完整示例"""

import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
# sys.path.insert(0, str(Path(__file__).parent.parent))  # 添加项目根目录到 Python 路径
sys.path.append('/workspaces/langchain')


from deep_search_agent.config import AgentConfig, LLMConfig # type: ignore
from deep_search_agent.agent import DeepSearchAgent # type: ignore
from deep_search_agent.nodes import FirstSearchNode # type: ignore


def test_llm_initialization():
    """测试 LLM 初始化"""
    print("=" * 50)
    print("测试 1: LLM 初始化")
    print("=" * 50)

    # 配置本地 vLLM 服务
    config = AgentConfig(
        llm=LLMConfig(
            provider="openai",
            model="/localmodels/Qwen3-4B-Thinking-2507",  # 替换为您的模型名称
            base_url="http://192.168.1.6:1128/v1",  # 替换为您的 vLLM 地址
            api_key="local vllm",  # 或者使用 SecretStr("EMPTY")
            temperature=0.0,
            max_tokens=4096,
        )
    )

    # 初始化 Agent (会自动初始化 LLM)
    agent = DeepSearchAgent(config=config)

    print(f"✓ LLM 初始化成功")
    print(f"  模型类型: {agent.llm_client._llm_type}")
    print(f"  模型名称: {config.llm.model}")
    print()

    return agent


def test_first_search_node(agent: DeepSearchAgent):
    """测试 FirstSearchNode"""
    print("=" * 50)
    print("测试 2: FirstSearchNode")
    print("=" * 50)

    # 初始化节点
    first_search_node = FirstSearchNode(llm_client=agent.llm_client)
    print("✓ FirstSearchNode 初始化成功")
    print()

    # 准备测试输入
    test_input = {
        "title": "人工智能的发展",
        "content": "探讨 2024 年人工智能技术的最新进展,包括大语言模型、多模态 AI 等领域"
    }

    print("测试输入:")
    print(f"  标题: {test_input['title']}")
    print(f"  内容: {test_input['content']}")
    print()

    # 方式 1: 使用 invoke (返回 Pydantic 模型)
    print("方式 1: 使用 invoke() 方法")
    try:
        """
        # 这里是原来的代码，需要手动清理和解析
        cleaned_output = remove_reasoning_from_output(output)
        cleaned_output = clean_json_tags(cleaned_output)
        result = json.loads(cleaned_output)
        reasoning = result.get("reasoning", "")
        """
        # 以下这个 invoke 方法 是 LLM 模型输出并经过 with_structured_output() 自动解析后的结果。
        # 代码位置： libs/core/langchain_core/language_models/chat_models.py
        result_model = first_search_node.invoke(test_input)
        print(f"✓ 调用成功")
        print(f"  搜索查询: {result_model.search_query}")
        print(f"  推理过程: {result_model.reasoning}")
        print()
    except Exception as e:
        print(f"✗ 调用失败: {str(e)}")
        print()

    # 方式 2: 使用 run (返回字典)
    print("方式 2: 使用 run() 方法")
    try:
        result_dict = first_search_node.run(test_input)
        print(f"✓ 调用成功")
        print(f"  搜索查询: {result_dict['search_query']}")
        print(f"  推理过程: {result_dict['reasoning']}")
        print()
    except Exception as e:
        print(f"✗ 调用失败: {str(e)}")
        print()

    # 测试输入验证
    print("测试 3: 输入验证")
    valid_inputs = [
        {"title": "测试", "content": "内容"},
        '{"title": "测试", "content": "内容"}',
    ]
    invalid_inputs = [
        {"title": "测试"},  # 缺少 content
        {"content": "内容"},  # 缺少 title
        "invalid json",
        123,
    ]

    for i, inp in enumerate(valid_inputs, 1):
        is_valid = first_search_node.validate_input(inp)
        print(f"  有效输入 {i}: {is_valid} ✓")

    for i, inp in enumerate(invalid_inputs, 1):
        is_valid = first_search_node.validate_input(inp)
        print(f"  无效输入 {i}: {is_valid} ✓")
    print()


# def main():
#     """主测试函数"""
#     try:
#         # 测试 LLM 初始化
#         agent = test_llm_initialization()

#         # 测试 FirstSearchNode
#         test_first_search_node(agent)

#         print("=" * 50)
#         print("所有测试完成!")
#         print("=" * 50)

#     except Exception as e:
#         print(f"\n✗ 测试失败: {str(e)}")
#         import traceback
#         traceback.print_exc()


from deep_search_agent.nodes import ReflectionNode # type: ignore


def test_reflection_node(agent: DeepSearchAgent):
    """测试 ReflectionNode"""
    print("=" * 60)
    print("测试 4: ReflectionNode")
    print("=" * 60)

    # 初始化节点
    reflection_node = ReflectionNode(llm_client=agent.llm_client)
    print("✓ ReflectionNode 初始化成功")
    print()

    # 准备测试输入
    test_input = {
        "title": "人工智能的发展",
        "content": "探讨 2024 年人工智能技术的最新进展",
        "paragraph_latest_state": "已经讨论了大语言模型的基础概念和训练方法,包括 Transformer 架构和预训练技术。"
    }

    print("测试输入:")
    print(f"  标题: {test_input['title']}")
    print(f"  内容: {test_input['content']}")
    print(f"  当前状态: {test_input['paragraph_latest_state'][:50]}...")
    print()

    # 方式 1: 使用 invoke (返回 Pydantic 模型)
    print("方式 1: 使用 invoke() 方法")
    try:
        result_model = reflection_node.invoke(test_input)
        print(f"✓ 调用成功")
        print(f"  搜索查询: {result_model.search_query}")
        print(f"  推理过程: {result_model.reasoning[:100]}...")
        print()
    except Exception as e:
        print(f"✗ 调用失败: {str(e)}")
        print()

    # 方式 2: 使用 run (返回字典)
    print("方式 2: 使用 run() 方法")
    try:
        result_dict = reflection_node.run(test_input)
        print(f"✓ 调用成功")
        print(f"  搜索查询: {result_dict['search_query']}")
        print(f"  推理过程: {result_dict['reasoning'][:100]}...")
        print()
    except Exception as e:
        print(f"✗ 调用失败: {str(e)}")
        print()

    # 测试输入验证
    print("测试 5: ReflectionNode 输入验证")
    valid_inputs = [
        {
            "title": "测试",
            "content": "内容",
            "paragraph_latest_state": "状态"
        },
    ]
    invalid_inputs = [
        {"title": "测试", "content": "内容"},  # 缺少 paragraph_latest_state
        {"title": "测试", "paragraph_latest_state": "状态"},  # 缺少 content
        {"content": "内容", "paragraph_latest_state": "状态"},  # 缺少 title
    ]

    for i, inp in enumerate(valid_inputs, 1):
        is_valid = reflection_node.validate_input(inp)
        print(f"  有效输入 {i}: {is_valid} ✓")

    for i, inp in enumerate(invalid_inputs, 1):
        is_valid = reflection_node.validate_input(inp)
        print(f"  无效输入 {i}: {is_valid} ✓")
    print()


def test_node_composition(agent: DeepSearchAgent):
    """测试节点组合"""
    print("=" * 60)
    print("测试 6: 节点组合 (模拟工作流)")
    print("=" * 60)

    first_search_node = FirstSearchNode(llm_client=agent.llm_client)
    reflection_node = ReflectionNode(llm_client=agent.llm_client)

    # 模拟完整工作流
    initial_input = {
        "title": "量子计算的未来",
        "content": "探讨量子计算技术的发展趋势和应用前景"
    }

    print("步骤 1: 首次搜索")
    try:
        first_result = first_search_node.invoke(initial_input)
        print(f"✓ 首次搜索查询: {first_result.search_query}")
        print()

        # 模拟搜索后的状态
        reflection_input = {
            "title": initial_input["title"],
            "content": initial_input["content"],
            "paragraph_latest_state": f"已搜索: {first_result.search_query}. 获得了关于量子比特和量子纠缠的基础信息。"
        }

        print("步骤 2: 反思并生成新搜索")
        reflection_result = reflection_node.invoke(reflection_input)
        print(f"✓ 反思搜索查询: {reflection_result.search_query}")
        print(f"✓ 工作流完成")
        print()
    except Exception as e:
        print(f"✗ 工作流失败: {str(e)}")
        print()


def main():
    """主测试函数"""
    try:
        # 测试 LLM 初始化
        agent = test_llm_initialization()

        # 测试 FirstSearchNode
        test_first_search_node(agent)

        # 测试 ReflectionNode
        test_reflection_node(agent)

        # 测试节点组合
        test_node_composition(agent)

        print("=" * 60)
        print("所有测试完成!")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()






import sys, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))  # 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append('/workspaces/langchain')


from llm_client import llm_client # type: ignore
from deep_search_agent.nodes import ReflectionSummaryNode # type: ignore

# 初始化节点
reflection_summary_node = ReflectionSummaryNode(llm_client=llm_client)

# 方式 1: 使用 invoke (返回字符串)
updated_summary = reflection_summary_node.invoke({
    "title": "人工智能的发展",
    "content": "探讨 AI 技术的最新进展",
    "search_query": "大语言模型实际应用案例",
    "search_results": "搜索结果内容...",
    "paragraph_latest_state": "已经讨论了基础概念..."
})
print(updated_summary)  # 直接是字符串

# 方式 2: 使用原有接口 run (返回字符串)
updated_summary = reflection_summary_node.run({
    "title": "人工智能的发展",
    "content": "探讨 AI 技术的最新进展",
    "search_query": "大语言模型实际应用案例",
    "search_results": "搜索结果内容...",
    "paragraph_latest_state": "已经讨论了基础概念..."
})



# if __name__ == "__main__":
#     main()
