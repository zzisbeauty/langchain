"""  
重试机制工具模块  
提供 with_retry 和 with_graceful_retry 装饰器  
"""  
  
from typing import Any, Callable, Optional  
from functools import wraps  
from tenacity import (  
    retry,  
    stop_after_attempt,  
    wait_exponential,  
    retry_if_exception_type,  
    before_sleep_log,  
    after_log  
)  
import logging  
  
# 配置日志  
logger = logging.getLogger(__name__)  
  
# LLM 调用重试配置  
LLM_RETRY_CONFIG = {  
    "stop": stop_after_attempt(3),  
    "wait": wait_exponential(multiplier=1, min=4, max=10),  
    "retry": retry_if_exception_type((ConnectionError, TimeoutError, Exception)),  
    "before": before_sleep_log(logger, logging.WARNING),  
    "after": after_log(logger, logging.INFO)  
}  
  
# 搜索 API 重试配置  
SEARCH_API_RETRY_CONFIG = {  
    "stop": stop_after_attempt(3),  
    "wait": wait_exponential(multiplier=1, min=4, max=10),  
    "retry": retry_if_exception_type((ConnectionError, TimeoutError, Exception)),  
    "before": before_sleep_log(logger, logging.WARNING),  
    "after": after_log(logger, logging.INFO)  
}  
  
  
def with_retry(config: dict):  
    """ 基础重试装饰器，失败后抛出异常  
    Args:  
        config: tenacity 重试配置  
    Returns:  
        装饰器函数  
    """  
    def decorator(func: Callable) -> Callable:  
        @wraps(func)  
        @retry(**config)  
        def wrapper(*args, **kwargs):  
            return func(*args, **kwargs)  
        return wrapper  
    return decorator  
  
  
def with_graceful_retry(config: dict, default_return: Any = None):  
    """  优雅降级重试装饰器，失败后返回默认值  
    Args:  
        config: tenacity 重试配置  
        default_return: 重试失败后的默认返回值  
    Returns:  
        装饰器函数  
    """  
    def decorator(func: Callable) -> Callable:  
        @wraps(func)  
        def wrapper(*args, **kwargs):  
            try:  
                @retry(**config)  
                def _retry_func():  
                    return func(*args, **kwargs)  

                return _retry_func()  
            except Exception as e:  
                logger.error(f"函数 {func.__name__} 重试失败，返回默认值: {str(e)}")  
                return default_return  
        return wrapper  
    return decorator
