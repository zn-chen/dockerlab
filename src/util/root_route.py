# -*- coding: utf-8 -*-
import os
import sys


def get_root_route():
    py_dir = os.path.dirname(__file__)
    exec_dir = os.path.dirname(sys.executable)
    now_dir = os.getcwd()

    if os.path.isfile(os.path.join(py_dir, '..', 'config.ini')):
        return os.path.join(py_dir, '..')
    elif os.path.isfile(os.path.join(exec_dir, 'config.ini')):
        return exec_dir
    elif os.path.isfile(os.path.join(now_dir, 'config.ini')):
        return now_dir
    else:
        return None
