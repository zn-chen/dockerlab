# -*- coding: utf-8 -*-
import sys
from signal import signal, SIGINT, SIGTERM
from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.options import options
from tornado.netutil import bind_sockets
from tornado.httpserver import HTTPServer
import logging

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
        self._log = logging.getLogger()
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

        logging.basicConfig(
            level=getattr(logging, (self._config.log_level or "").upper(), logging.INFO),
            format="[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d]%(message)s",
            datefmt="%y%m%d %H:%M:%S"
        )

        self._log.info("configuration initialization")

    def start(self):
        """
        启动tornado
        :return:
        """
        self._log.info(LOGO)
        self._server.add_sockets(self._sockets)
        self._log.info("tornado service start")
        scheduled.start()
        self._log.info("scheduled task start")
        self._ioloop.start()

    def stop(self, code=0, frame=None):
        """
        停止tornado服务
        :return:
        """
        self._server.stop()
        self._log.info("http service stop")
        self._ioloop.stop()
        self._log.info("tornado service exit")
        sys.exit(0)


if __name__ == r'__main__':
    Entry().start()
