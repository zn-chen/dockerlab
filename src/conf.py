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
        self.log_to_stderr = log.getboolean("to_stderr")
        self.log_to_file = log.getboolean("to_file")

        self.log_rotate_mode = log.get("rotate_mode")
        self.log_rotate_when = log.get("rotate_when")
        self.log_rotate_interval = log.getint("rotate_interval")
        self.log_file_max_size = log.getint("file_max_size")
        self.log_file_path = log.get("file_path")
        self.log_file_num_backups = log.getint("file_num_backups")

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
