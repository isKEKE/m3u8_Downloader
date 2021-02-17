# Python 3.8
# encoding:utf-8
# Unencrypted Spider - 未加密m3u8记录爬虫
from .network_request.req import NetworkRequest
import re

class ClientGetsTsUrlDirectory(NetworkRequest):
    def __init__(self):
        NetworkRequest.__init__(self)
        self.new_url = None

    def callback(self,func,*args,**kwargs):
        return func(*args,**kwargs)

    def judgment_form_m3u8(self,url,old_url=None,old_html=None):
        '''请求m3u8_url返回响应体判断是否是m3u8链接...'''
        if url:
            try:
                if "\\" in url:
                    raise AssertionError
            except AssertionError:
                url = url.replace("\\",'')
            finally:
                self.set_url = url
                response = self.req_get
                self.html = response.text
                if "#EXTM3U" in self.html:
                    old_url, old_html = url, self.html
                    if "http" in self.html or "ts" in self.html:
                        print("isALE:获取ts链接目录成功...")

                        bool_aes = self.judgment_form_is_aes
                        if bool_aes:
                            print('isALE:是AES加密...','Not')
                            key_vi = [item for item in self.html.split('\n') if "EXT-X-KEY" in item][0]
                            if "vi" in key_vi:
                                self.decrypt_aes_cbc(self.html)
                            else:
                                return self.decrypt_aes_ecb(url,self.html,key_vi)
                        else:
                            print('isALE:文件未加密...')
                            result = self.get_ts_url_list(url,self.html)
                            return result

                    elif "m3u8" in self.html:
                        print("isALE:获取ts链接目录失败，需二次请求...")
                        self.second_url = self.get_new_url(url)
                        # 回调
                        return self.callback(self.judgment_form_m3u8,self.second_url,old_url,old_html)

                    else:
                        print("isALE:获取ts链接目录失败(无m3u8关键字)，需二次请求...")
                        self.second_url = self.get_new_url(url)
                        return self.callback(self.judgment_form_m3u8, self.second_url, old_url, old_html)

                elif "m3u8" in self.second_url:
                    print("isALE:获取ts链接目录失败，需重构URL...")
                    # 回调 三次
                    third_url = self.callback(self.get_new_url,old_url,old_html,True)
                    return self.callback(self.judgment_form_m3u8,third_url)

                else:
                    print("isALE:获取ts链接目录失败(无m3u8关键字)...")
                    # 回调 三次
                    third_url = self.callback(self.get_new_url, old_url, old_html, True)
                    return self.callback(self.judgment_form_m3u8, third_url)
        else:
            print("isALE:请先输入m3u8...")
            return None

    def url_join(self,url,item,bool):
        ''' 二级URL组合功能内 '''
        try:
            if bool == True:
                raise AssertionError
        except AssertionError:
            done = re.match("(http|https)://(.*?)/", url).group(0)
            new_url = f"{done}{item}"
            return new_url
        else:
            new_url = '{}{}'.format(re.search("http(.*)/", url).group(0), item)
            return new_url

    def get_new_url(self,url,html=None,bool=False):
        ''' 二级URL组合功能外 '''
        if bool == True:
            self.html = html
        html_list = [item for item in self.html.split("\n") if item != ""]
        for item in html_list[1:]:
            if "m3u8" in item:
                return self.callback(self.url_join,url,item,bool)
        return self.callback(self.url_join,url,html_list[-1],bool)

    @property
    def judgment_form_is_aes(self):
        ''' 判断是否加密 '''
        if "#EXT-X-KEY" in self.html:
            return True
        else:
            return False

    def decrypt_aes_ecb(self,url,html,kev_vi):
        ''' 获取AES解密KEY并返回 '''
        print('isALE:AES加密,ECB模式...')
        method,key_url_str = kev_vi.split(',')
        key_url = re.search('URI="(.*)"',key_url_str).group(1)
        self.set_url = key_url
        key = self.req_get.text.encode('utf-8')
        result = self.get_ts_url_list(url,html,key,"ECB")
        return result


    def decrypt_aes_cbc(self,html):
        print('isALE:AES加密,CBC模式...')
        return None
            # print(item)

    def get_ts_url_list(self,url,html,key=None,mode=None):
        '''
        获取TS链接目录所有链接
        :return: ts_url_list:list
        '''
        ts_list = []

        for item in html.split('\n'):
            try:
                if "\r" in item:
                    raise AssertionError
            except AssertionError:
                item = item.replace('\r','')

            finally:
                if "http" in item and "EXT-X-KEY" not in item:
                    ts_list.append(item)

                elif "ts" in item and not "http" in item:
                    ts_url = f'{re.search("http(.*)/",url).group(0)}{item}'
                    ts_list.append(ts_url)

                elif "ts" in item and "http" in item:
                    ts_list.append(item)

        return (ts_list,len(ts_list),key,mode)


if __name__ == '__main__':
    # 可直接获得
    url1 = "https://wy.bigmao.top/api/GetDownUrlMu/3bb24322f78b47dfb8723c13d46d45ee/7fe5e63ce5844423ac0a8ec97c96d15d.m3u8"
    # 不可直接获得,并且带有斜杠
    url2 = "https:\/\/jingdian.qincai-zuida.com\/20200911\/11082_be11fca7\/index.m3u8"
    # AES加密,ECB模式
    url3 = "https://video.hcyunshang.cn/20210215/cEkErZnB/index.m3u8"
    # 不可直接获得，但也没有m3u8关键字
    url4 = "https://www.kkarm.com:65/20190907/7TbuJfha/index.m3u8"

    client_ts = ClientGetsTsUrlDirectory()
    result = client_ts.judgment_form_m3u8(url4)
    print(len(result))
