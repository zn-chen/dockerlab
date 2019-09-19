# -*- coding: utf-8 -*-
from tornado import gen
import time
from tornado.web import RequestHandler
from tornado.log import gen_log

from model import DockerClient
from service.base import ServerBase
from service.container_server import ContainerServer, get_containers_info


class Container(RequestHandler):
    """
    容器操作接口
    """

    async def post(self, container_id=None):
        """
        对容器操作均为post,请求格式为:
        {
            "option":"option"
            "paramList": {
                params,
                ...
            }
        }
        """
        container_server = ContainerServer(request=self, docker_client=DockerClient, container_id=container_id)
        # 查询并初始化容器服务,如果初始化失败直接返回.
        result = await container_server.init_container_info()
        if not result:
            return

        await container_server.execute(
            option=self.get_body_argument("option"),
            params=self.get_body_argument("params"),
        )


class Containers(RequestHandler):
    """
    容器信息列表查询接口
    """

    async def get(self):
        """
        查询所有容器的简略信息
        """
        server = ServerBase(request=self)
        try:
            containers_info = await get_containers_info(docker_client=DockerClient)
            await server.send_message(data=containers_info)
        except Exception as e:
            gen_log.error(e)
            await server.on_err(code="500")