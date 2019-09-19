# -*- coding: utf-8 -*-
"""
Tornado 路由文件
"""
from controller import container_controller

ROUTER = [
    (r'^/container/(?P<container_id>[0-9a-z]{12}$)?', container_controller.Container),
    (r'^/containers', container_controller.Containers),
]
