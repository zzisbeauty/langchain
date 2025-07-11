import os
import sys
import json, requests
from flask import Flask, request, jsonify
import platform
import pathlib

# func-1
sys.path.append(os.getcwd())

# func-2
# OS_NAME = platform.system()
# if OS_NAME == "Windows":
#     sys.path.append(r"E:\langchain-core-0.3.64")
# else:
#     sys.path.append('/home/langchain')

# func-3
# project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# if project_root not in sys.path:
#     sys.path.append(project_root)



from cdify.utils.loggers import logger
from api import all_blueprints

app = Flask(__name__)

for bp in all_blueprints:
    app.register_blueprint(bp)


if __name__ == '__main__':
    logger.info("日志系统初始化成功！ Server Running...")

    # windows local
    # app.run(debug=True, host='0.0.0.0', port=5611)

    # servr docker
    app.run(debug=True, host='0.0.0.0', port=5627)
