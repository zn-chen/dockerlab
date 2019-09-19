# -*- coding: utf-8 -*-
"""
配置文件读取
"""
import configparser
import os

from util.root_route import get_root_route


class _Config(object):
    def __init__(self):
        project_root = get_root_route()
        config = configparser.ConfigParser()
        config.read(os.path.join(project_root, "config.ini"))

        # Base
        base = config["Base"]
        self.base_port = base.getint("Port")

        # Logger
        log = config["Log"]
        self.log_level = log.get("level")

        # MongoDB
        mongdb = config["MongoDB"]
        self.mongdb_IP = mongdb.get("IP")
        self.mongdb_port = mongdb.getint("port")

        # DockerRemote
        docker_remote = config["DockerRemote"]
        self.docker_remote_ip = docker_remote.get("ip")
        self.docker_remote_port = docker_remote.get("port")

        # DockerSettings
        docker_settings = config["DockerSettings"]
        self.docker_default_life = docker_settings.getint("default_life")


Config = _Config()
