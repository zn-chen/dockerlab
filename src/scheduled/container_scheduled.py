# -*- coding: utf-8 -*-
import time
from tornado.ioloop import PeriodicCallback
from logging import getLogger

from model.container import get_containers_info, get_container
from model import DockerClient


async def del_containers(container_id: str) -> None:
    try:
        container_remote = await DockerClient.containers.get(container_id)
        await container_remote.stop()
        await container_remote.delete()
    except Exception as e:
        # TODO:此处无法找到容器的处理有待商榷
        getLogger().error(e)

    container_db = await get_container(_id=container_id)
    await container_db.remove()

    getLogger().info("Delete the expired container {}".format(container_id))


async def containers_clear():
    """
    清理过期容器
    """
    # getLogger().debug("Execute the scheduled task containers_clear")

    judge = lambda destroy_time: True if destroy_time <= int(time.time()) else False
    async for i in get_containers_info():
        destroy_time = i.get("destroyTime")
        if destroy_time is None:
            continue

        if judge(destroy_time):
            await del_containers(i.get("_id"))


CONTAINER_TASK_LIST = [
    PeriodicCallback(containers_clear, 2*1000),
]
