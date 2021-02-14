# Pyhon 3.8
# encoding:utf-8
# 获取m3u8中*.ts超链接
import requests
import re
import pickle
import random
from time import sleep
from setting import CONFIG_PATH
import sys

class RequestHeaders():
    ''' 设置请求头类 '''
    def __init__(self):
        self.__headers = {}

    @property  # 只读
    def userAgent(self):
        # 类的方法属性化
        with open(f'{CONFIG_PATH}\\user_agent.pkl', 'rb') as f:
            self.__user_agent = pickle.load(f)
        return random.choice(self.__user_agent)

    @property
    def headers(self):
        # 设置请求头
        self.__headers['User-Agent'] = self.userAgent
        return self.__headers

    @headers.setter
    def headers(self, *args):
        # 实例化可更新 headers 参数
        # args：传递参数为字典
        for item in args:
            for key, value in dict(item).items():
                self.__headers[key] = value

class Movie(RequestHeaders):
    def __init__(self):
        # 继承
        RequestHeaders.__init__(self)
        self.__url = ''
        self.length = 0

    @property
    def setUrl(self):
        return self.__url

    @setUrl.setter
    def setUrl(self,value):
        self.__url = value

    @property
    def uGet(self):
        '''
        Get请求，有5秒超时判断
        :return:response
        '''
        response = requests.get(url=self.__url,headers=self.headers,timeout=(5,30))
        return response

    def m3u8(self):
        '''
        获取*.m3u8超链接
        :return: 网址[字符串]
        '''
        if self.setUrl:
            count = 0
            while True:
                try:
                    # 通过访问视频播放界面获取m3u8链接
                    response = self.uGet
                    html = response.text
                    getM3u8Url = re.search("http(.*?)m3u8",html,re.U).group()
                    if "\\" in getM3u8Url:
                        getM3u8Url = getM3u8Url.replace("\\",'')
                    # 设置获取的第一次m3u8链接，并访问获取最终m3u8链接
                    self.setUrl = getM3u8Url
                    response = self.uGet
                    html = response.text
                    m3u8_url = html.split('\n')[-1]
                except requests.exceptions.ConnectTimeout:
                    count += 1
                except requests.exceptions.ReadTimeout:
                    count += 1
                except requests.exceptions.ConnectionError:
                    count += 1
                    print("KEKE:请求频繁,休息3秒...")
                    sleep(3)
                except AttributeError:
                    count += 1
                else:
                    # 清除URL属性
                    self.setUrl = ''
                    if not self.setUrl:
                        # 返回最终m3u8链接
                        _m3u8_url = f"{getM3u8Url.replace('index.m3u8',m3u8_url)}"
                        return _m3u8_url
                finally:
                    if count == 20:
                        print("爬虫异常20次，退出程序...")
                        sys.exit()

        else:
            print("请输入视频网页链接...")
            return None

    def tsDoc(self):
        '''
        获取视频*.ts目录
        :return:*.ts目录[列表]
        '''
        tsList = []
        if self.setUrl:
            response = self.uGet
            html = response.text
            htmlList = html.split('\n')

            for item in htmlList:
                if "ts" in item:
                    tsList.append(re.search("(.*)/",self.setUrl).group() + item)
            # print(tsList) # 测试
            # 所有*.ts文件总个数
            self.length = len(tsList)

            self.setUrl = ''
            return tsList
        else:
            print("获取.*/index.m3u8链接失败...",112)
            return None

mv = Movie()
def makeM3u8(url):
    '''
    分装m3u8爬虫
    :return: *.ts超链接目录[列表]
    '''
    mv.setUrl = url
    mv.setUrl = mv.m3u8()
    tsList = mv.tsDoc()
    return (tsList,mv.length)

if __name__ == "__main__":
    url = "https://www.nfmovies.com/video/62082-1-0.html"
    tsList = makeM3u8(url)
    print(tsList)
