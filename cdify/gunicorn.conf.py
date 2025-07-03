bind = "0.0.0.0:5627"
workers = 4

worker_class = "sync"  # # 进程内并发: 也可以换成 WSGI   gevent、  # ASGI    uvicorn.workers.UvicornWorker 
# threads = 2 #  每个进程开启的线程数目

timeout = 120
accesslog = "-"
errorlog = "-"
loglevel = "info"

# 启动命令
# gunicorn fast_server:app -c gunicorn.conf.py

# 后台启动
# nohup gunicorn -w 4 -b 0.0.0.0:5627 fast_server:app > gunicorn.log 2>&1 &
# 启动后检查进程 ps -ef | grep gunicorn
# kill pid 停止服务 or  pkill gunicorn

# 高阶管理 gunicorn pid 方案
# nohup gunicorn -w 4 -b 0.0.0.0:5627 fast_server:app --pid gunicorn.pid > gunicorn.log 2>&1 &
# 杀死进程 kill $(cat gunicorn.pid)