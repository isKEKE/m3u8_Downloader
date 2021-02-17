# Pyhon 3.8
# encoding:utf-8
# 异步计数器
from copy import deepcopy

class Counter():
    def __init__(self,count):
        self.count = count
        self.all = deepcopy(count)

    async def readline(self):
        self.count -= 1
        if self.count == 0:
            return None
        proportion = f"{100 - (self.count / self.all * 100):.2f}"
        all_count = f"{self.all - self.count}/{self.all}"
        return (proportion,all_count)

    def __aiter__(self):
        return self

    async def __anext__(self):
        val = await self.readline()
        if val == None:
            raise StopAsyncIteration
        return val

async def counter(obj):
    async for i in obj:
        return i

if __name__ == '__main__':
    count = 100
    counter = Counter(count)











