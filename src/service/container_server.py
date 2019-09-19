# -*- coding: utf-8 -*-
import json
from logging import getLogger
from aiodocker import Docker

from service.base import *
from util.serialization import container_brief_info_serialize
from model.container import get_container
from model.container import Container as ContainerDB


class ContainerServer(ServerBase):
    """
    容器操作中心

    收到对应报文后根据对应的option进行对应的不同操作
    options:
        create:     创建容器
        start:      启动容器
        delete:     删除容器
        query:      查询容器详细信息
        delay:      设置容器销毁时间
    """
    _log = getLogger()

    def __init__(self, request: RequestHandler, docker_client: Docker, container_id):

        self.docker_client = docker_client
        super(ContainerServer, self).__init__(request)

        self._handlers = {
            "start": self._on_start,
            "create": self._on_create,
            "delete": self._on_delete,
            "query": self._on_query,
            "delay": self._on_delay,
            "stop": self._on_stop,
        }
        self.container_id = container_id

        # 容器是否存在
        self.container_is = None
        # 容器客户端
        self.container_client = None

    async def init_container_info(self) -> bool:
        """
        必须在执行容器客户端之前显示调用
        初始化容器信息
        """
        if self.container_id is None:
            self.container_is = False
            return True
        try:
            self.container_client = await self.docker_client.containers.get(self.container_id)
            return True
        except Exception as e:
            # 如果提供的id无法查询到容器则直接拒绝访问
            self._log.debug("The container could not be found")
            await self.send_message(code="400")
            return False

    async def execute(self, option: str, params: str) -> None:
        """
        执行对应的options
        """
        # 获得操作对应的的_handler
        _handler = self._handlers.get(option)
        if _handler is None:
            self._log.error("Can't find options {}".format(option))
            await self.on_err(code="300")
            return

        # 序列化参数列表
        try:
            params = json.loads(params)
        except Exception as e:
            self._log.error(e)
            await self.on_err(code="400")
            return

        # 执行对应的操作
        try:
            await _handler(params)
        except Exception as e:
            self._log.error(e)
            await self.on_err(code=e.__str__())

    @staticmethod
    def _is_running(info: dict) -> bool:
        if info.get("State").get("Status") == "running":
            return True
        else:
            return False

    async def _on_create(self, params: dict) -> None:
        """
        判断params缺省,填充部分默认参数
        以下_on_XX方法同上
        """
        image_list = params.get("imageList")
        if image_list is None or image_list == []:
            raise ParamsException()

        await self.on_create(image_list=image_list)

    async def _on_start(self, params: dict) -> None:
        await self.on_start()

    async def _on_stop(self, params: dict) -> None:
        await self.on_stop()

    async def _on_delete(self, params: dict) -> None:
        await self.on_delete()

    async def _on_query(self, params: dict) -> None:
        await self.on_query()

    async def _on_delay(self, params: dict) -> None:
        destroy_time = params.get("destroyTime")
        if destroy_time is None:
            raise ParamsException()

        await self.on_delay(destroy_time=destroy_time)

    async def on_create(self, image_list: list) -> None:
        """
        创建容器
        # TODO: 容器端口设置存在争议
        """
        container_infos = {}
        container_ids = {}

        for i in image_list:
            image = str(i)

            image_info = await self.docker_client.images.get(image)
            exposed_ports = image_info.get("Config").get("ExposedPorts")
            host_config = None
            if exposed_ports is not None:
                host_config = {"PortBindings": {}}
                for i in exposed_ports:
                    host_config["PortBindings"][i] = [{"HostPort": None}]

            tmp = await self.docker_client.containers.create_or_replace(
                config={
                    "image": image,
                    "ExposedPorts": exposed_ports,
                    "HostConfig": host_config,
                },
                name=None,
            )
            info = await tmp.show()

            # 创建数据库记录
            container_db = ContainerDB(container_info=info)
            await container_db.write()

            info = container_brief_info_serialize(info)
            container_infos[image] = info
            container_ids[image] = info.get("containerId")

        await self.send_message(
            data=container_infos,
        )

        self._log.info("Containers be create {0} {1}".format(container_ids, self.request.request.remote_ip))

    async def on_start(self) -> None:
        """
        启动容器
        """
        await self.container_client.start()
        await self._on_query(params=dict())

        self._log.info("Start container {0} ({1})".format(self.container_id, self.request.request.remote_ip))

    async def on_stop(self) -> None:
        """
        停止运行中容器
        """
        await self.container_client.stop()
        await self._on_query(dict())

        self._log.info("Stop container {0} ({1})".format(self.container_id, self.request.request.remote_ip))

    async def on_delete(self) -> None:
        """
        删除容器操作
        """
        info = await self.container_client.show()

        if self._is_running(info=info):
            await self.send_message(
                code=601,
                message="You cannot delete a running container",
            )
            self._log.info("Can not delete container {0} , not stop container ({1})".format(
                self.container_id, self.request.request.remote_ip))
            return

        await self.container_client.delete()
        await self.send_message(
            data=container_brief_info_serialize(info),
        )

        # 删除数据库中的记录
        container_db = await get_container(_id=self.container_id)
        await container_db.remove()

        self._log.info("Delete container {0} ({1})".format(self.container_id, self.request.request.remote_ip))

    async def on_query(self) -> None:
        """
        查询容器的简略信息
        """
        info = await self.container_client.show()
        data = container_brief_info_serialize(info)

        try:
            container_db = await get_container(_id=self.container_id)
            data['destroyTime'] = container_db.get_dict().get("destroyTime")
        except Exception as e:
            pass

        await self.send_message(data=data)
        self._log.info("Query container {0} ({1})".format(self.container_id, self.request.request.remote_ip))

    async def on_delay(self, destroy_time) -> None:
        """
        延迟容器销毁时间
        """
        container_db = await get_container(_id=self.container_id)
        await container_db.set_destroy_time(destroy_time=destroy_time)

        await self._on_query(dict())
        self._log.info("Delay container {0} {1} ({2})".format(self.container_id, destroy_time,
                                                            self.request.request.remote_ip))


async def get_containers_info(docker_client: Docker):
    """
    获取所有容器的简略信息
    """
    containers_list = await docker_client.containers.list(all=True)
    data = []
    for i in containers_list:
        info = container_brief_info_serialize(await i.show())
        container_id = info.get("containerId")

        try:
            container_db = await get_container(_id=container_id)
            info['destroyTime'] = container_db.get_dict().get("destroyTime")
        except Exception as e:
            pass

        data.append(info)

    return data 
