import asyncio
from primitives.queue import Queue

class Consume:
    
    def __init__(self):
        print('Creating Comsumer')
        self.queue = Queue()
        self.result = 0
        self.task = asyncio.create_task(self.run())
        
    async def put(self, value):
        print("Running consume.put()")
        print(value)
        print(self.queue.qsize())
        await self.queue.put(value)
        print(self.queue.qsize())
        
    async def get(self):
        print("Running consume.get()")
        self.result = await self.queue.get()  # Blocks until data is ready
        print('Result was {}'.format(self.result))
        self.queue.task_done()
    
    async def run(self):
        print('Consume.run started...')
        await self.get()
        
class Produce():
    
    def __init__(self, consumer):
        print('Creating Producer')
        self.consumer = consumer
        self.result = 0
        self.task = asyncio.create_task(self.run())
        
    async def run(self):
        print('Produce.run started...')
        await self.put()
        
    async def put(self):
        await asyncio.sleep(2)
        print('Waiting for slow process.')
        self.result = 42
        print('Putting result onto queue')
        await self.consumer.put(self.result)  # Put result on queue

async def slow_process():
    await asyncio.sleep(2)
    return 42

async def produce(queue):
    print('Waiting for slow process.')
    result = await slow_process()
    print('Putting result onto queue')
    await queue.put(result)  # Put result on queue

async def consume(queue):
    print("Running consume()")
    result = await queue.get()  # Blocks until data is ready
    print('Result was {}'.format(result))

async def queue_go(delay):
    #queue = Queue()
    #t1 = asyncio.create_task(consume(queue))
    #t2 = asyncio.create_task(produce(queue))
    consumer = Consume()
    producer = Produce(consumer)
    await asyncio.sleep(delay)
    print("Done")

asyncio.run(queue_go(10))