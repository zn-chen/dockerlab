# -*- coding: utf-8 -*-
"""
计划任务
"""
from .container_scheduled import CONTAINER_TASK_LIST


def start():
    """
    开始周期任务
    """
    for i in CONTAINER_TASK_LIST:
        i.start()