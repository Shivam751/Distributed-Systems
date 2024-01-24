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

async def check_heartbeat(server_name = None):
    url = f'http://{server_name}:5000/heartbeat'
    try:
        async with aiohttp.ClientSession() as client_session:
            async with client_session.get(url) as response:
                if response.status == 200:
                    return True
                else:
                    return False
    except Exception as e:
        return False