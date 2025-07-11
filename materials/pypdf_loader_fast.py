import sys
import os, pathlib
# print("CWD :", os.getcwd())
sys.path.append(os.getcwd())

from cdify.utils.loggers import get_logger
logger = get_logger("pdf_extractor_log_obj")

import langchain_community
print(langchain_community.__file__)

from langchain.prompts import ChatPromptTemplate

from langchain_community.llms import Ollama
from langchain.document_loaders import PyPDFLoader
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_community.document_loaders import UnstructuredPDFLoader

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableMap

# logger.info('import success')

# 矢量图型PDF
# pdf_path = r"C:\Users\lenovo\Desktop\02-标准及政策文件合集\01-强制性国家标准\现行_GB51222-2017_《城镇内涝防治技术规范》.pdf"
# pdf_path = r"C:\Users\lenovo\Desktop\02-标准及政策文件合集\01-强制性国家标准\现行_GBT39195-2020_《城市内涝风险普查技术规范》.pdf"
pdf_path = './materials/pdf_data/文字型PDF/TCECS 20002-2020_《城市供水信息系统基础信息加工处理 技术指南》.pdf'

# 标准文字型PDF
# pdf_path = r'E:\其他文件\知识库接口逻辑梳理-无权限控制.pdf'


loader = PyPDFLoader(pdf_path)
# loader = PDFPlumberLoader(pdf_path)
# loader = UnstructuredPDFLoader(pdf_path, mode="elements") # × windows 无法运行，缺失且无法安装  pip install python-heif -i https://pypi.tuna.tsinghua.edu.cn/simple

docs = loader.load()
texts = [doc.page_content for doc in docs]
print(texts)
logger.info('load and pasered')
"""
[
  Document(
    page_content="这一页的纯文本",
    metadata={"source": "...", "page": 1}
  ),
  Document(
    page_content="下一页的纯文本",
    metadata={"source": "...", "page": 2}
  ),
  ...
]
"""