from flask import Blueprint
from cdify.utils.config import *
from cdify.utils.decorators import timed_request


# 一 添加蓝图
health = Blueprint('health', __name__)


# 二 构造蓝图路由
@health.route(BASE_URL + '/hello', methods=['GET'])
@timed_request # 此处为视图函数
def healthy_check():
    from cdify.dify_client.health import say_hello
    response = say_hello()
    if response.status_code != 200: # info == 错误信息说明
        return {
            'code': -1, 'data': "", 
            'message': 'Healthy check failed!',
        }
    return {
        'code': 0, 'data': '',
        'message': 'Healthy check successful!',
    }