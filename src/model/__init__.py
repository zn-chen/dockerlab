# -*- coding: utf-8 -*-
"""
模型
"""
import aiodocker
from motor import motor_tornado

from conf import Config

docker_remote_url = "http://{0}:{1}".format(Config.docker_remote_ip, Config.docker_remote_port)

DockerClient = aiodocker.Docker(docker_remote_url)

MongoClient = motor_tornado.MotorClient(Config.mongdb_IP, Config.mongdb_port)

DBClient = MongoClient.DockerLab
