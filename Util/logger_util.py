import logging


# 错误日志
def error_log(message):
    logger = logging.getLogger(__name__)
    logger.error(message)
    raise Exception(message)


# 信息日志的输出
def info_log(message):
    logger = logging.getLogger(__name__)
    logger.info(message)
