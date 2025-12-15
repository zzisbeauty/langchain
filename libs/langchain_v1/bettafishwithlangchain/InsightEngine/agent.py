"""  改写 DeepSearchAgent 类，将其转换为 LangChain Agent 架构。

整合所有模块，实现完整的深度搜索流程
"""

import json
import os
import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Union


import numpy as np
from loguru import logger
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans


from llms.base import LLMClient

