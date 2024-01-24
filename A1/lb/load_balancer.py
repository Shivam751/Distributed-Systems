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
    
async def periodic_server_monitor(interval = 1):
    while True:
        dead_servers = []
        tasks = [check_heartbeat(server_name) for server_name in server_hostname_to_id.keys()]
        results = await asyncio.gather(*tasks)
        results = zip(server_hostname_to_id.keys(), results)
        for server_name, result in results:
            if result == False:
                server_id = server_hostname_to_id[server_name]
                ch.remove_server(server_id)
                dead_servers.append(server_name)
        
        for server_name in dead_servers:
            server_id = server_hostname_to_id[server_name]

            try:
                res = client.containers.run(image=image, name=server_name, network=network, detach=True, environment={'SERV_ID': server_id})
            except Exception as e:
                print(e)

            ch.add_server(server_id)
        
        await asyncio.sleep(interval)