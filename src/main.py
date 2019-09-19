# -*- coding: utf-8 -*-
import sys
import os
import time
from signal import signal, SIGINT, SIGTERM
from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.options import options, define
from tornado.netutil import bind_sockets
from tornado.httpserver import HTTPServer
from tornado.log import gen_log

from router import ROUTER
from conf import Config
import scheduled


LOGO = """
╔╦╗┌─┐┌─┐┬┌─┌─┐┬─┐╦  ┌─┐┌┐ 
 ║║│ ││  ├┴┐├┤ ├┬┘║  ├─┤├┴┐
═╩╝└─┘└─┘┴ ┴└─┘┴└─╩═╝┴ ┴└─┘"""

class Entry(object):
    """
    程序入口类
    """

    def __init__(self):
        """
        构造器
        """
        self._config = Config
        self._options = options
        self._ioloop = IOLoop.current()
        self._sockets = bind_sockets(self._config.base_port)

        self._init_options()

        # exit signal
        signal(SIGINT, lambda sig, frame: self._ioloop.add_callback_from_signal(self.stop))
        signal(SIGTERM, lambda sig, frame: self._ioloop.add_callback_from_signal(self.stop))

        self._server = HTTPServer(Application(**self._settings))

    def _init_options(self):
        """
        初始化配置
        :return:
        """
        # make application setting
        self._settings = {
            r'handlers': ROUTER,
        }

        # init log
        self._options.logging = self._config.log_level

        # log to file
        if self._config.log_to_file:
            self._options.log_rotate_mode = self._config.log_rotate_mode

            # 时间分割
            if self._config.log_rotate_mode == "time":
                self._options.log_rotate_when = self._config.log_rotate_when
                self._options.log_rotate_interval = self._config.log_rotate_interval

            # 文件大小分割
            elif self._config.log_rotate_mode == "size":
                self._options.log_max_size = self._config.log_file_max_size

            else:
                # TODO 日志初始化失败通知
                pass
            self._options.log_file_num_backups = self._config.log_file_num_backups

            options.log_file_prefix = r'{0:s}/runtime-{1:s}.pid-{2:s}.log'.format(
                self._config.log_file_path,
                time.strftime("%Y-%m-%d", time.localtime()),
                str(os.getpid()),
            )

        # log to stderr
        self._options.log_to_stderr = self._config.log_to_stderr

        # start log
        self._options.parse_command_line()

        gen_log.info("configuration initialization")

    def start(self):
        """
        启动tornado
        :return:
        """
        gen_log.info(LOGO)
        self._server.add_sockets(self._sockets)
        gen_log.info("tornado service start")
        scheduled.start()
        gen_log.info("scheduled task start")
        self._ioloop.start()

    def stop(self, code=0, frame=None):
        """
        停止tornado服务
        :return:
        """
        self._server.stop()
        gen_log.info("http service stop")
        self._ioloop.stop()
        gen_log.info("tornado service exit")
        sys.exit(0)


if __name__ == r'__main__':
    Entry().start()
