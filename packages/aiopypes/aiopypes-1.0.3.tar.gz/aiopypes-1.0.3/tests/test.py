import aiopypes

import asyncio

import time

from aiopypes.balance import CongestionLoadBalancer, RoundRobinLoadBalancer


app = aiopypes.App()

@app.task(interval=1.0)
async def trigger():
    return 1.0


# @app.task(balancer=RoundRobinLoadBalancer())
# async def route_a(input: aiopypes.Stream):
#     async for sleep in input:
#         await asyncio.sleep(sleep)
#         yield 'A'

# @app.task(scale=10)
# async def route_b(input: aiopypes.Stream):
#     async for sleep in input:
#         await asyncio.sleep(sleep)
#         yield 'B'

# @app.task(scale=1)
# async def task1(input: aiopypes.Stream):
#     async for router, sleep in input:
#         await asyncio.sleep(5 * sleep)
#         yield router, 1, input.queue.qsize()

# @app.task(scale=50)
# async def task2(input: aiopypes.Stream):
#     async for router, sleep in input:
#         await asyncio.sleep(5 * sleep)
#         yield router, 2, input.queue.qsize()

@app.task()
async def classify(input: aiopypes.Stream):
    async for _ in input:
        yield 'A', 'message from A'
        # yield 'B', 'message from B'

@app.task()
async def receive_a(input: aiopypes.Stream):
    async for obj in input:
        print(f"A: received {obj}")
        yield

@app.task()
async def receive_b(input: aiopypes.Stream):
    async for obj in input:
        print(f"B: received {obj}")
        yield

if __name__ == '__main__':

    pipeline = trigger \
               .map(classify) \
               .map(receive_a, receive_b, routes=['A', 'B'])

    pipeline.run()