#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
@Author: Rodney Cheung
@Date: 2020-04-29 17:02:25
@LastEditors: Sphantix Hang
@LastEditTime: 2020-05-13 10:15:39
@FilePath: /Wesker/core/mods/log.py
'''

import logging
import os
import sys
import time
import io
import traceback


class MyLogger(logging.Logger):
    def findCaller(self, stack_info=False, stacklevel=1):
        n_frames_upper = 2
        f = logging.currentframe()
        for _ in range(n_frames_upper):  # <-- correct frame
            if f is not None:
                f = f.f_back
        rv = "(unknown file)", 0, "(unknown function)", None
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename == logging._srcfile:
                f = f.f_back
                continue
            sinfo = None
            if stack_info:
                sio = io.StringIO()
                sio.write('Stack (most recent call last):\n')
                traceback.print_stack(f, file=sio)
                sinfo = sio.getvalue()
                if sinfo[-1] == '\n':
                    sinfo = sinfo[:-1]
                sio.close()
            rv = (co.co_filename, f.f_lineno, co.co_name, sinfo)
            break
        return rv


class Log:
    logging.setLoggerClass(MyLogger)
    console_logger = None
    console_handler = None
    log_formatter = logging.Formatter(
        "%(asctime)s %(funcName)s %(lineno)d %(levelname)s: %(message)s")
    is_log_to_file = False
    is_log_to_console = True
    file_loggers = {}

    LOG_DIR = os.path.join(
        os.getcwd(), "runtime", "log", time.strftime("%Y-%m-%d %H:%M:%S",
                                          time.localtime()))
    if not (os.path.exists(LOG_DIR) and os.path.isdir(LOG_DIR)):
        os.makedirs(LOG_DIR)

    LOG_DEBUG_PATH = os.path.join(LOG_DIR, "debug.log")
    LOG_INFO_PATH = os.path.join(LOG_DIR, "info.log")
    LOG_ERROR_PATH = os.path.join(LOG_DIR, "error.log")
    LOG_WARNING_PATH = os.path.join(LOG_DIR, "warning.log")
    LOG_CRITICAL_PATH = os.path.join(LOG_DIR, "critical.log")

    log_path_dict = {
        logging.DEBUG: LOG_DEBUG_PATH,
        logging.WARNING: LOG_WARNING_PATH,
        logging.ERROR: LOG_ERROR_PATH,
        logging.CRITICAL: LOG_CRITICAL_PATH,
        logging.INFO: LOG_INFO_PATH
    }

    file_handler_created_flag = {
        logging.DEBUG: False,
        logging.WARNING: False,
        logging.ERROR: False,
        logging.CRITICAL: False,
        logging.INFO: False
    }

    @classmethod
    def init_logger(cls,
                    name,
                    console_log_level=logging.DEBUG,
                    isLogToConsole=True,
                    isLogToFile=False):
        cls.is_log_to_console = isLogToConsole
        if isLogToConsole:
            cls.console_handler = logging.StreamHandler()
            cls.console_handler.setFormatter(cls.log_formatter)
            cls.console_handler.setLevel(console_log_level)
            cls.console_logger = logging.getLogger(name)
            cls.console_logger.setLevel(logging.DEBUG)
            cls.console_logger.addHandler(cls.console_handler)
        cls.is_log_to_file = isLogToFile

    @classmethod
    def __position_format(cls, *args):
        position_str = '{}'
        position_str_list = list()
        arglen = len(args)
        while arglen > 0:
            position_str_list.append(position_str)
            arglen -= 1
        return "".join(position_str_list).format(*args)

    @classmethod
    def debug(cls, *msg):
        data = cls.__position_format(*msg)
        if cls.is_log_to_console:
            cls.console_logger.debug(data)
        if cls.is_log_to_file:
            if not cls.file_handler_created_flag[logging.DEBUG]:
                cls.add_file_handler(cls.LOG_DEBUG_PATH, logging.DEBUG)
                cls.file_handler_created_flag[logging.DEBUG] = True
            cls.file_loggers[logging.DEBUG].debug(data)

    @classmethod
    def info(cls, *msg):
        data = cls.__position_format(*msg)
        if cls.is_log_to_console:
            cls.console_logger.info(data)
        if cls.is_log_to_file:
            if not cls.file_handler_created_flag[logging.INFO]:
                cls.add_file_handler(cls.LOG_INFO_PATH, logging.INFO)
                cls.file_handler_created_flag[logging.INFO] = True
            cls.file_loggers[logging.INFO].info(data)

    @classmethod
    def warning(cls, *msg):
        data = cls.__position_format(*msg)
        if cls.is_log_to_console:
            cls.console_logger.warning(data)
        if cls.is_log_to_file:
            if not cls.file_handler_created_flag[logging.WARNING]:
                cls.add_file_handler(cls.LOG_WARNING_PATH, logging.WARNING)
                cls.file_handler_created_flag[logging.WARNING] = True
            cls.file_loggers[logging.WARNING].warning(data)

    @classmethod
    def error(cls, *msg):
        data = cls.__position_format(*msg)
        if cls.is_log_to_console:
            cls.console_logger.error(data)
        if cls.is_log_to_file:
            if not cls.file_handler_created_flag[logging.ERROR]:
                cls.add_file_handler(cls.LOG_ERROR_PATH, logging.ERROR)
                cls.file_handler_created_flag[logging.ERROR] = True
            cls.file_loggers[logging.ERROR].error(data)

    @classmethod
    def critical(cls, *msg):
        data = cls.__position_format(*msg)
        if cls.is_log_to_console:
            cls.console_logger.critical(data)
        if cls.is_log_to_file:
            if not cls.file_handler_created_flag[logging.CRITICAL]:
                cls.add_file_handler(cls.LOG_CRITICAL_PATH, logging.CRITICAL)
                cls.file_handler_created_flag[logging.CRITICAL] = True
            cls.file_loggers[logging.CRITICAL].critical(data)

    @classmethod
    def add_file_handler(cls, log_file, log_level):
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(cls.log_formatter)
        file_handler.setLevel(log_level)
        file_logger = logging.getLogger(str(log_level))
        file_logger.setLevel(logging.DEBUG)
        file_logger.addHandler(file_handler)
        cls.file_loggers.update({log_level: file_logger})

    @classmethod
    def set_console_loglevel(cls, log_level):
        cls.console_handler.setLevel(log_level)

    @classmethod
    def close(cls):
        cls.clear_file_handler()

    @classmethod
    def clear_file_handler(cls):
        for l in cls.file_loggers:
            cls.file_loggers[l].handlers[0].close()
            cls.file_handler_created_flag[l] = False
        cls.file_loggers.clear()
