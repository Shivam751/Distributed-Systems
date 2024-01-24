import requests
import aiohttp
import asyncio
import re
import matplotlib.pyplot as plt

def extract_serv_id(input_string):
    match = re.search(r"Hello from Server: (\S+)", input_string)
    if match:
        return match.group(1)  # This is the server ID
    else:
        return None
def add(n = 1, hostnames = ["s1"]):
    r = requests.post('http://localhost:5000/add', json={"n": n, "hostnames": hostnames})
    print(r.json())

def rm(n = 1, hostnames = ["s1"]):
    r = requests.delete('http://localhost:5000/rm', json={"n": n, "hostnames": hostnames})
    print(r.json())

async def request(session, url):
    # Example of an async GET request
    async with session.get(url) as response:
        return await response.json()

async def main():
    url = 'http://localhost:5000/home'
    responses = None
    dic = {}

if __name__ == '__main__':
    asyncio.run(main())
