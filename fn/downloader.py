# Python 3.8
# encoding:utf-8
# 异步存储
import asyncio

class AsyncioDownloader():
    def __init__(self,path):
        self.path = path

    async def writeByte(self,byte):
        if self.file.write(byte):
            return True

    async def __aenter__(self):
        self.file = open(f"{self.path}","wb")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

async def downloader(path,byte):
    # 分装成协程函数
    async with AsyncioDownloader(path) as f:
        return await f.writeByte(byte)


if __name__ == '__main__':
    paht = "1.txt"
    byte = b"1"
    asyncio.run(downloader(paht,byte))