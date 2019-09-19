# -*- coding: utf-8 -*-
"""
序列化函数
"""


def container_brief_info_serialize(container_data: dict) -> dict:
    """
    对容器的简单信息进行序列化
    """
    infos = dict()
    container_id = container_data.get("Id")
    node = container_data.get("Node")
    net_work_settings = container_data.get("NetworkSettings")
    state = container_data.get("State")

    infos["containerId"] = str(container_id)[:12] if container_id is not None else None
    infos["hostIP"] = node.get("IP") if node is not None else None
    infos["username"] = None
    infos["password"] = None
    infos["containerPort"] = net_work_settings.get("Ports") if net_work_settings is not None else None
    infos["destroyTime"] = None
    infos["contianerState"] = state.get("Status") if state is not None else None

    return infos
