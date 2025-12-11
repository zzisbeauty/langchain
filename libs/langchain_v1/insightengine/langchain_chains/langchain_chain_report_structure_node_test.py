import sys
from pathlib import Path


project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))  


# from insightengine.config import Settings
from llms.bfishunifiedlangchainllm import vllm_model
from insightengine.langchain_chains.langchain_chain_report_structure_node import ReprotStructureChain


def test_report_structure_chain():
    # config = Settings()

    # print(type(vllm_model.llm), ":  ", vllm_model.llm)

    # chain 内部已经包含 llm，且 llm 支持外部导入，可以随时切换 llm server

    chain = ReprotStructureChain(vllm_model.llm)
    
    
    # test_query = "武汉大学舆情分析"
    # print(f"测试查询: {test_query}") 
    # print("=" * 50)
    # 构造符合 output_schema_report_structure 的输入
    input_for_chain = {
        "items": [
            {
                "title": "武汉大学舆情分析",
                "content": (
                    "近期，武汉大学在校内外的舆情呈现出多方面的讨论，涉及学术活动、校园管理、学生事务等，"
                    "公众关注度较高。网络舆情总体正面，但部分事件引发讨论和争议，需要学校及时回应。"
                )
            },
            {
                "title": "校园安全与管理",
                "content": (
                    "校园安全事件包括消防演练、交通管理和学生突发情况处理。舆论关注学校管理措施的透明度和效率，"
                    "建议进一步完善安全预案，加强信息公开与舆情监控。"
                )
            }
        ]
    }

    
    # 调用生成报告结构的 chain
    try:
        result = chain.generate_sturcture(input_for_chain)

        print(f"生成成功！共 {len(result)} 个段落:")  
        for i, paragraph in enumerate(result, 1):  
                print(f"\n{i}. 标题: {paragraph.get('title', 'N/A')}")  
                print(f"   内容: {paragraph.get('content', 'N/A')[:50]}...")  

        # 验证格式  
        if all(isinstance(p, dict) and 'title' in p and 'content' in p for p in result):  
                print("\n✅ 格式验证通过")  
        else:  
                print("\n❌ 格式验证失败") 
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")  
        import traceback  
        traceback.print_exc()  

if __name__ == "__main__":  
    test_report_structure_chain()