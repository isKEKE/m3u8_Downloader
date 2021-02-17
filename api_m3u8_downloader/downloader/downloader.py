# Python 3.8
# encoding:utf-8
# 异步存储
import asyncio
from Crypto.Cipher import AES
class AsyncioDownloader():
    def __init__(self,path):
        self.path = path

    async def writeByte(self,byte,key,mode):
        if mode == "ECB":
            cryptor = AES.new(key, AES.MODE_CBC,key)
            if self.file.write(cryptor.decrypt(byte)):
                return True

        elif mode == "CBC":
            # cryptor = AES.new(key, AES.MODE_CBC, vi)
            pass

        else:
            if self.file.write(byte):
                return True

    async def __aenter__(self):
        self.file = open(f"{self.path}","wb")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

async def downloader(path,byte,key,mode):
    # 分装成协程函数
    async with AsyncioDownloader(path) as f:
        return await f.writeByte(byte,key,mode)


if __name__ == '__main__':
    paht = "1.txt"
    byte = b"1"
    asyncio.run(downloader(paht,byte))