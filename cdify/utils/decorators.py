# 接口计时
import time
from functools import wraps
from cdify.utils.loggers import logger
from flask import make_response, jsonify


def timed_request(func):
    """ 优化输出 """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        response = func(*args, **kwargs)
        # duration_ms = round((time.perf_counter() - start) * 1000, 2)
        duration_s = round(time.perf_counter() - start, 4)  # 精确到 4 位小数

        # 注入耗时字段（如果返回的是 dict）
        if isinstance(response, dict):
            response['elapsed_s'] = duration_s

        # print(f"[{func.__name__}] 请求耗时: {duration_s} s")
        # 可选：将日志写入 logger，避免 gunicorn 打印不到 print
        # logger.info(f"[{func.__name__}] 请求耗时: {duration_s} s")

        return response
    
    return wrapper
