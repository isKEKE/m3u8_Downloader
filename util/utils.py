
from m3u8_spider.client_gets_ts_url_dir import ClientGetsTsUrlDirectory
from async_spider.async_spider import requestAsync
from operation_dir.operation_dir import DOWNLOAD_TS_PATH,DOWNLOAD_MP4_PATH,Path
from downloader.downloader import downloader
from counter.counter import Counter,counter
from merge.merge import mergeTs
import asyncio
import time

async def worker(queue,COUNTER_CLASS):
    while True:
        index,url,key,mode = await queue.get()
        # print(f"开始任务:{name}")

        try:
           content = await requestAsync(url)
        except Exception as exc:
            # 异常，元素重新加入队列中
            print('异常',time.time())
            await asyncio.sleep(0.3) # 休息一下...
            queue.put_nowait((index,url))
        else:
            path = f"{DOWNLOAD_TS_PATH}\\{index}.ts"
            done = await downloader(path, content,key,mode)
            if done:
                # 判断是否下载成功，输出完成度
                per,count = await counter(COUNTER_CLASS)
                if per != None:
                    print(f"完成度:{per}%,已下载数量:{count}个")
                else:
                    print('下载完成:100%')
        finally:
            queue.task_done()
            # print(f"结束任务:{name}")

async def worker_close(tasks):
    try:
        for index,task in enumerate(tasks):
            task.cancel()
            # print(index, task) # 调试
    except RuntimeError:
        pass

async def asyncLoop(*args):
    print("开始下载...")
    t1 = time.time()
    count,tsList,length,key,mode = args
    # 队列集实例化
    queue = asyncio.Queue()

    # 元素添加队列
    for index, u in enumerate(tsList):
        queue.put_nowait((index, u,key,mode))

    # 添加事务至循环
    COUNTER_CLASS = Counter(length)
    tasks = []
    for i in range(count):
        task = asyncio.create_task(worker(queue,COUNTER_CLASS))
        tasks.append(task)

    # 阻塞至队列中所有的元素都被接收和处理完毕。
    await queue.join()

    # 关闭事务
    await worker_close(tasks)
    # 合并TS文件
    mergeTs(f"{time.time():.0f}")
    print(f"用时:{time.time() - t1}秒")

def create_download_dir(func):
    ''' 此装饰器功能：判断存储文件夹是否存在并创建 '''
    def wapper(*args,**kwargs):
        if Path.exists():
            func(*args,**kwargs)
        else:
            print("isALE:创建存储文件夹失败...")
    return wapper

def set_ts_url(count=16):
    def outter(func):
        def wapper(*args,**kwargs):
            done = func(*args,**kwargs)
            if done:
                tsList, length, key, mode = done
                loop = asyncio.get_event_loop()
                loop.run_until_complete(asyncLoop(*(count, tsList, length, key, mode)))
        return wapper
    return outter

@create_download_dir
@set_ts_url(count=16) # count-并发数量
def m3u8_download_main(url):
    client_ts = ClientGetsTsUrlDirectory()
    result = client_ts.judgment_form_m3u8(url)
    return result

if __name__ == '__main__':
    # 可直接获得
    url1 = "https://wy.bigmao.top/api/GetDownUrlMu/3bb24322f78b47dfb8723c13d46d45ee/7fe5e63ce5844423ac0a8ec97c96d15d.m3u8"
    # 不可直接获得,并且带有斜杠
    url2 = "https:\/\/jingdian.qincai-zuida.com\/20200911\/11082_be11fca7\/index.m3u8"
    # AES加密,ECB模式
    url3 = "https://video.hcyunshang.cn/20210215/cEkErZnB/index.m3u8"
    # 不可直接获得，但也没有m3u8关键字
    url4 = "https://www.kkarm.com:65/20190907/7TbuJfha/index.m3u8"

    m3u8_download_main(url1)


