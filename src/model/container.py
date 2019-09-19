# -*- coding: utf-8 -*-
import time
from pymongo.results import UpdateResult, InsertOneResult, DeleteResult

from model import DBClient
from conf import Config


class Container(object):
    def __init__(self, _id=None, destroy_time=None, port=None, host_ip=None,
                 container_info=None, db_client=None):
        """
        容器大部分操作aiodocker已经封装,在此补充数据库操作部分.
        """
        if _id is None and container_info is None:
            raise TypeError("Missing necessary parameters id or container_info")

        if container_info is not None:
            _id = container_info.get("Id")
            net_work_settings = container_info.get("NetworkSettings")
            port = net_work_settings.get("Ports") if net_work_settings is not None else port
            node = container_info.get("Node")
            host_ip = node.get("IP") if node is not None else host_ip

        self._id = _id[:12]
        self._host_ip = host_ip
        self._create_time = int(time.time())
        self._destroy_time = self._create_time + Config.docker_default_life if destroy_time is None else destroy_time
        self._port = port
        self._db_client = DBClient if db_client is None else db_client

    def set_db_client(self, db_client) -> None:
        """
        设置数据库客户端取代默认客户端.
        """
        self._db_client = db_client

    def set_create_time(self, create_time: int):
        """
        从数据库初始化用,不要调用
        """
        self._create_time = create_time

    def get_dict(self) -> dict:
        """
        从内存中获得容器数据
        """
        record = dict()
        record['_id'] = self._id
        record['createTime'] = self._create_time
        record['destroyTime'] = self._destroy_time
        record['containerPort'] = self._port
        record['hostIP'] = self._host_ip

        return record

    async def get_dict_db(self) -> dict:
        """
        从数据库查询容器数据(感觉不太用得上)
        """
        return await self._db_client.container.find_one({'containerId': self._id})

    async def write(self) -> InsertOneResult:
        """
        把内存中的数据写入数据库
        """
        record = self.get_dict()
        return await self._db_client.container.insert_one(record)

    async def update(self) -> UpdateResult:
        """
        更新数据库
        """
        record = self.get_dict()
        id = record.get("_id")
        return await self._db_client.container.replace_one({'_id': id}, record)

    async def remove(self) -> dict:
        """
        删除记录
        """
        return await self._db_client.container.delete_many({'_id': self._id})

    async def is_valid(self) -> bool:
        """
        判断容器是否未过期
        未过期返回True
        过期返回False
        """
        if self._destroy_time <= int(time.time()):
            return False
        else:
            return True

    async def set_destroy_time(self, destroy_time) -> UpdateResult:
        """
        设置容器销毁时间
        """
        self._destroy_time = destroy_time
        return await self.update()


async def get_container(_id: str) -> Container:
    """
    查询数据库并返回一个Container对象
    """
    _id = _id[:12]
    record = await DBClient.container.find_one({'_id': _id})
    if record is None:
        raise Exception("No container was found")

    tmp = Container(
        _id=record.get('_id'),
        destroy_time=record.get('destroyTime'),
        port=record.get('containerPort'),
        host_ip=record.get('hostIP'),
    )
    tmp.set_create_time(create_time=record.get("createTime"))

    return tmp


def get_containers_info():
    """
    查询所有容器信息
    """
    return DBClient.container.find({})


if __name__ == "__main__":
    """
    test
    """
    from test.motor_test_data import test_data
    from tornado.ioloop import IOLoop
    from pymongo.results import UpdateResult

    tmp = Container(
        container_info=test_data
    )

    async def do_some():
        await tmp.write()
        await tmp.set_destroy_time(int(time.time())+20)


    loop = IOLoop.current()
    loop.run_sync(do_some)
