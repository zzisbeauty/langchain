import sys
from pathlib import Path  
sys.path.insert(0, str(Path(__file__).parent.parent))  # 添加项目根目录到 Python 路径

from llms.base import LLMClient
from nodes.report_structure_node import ReportStructureNode
from state.state import State


# from ..llms.base import LLMClient
# from .report_structure_node import ReportStructureNode
# from ..state.state import State


def main():
    llm_client = LLMClient()
    node = ReportStructureNode(llm_client=llm_client, query="如何评价中国研制的 J-20")

    print("\n===== run() =====")
    result = node.run()
    for i, p in enumerate(result, 1):
        print(f"{i}. {p['title']} - {p['content']}")

    print("\n===== mutate_state() =====")
    state = node.mutate_state(state=State())
    print("Report title:", state.report_title)
    for i, p in enumerate(state.paragraphs, 1):
        print(f"{i}. {p['title']}\n   {p['content']}")

if __name__ == "__main__":
    main()