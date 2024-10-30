# Use this outside of the container, making REST calls to the running seldon container
import asyncio
import httpx
from queries import queries
import time

IN_FLIGHT=4
URL = 'http://127.0.0.1:9999/api/v1.0/predictions'


async def get_embedding(client, test):
    params = {
        "data": {
            "ndarray": [test]
            }
        }
    response = await client.post(url=URL, json=params)
    if response.status_code == 200:
        print('.',end='', flush=True)
        return '.'
    else:
        print('X',end='', flush=True)
        return 'x'


  

async def bound_fetch(sem, client,test):
    async with sem:
        return await get_embedding(client, test)


async def main():
    sem = asyncio.Semaphore(IN_FLIGHT)
    limits = httpx.Limits(max_keepalive_connections=IN_FLIGHT, max_connections=IN_FLIGHT, keepalive_expiry=10)
    client = httpx.AsyncClient(limits=limits, verify=False)
    start_time = time.perf_counter()
    await asyncio.gather(*[asyncio.ensure_future(bound_fetch(sem,client,test)) for test in queries], return_exceptions=True)
    end_time = time.perf_counter()
    print(f"{len(queries)} embeddings done in {round(end_time-start_time,2)} seconds.")


if __name__=='__main__':
    asyncio.run(main())
