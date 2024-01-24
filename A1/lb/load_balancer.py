from consistent_hashing import ConsistentHashMap
from quart import Quart, jsonify, Response
import asyncio
import aiohttp
import docker
import random
import os

network = "n1"
image = "serv"
app = Quart(__name__)
ch = None
client = docker.from_env()
server_id_to_hostname = {}
server_hostname_to_id = {}