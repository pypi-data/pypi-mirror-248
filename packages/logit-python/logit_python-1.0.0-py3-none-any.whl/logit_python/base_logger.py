#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
log base module
日志规范：https://ku.baidu-int.com/knowledge/HFVrC7hq1Q/pKzJfZczuc/I1E7bZqZ7Q/MSvKRRmYufHF20
"""

import logging
import logging.handlers
import os
import sys

# 自定义LOG等级 - TRACE
level_trace = logging.INFO + 1
trace_name = 'TRACE'
logging.addLevelName(level_trace, trace_name)


def my_excepthook(exc_type, exc_value, traceback):
    logging.error(
        'Uncaught Exception',
        exc_info=(exc_type, exc_value, traceback)
    )


sys.excepthook = my_excepthook


class Logger(object):
    def __init__(self, config_dict: dict):
        conf_file_path = config_dict.get("file_name")
        if Logger.isabs(conf_file_path):
            # log文件路径是绝对路径
            log_dir = os.path.dirname(conf_file_path)
        else:
            # log文件路径是相对当前工作目录的路径
            file_path = os.path.join(os.getcwd(), conf_file_path)
            log_dir = os.path.dirname(file_path)

        # 创建log目录
        Logger.make_log_dir(log_dir)

        logger_name = config_dict.get("logger_name")
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)

        # 日志格式
        log_fmt = '%(levelname)s: %(asctime)s %(filename)s[line:%(lineno)d] %(message)s'
        # 默认日志时间精确到秒，default_ms参数精确到毫秒
        date_fmt = '%Y-%m-%d %H:%M:%S'
        if config_dict.get("prefix") == 'default_ms':
            date_fmt = None
        format_str = logging.Formatter(log_fmt, datefmt=date_fmt)  # 设置日志格式

        # 输出日志到控制台
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(format_str)
        stream_handler.setLevel(logging.DEBUG)
        self.logger.addHandler(stream_handler)

        # log文件的数量
        log_backup_count = 15
        if config_dict.get("max_file_num") >= 15 or config_dict.get("max_file_num") <= 31:
            log_backup_count = config_dict.get("max_file_num")

        # 日志按时间切分规则
        when = 'D'

        # ################################### debug log config  ######################################################
        if len(config_dict.get("debug_file_suffix")) > 0:
            # 日志文件名字
            debug_log_file = conf_file_path + config_dict.get("debug_file_suffix")

            debug_filter = logging.Filter()
            debug_filter.filter = lambda record: record.levelno == logging.DEBUG

            # 日志文件处理
            debug_file_handler = logging.handlers.TimedRotatingFileHandler(
                filename=debug_log_file,
                when=when,  # 日志文件按时间切分规则，目前只支持按天切分文件
                interval=1,  # 每1天切分文件
                backupCount=log_backup_count,  # 日志滚存文件数量
                encoding='utf-8')
            debug_file_handler.setFormatter(format_str)  # 设置文件里写入的格式
            debug_file_handler.addFilter(debug_filter)  # 设置日志文件过滤器
            self.logger.addHandler(debug_file_handler)

        # ################################### info or trace log config  ##############################################
        if len(config_dict.get("info_file_suffix")) > 0:
            # 日志文件名字
            info_log_file = conf_file_path + config_dict.get("info_file_suffix")

            info_filter = logging.Filter()
            info_filter.filter = lambda record: record.levelno == logging.INFO or record.levelno == level_trace

            # 日志文件处理
            info_file_handler = logging.handlers.TimedRotatingFileHandler(
                filename=info_log_file,
                when=when,  # 日志文件按时间切分规则，目前只支持按天切分文件
                interval=1,  # 每1天切分文件
                backupCount=log_backup_count,  # 日志滚存文件数量
                encoding='utf-8')
            info_file_handler.setFormatter(format_str)  # 设置文件里写入的格式
            info_file_handler.addFilter(info_filter)  # 设置日志文件过滤器
            self.logger.addHandler(info_file_handler)

        # ################################### warning or above log config  ###########################################
        if len(config_dict.get("wf_file_suffix")):
            # 日志文件名字
            warn_log_file = conf_file_path + config_dict.get("wf_file_suffix")

            warn_filter = logging.Filter()
            warn_filter.filter = lambda record: record.levelno >= logging.WARNING

            # 日志文件处理
            warn_file_handler = logging.handlers.TimedRotatingFileHandler(
                filename=warn_log_file,
                when=when,  # 日志文件按时间切分规则，目前只支持按天切分文件
                interval=1,  # 每1天切分文件
                backupCount=log_backup_count,  # 日志滚存文件数量
                encoding='utf-8')
            warn_file_handler.setFormatter(format_str)  # 设置文件里写入的格式
            warn_file_handler.addFilter(warn_filter)  # 设置日志文件过滤器
            self.logger.addHandler(warn_file_handler)

    @staticmethod
    def make_log_dir(log_dir):
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

    @staticmethod
    def isabs(file_path: str) -> bool:
        s = os.fspath(file_path)  # 判断path类型是否str或bytes,否抛出异常
        return s.startswith('/')


def format_message(message, **kwargs):
    tags = str()
    for key, value in kwargs.items():
        tags += "{key}[{value}] ".format(key=key, value=value)

    if len(tags) > 0:
        return tags + "message[" + message + "]"

    return "message[" + message + "]"
