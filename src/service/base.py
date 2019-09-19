# -*- coding: utf-8 -*-
from copy import deepcopy
from tornado.web import RequestHandler

MESSAGE_CODE = {
    "200": "success",  # 正常返回
    "300": "Invalid operation",  # 无效操作
    "400": "Invalid params",  # 无效参数
    "500": "unknown exception",  # 未知异常
}


class ExceptionBase(Exception):
    """
    内部异常基类
    """

    def __init__(self, code: int):
        super().__init__()
        self._code = str(code)

    def __str__(self):
        return self._code


class ParamsException(ExceptionBase):
    """
    缺少必要参数或参数异常
    """

    def __init__(self):
        super().__init__(code=400)


class OptionException(ExceptionBase):
    """
    操作异常
    """

    def __init__(self):
        super().__init__(code=300)


class ServerBase(object):
    """
    服务基类
    """

    def __init__(self, request: RequestHandler):
        self.request = request

        self._template = {
            "meta": {
                "code": 200,
                "message": None,
            },
            "data": None,
        }

    async def on_err(self, code: str, data=None):
        """
        返回一个带有异常信息的报文,并在日志中记录对应的异常.
        """
        message = MESSAGE_CODE.get(code)
        if message is None:
            code = "500"
            message = MESSAGE_CODE.get(code)

        # 返回失败信息
        await self.send_message(
            code=int(code),
            message=message,
            data=data,
        )

    async def send_message(self, code=200, message=None, data=None):
        """
        发送一个固定格式的报文.
        """
        tmp = deepcopy(self._template)
        tmp['meta']['code'] = int(code)
        tmp['meta']['message'] = message
        tmp['data'] = data

        self.request.write(tmp)
