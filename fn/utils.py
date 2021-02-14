# Python 3.8
# encoding:utf-8
# 主进程
import asyncio
from asyncSpider import requestAsync
from downloader import downloader
from setting import DOWNLOAD_PATH
from m3u8Spider import makeM3u8
from counter import counter,Counter
from merge import mergeTs
import time

async def worker(queue,COUNTER_CLASS):
    while True:
        index,url = await queue.get()
        # print(f"开始任务:{name}")

        try:
           content = await requestAsync(url)
        except Exception as exc:
            # 异常，元素重新加入队列中
            queue.put_nowait((index,url))
        else:
            path = f"{DOWNLOAD_PATH}\\{index}.ts"
            done = await downloader(path, content)
            if done:
                # 判断是否下载成功，输出完成度
                count = await counter(COUNTER_CLASS)
                if count != None:
                    print(f"下载完成:{100 - count}%")
                else:
                    print('下载完成...')
        finally:
            queue.task_done()
            # print(f"结束任务:{name}")

async def main(url=None,count=128):
    t1 = time.time()
    if url:
        tsList,length = makeM3u8(url)
        if tsList:
            # 队列集实例化
            queue = asyncio.Queue()

            # 元素添加队列
            for index, u in enumerate(tsList):
                queue.put_nowait((index, u))

            # 添加事务至循环
            COUNTER_CLASS = Counter(length)
            tasks = []
            for i in range(count):
                task = asyncio.create_task(worker(queue,COUNTER_CLASS))
                tasks.append(task)

            # 阻塞至队列中所有的元素都被接收和处理完毕。
            await queue.join()
            print(f"用时:{time.time() - t1}秒")

            # 关闭事务
            for task in tasks:
                task.cancel()

            # 合并TS文件
            mergeTs(f"{time.time():.0f}")

        else:
            print("KeKe:获取ts文件超链接失败...")
    else:
        print("KeKe:请先输入要下载视频的链接...")

if __name__ == '__main__':
    url = "https://www.nfmovies.com/video/62082-1-0.html"
    asyncio.run(main(url=url))
