from os.path import abspath,dirname,join
from os.path import exists as es
from os import mkdir
# 获取路径模块
ROOT_PATH = dirname(
    dirname(
        dirname(abspath(__file__))
    )) # 根路径
DOWNLOAD_PATH = join(ROOT_PATH,"download")
DOWNLOAD_TS_PATH = join(DOWNLOAD_PATH,"ts")
DOWNLOAD_MP4_PATH = join(DOWNLOAD_PATH,"mp4")

class Path:
    @staticmethod
    def exists():
        # 判断文件夹是否存在
        try:
            if not es(DOWNLOAD_PATH):
                mkdir(DOWNLOAD_PATH)

            if not es(DOWNLOAD_TS_PATH):
                mkdir(DOWNLOAD_TS_PATH)

            if not es(DOWNLOAD_MP4_PATH):
                mkdir(DOWNLOAD_MP4_PATH)
        except:
            return False
        else:
            return True

if __name__ == '__main__':
    print(DOWNLOAD_PATH)
    Path.exists()
