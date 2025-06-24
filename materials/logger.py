import logging
from typing import Optional

def get_logger(name: Optional[str] = None, level=logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name or __name__)
    if logger.hasHandlers():
        return logger  # 防止重复添加 handler

    logger.setLevel(level)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s", "%H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger



# logger = get_logger("pdf_extractor")
# logger.info("开始加载 PDF")
# logger.warning("找不到第一页内容，跳过")
# logger.error("模型调用失败，退出")