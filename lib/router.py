from logging import logging
import asyncio
from primitives.queue import Queue

log = logging.getLogger(__name__)

class Router:
    
    def __init__(self):
        log.debug('Router created')
        self.queue = Queue
        log.debug(isinstance(self.queue, Queue))
        self.task = asyncio.create_task(self.run())
        
    async def run(self):
        log.debug('Router.run started.')
        while True:
            self.get()
        
    async def put(self, value):
        print("Running Router.put()")
        print(value)
        print(self.queue.qsize())
        await self.queue.put(value)
        print(self.queue.qsize())
        
    async def get(self):
        print("Running Router.get()")
        self.result = await self.queue.get()  # Blocks until data is ready
        print('Result was {}'.format(self.result))
        self.queue.task_done()