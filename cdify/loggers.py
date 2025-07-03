import os, sys
import logging
import threading
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

class CustomFormatter(logging.Formatter):
    def format(self, record):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        trace_id = getattr(record, 'trace_id', 'N/A')
        system_name = getattr(record, 'system_name', 'N/A')
        domain_service = getattr(record, 'domain_service', 'N/A')
        thread_id = threading.get_ident()
        class_name = record.pathname.split('/')[-1].replace('.py', '')
        method_name = record.funcName
        line_number = record.lineno
        log_level = record.levelname
        message = record.getMessage()
        log_entry = (
            f"[{timestamp}]-[{trace_id}]-[{system_name}-{domain_service}]"
            f"-[{thread_id}]-[{class_name}.{method_name}.{line_number}]-[{log_level}]:{message}"
        )
        return log_entry

class CustomLogger(logging.Logger):
    def __init__(self, name, system_name, domain_service):
        super().__init__(name)
        self.system_name = system_name
        self.domain_service = domain_service

    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False, stacklevel=1):
        if extra is None:
            extra = {}
        extra['system_name'] = self.system_name
        extra['domain_service'] = self.domain_service
        super()._log(level, msg, args, exc_info, extra, stack_info, stacklevel)

def get_logger(name, system_name='Linux', domain_service='task_name', log_dir=None):
    # 日志目录默认为项目根目录下 loggers_dir/
    if log_dir is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        log_dir = os.path.join(base_dir, 'loggers')
    os.makedirs(log_dir, exist_ok=True)

    logger = CustomLogger(name, system_name, domain_service)

    def custom_filename(filename):
        base, ext = os.path.splitext(filename)
        return f"{base}_{datetime.now().strftime('%Y-%m-%d')}{ext}"

    log_file = custom_filename(os.path.join(log_dir, f"{name}.log"))

    handler = TimedRotatingFileHandler(
        filename=log_file,
        when='midnight',
        interval=1,
        backupCount=30,
        encoding='utf-8',
        utc=True
    )

    def rename_log_files(handler):
        for i in range(handler.backupCount - 1, 0, -1):
            sfn = handler.rotation_filename(f"{handler.baseFilename}.{i}")
            dfn = handler.rotation_filename(f"{handler.baseFilename}.{i + 1}")
            if os.path.exists(sfn):
                os.rename(sfn, dfn)
        dfn = handler.rotation_filename(handler.baseFilename + ".1")
        if os.path.exists(handler.baseFilename):
            os.rename(handler.baseFilename, dfn)
        return custom_filename(handler.baseFilename)

    handler.namer = rename_log_files
    formatter = CustomFormatter()
    handler.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(handler)

    logger.setLevel(logging.DEBUG)
    return logger


# 示例用法
# LOGS = 'logs'  # 存储日志的文件夹
# OSNAME = 'Linux'  # 操作系统
# DOMAIN_SERVICE = 'task_name'  # 任务信息
# logger = get_logger(__name__, system_name=OSNAME, domain_service=DOMAIN_SERVICE, log_dir=LOGS)
# logger.info("日志系统初始化成功！")



from cdify.tools import OS_NAME

logger_config = {
    'system_name': OS_NAME,
    'domain_service': 'chat-service-hanwe',
    'log_dir': None  # 默认为 None，使用默认日志目录
}

logger = get_logger(__name__, system_name=logger_config['system_name'], domain_service=logger_config['domain_service'], log_dir=logger_config['log_dir'])