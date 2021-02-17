# Python 3.8
# encoding=utf-8
# 合并*.ts文件为mp4
from operation_dir.operation_dir import DOWNLOAD_MP4_PATH,DOWNLOAD_TS_PATH
import os

def mergeTs(title):
    with open(f"{DOWNLOAD_MP4_PATH}\\{title}.mp4",'wb+') as f:
        ts_list = os.listdir(DOWNLOAD_TS_PATH)
        for item in range(len(ts_list)):
            if f"{item}.ts" in ts_list:
                file = f"{DOWNLOAD_TS_PATH}\\{item}.ts"
                f.write(
                    open(file,'rb').read()
                )
                os.remove(file)
            else:
                print(f"{item}.ts不存在")

if __name__ == '__main__':
    mergeTs("1")