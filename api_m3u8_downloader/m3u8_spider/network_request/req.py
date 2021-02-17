# Python 3.8
# encoding:utf-8
# 请求Headers的设置和requests.Get请求的分装
import requests
from random import choice
import sys

USER_AGENT = [
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
        "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
        "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "NOKIA5700/ UCWEB7.0.2.37/28/999",
        "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)"
    ]

class RequestHeaders():
    ''' 设置请求头类 '''

    def __init__(self):
        self.__headers = {}

    @property  # 只读
    def user_agent(self):
        # 类的方法属性化
        user_agent = choice(USER_AGENT)
        return user_agent

    @property
    def headers(self):
        # 设置请求头
        self.__headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        self.__headers["Accept-Encoding"] = "gzip, deflate" # 注:requests不支持br解压
        self.__headers["Accept-Language"] = "Accept-Language: zh-CN,zh;q=0.9"
        self.__headers["Cache-Control"] = "no-store" # 本地不保存缓存，每次请求服务器都需发送资源.
        self.__headers["Connection"] = "close" # 关闭长连接
        self.__headers['User-Agent'] = self.user_agent
        return self.__headers

    @headers.setter
    def headers(self, *args):
        # 实例化可更新 headers 参数
        # args：传递参数为字典
        for item in args:
            for key, value in dict(item).items():
                self.__headers[key] = value

class NetworkRequest(RequestHeaders):
    def __init__(self):
        # 继承
        RequestHeaders.__init__(self)
        self.__url = ''
        self.__host_mode = False
        self.length = 0

    @property
    def set_url(self):
        return self.__url

    @set_url.setter
    def set_url(self,value):
        # 设置url
        self.__url = value

    @property
    def req_get(self):
        '''
        Get请求，有5秒超时判断
        :return:response
        '''
        count = 0
        while True:
            try:
                response = requests.get(url=self.__url,headers=self.headers,timeout=(5,30))
            except requests.exceptions.ConnectTimeout:
                count += 1
            except requests.exceptions.ReadTimeout:
                count += 1
            except requests.exceptions.ConnectionError:
                count += 1
            else:
                count = 0
                self.set_url = None
                return response
            finally:
                if count == 10:
                    sys.exit()



if __name__ == '__main__':
    nr = NetworkRequest()
    nr.set_url = "http://www.baidu.com/index?t=100"
    print(nr.headers["Host"]) # 报错
