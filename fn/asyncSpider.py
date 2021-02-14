# Python 3.8
# encoding:utf-8
# 异步爬虫，下载请求TS超链接
import asyncio
import aiohttp

async def requestAsync(url):
    '''
    简单的异步请求
    :param url: ts超链接
    :return: 二进制ts文件
    '''
    async with aiohttp.ClientSession() as session:
        timeout = aiohttp.ClientTimeout(total=10)
        async with session.get(url,timeout=timeout) as response:
            return await response.read()
asyncio.Event()