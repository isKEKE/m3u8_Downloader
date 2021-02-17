from sys import path
path.append(".\\api_m3u8_downloader")
path.append(".\\api_m3u8_get")
path.append(".\\api_m3u8_get\\customizesw")
from encapsulation_main import EncapsulationShelveOOP
from util.utils import m3u8_download_main
from re import search

'''
    自定义搜集m3u8接口方式：
        导入你写的模块(建议保存到.\\api_m3u8_get\\customizesw 文件夹中);
        @exists_shelve_OOP(**dict),传入参数是个字典，格式:
            key:爬虫URL的服务器域名
            value:你的类对象，无需实例化...
        PS：你的代码只需作为参数填写一次并运行完成即可，第二次运行可删除参数...
        
    并发数量修改:.\\util\\utils.py文件中修改，`@set_ts_url(count=16)`,93行,默认16.
'''

def exists_shelve_OOP(**kwargs_1):
    # 对象持久化模块
    eso = EncapsulationShelveOOP()
    # 读取返回值字典
    obj_dict = eso.Read_Shelve_OOP
    # key组合列表
    obj_key_list = [key for key in obj_dict.keys()]
    # 判断key是否存在
    element_bool_list = [1 if key in obj_key_list else 0 for key in kwargs_1.keys()]
    bool_sum = sum(element_bool_list)
    def outter(func):
        def wapper(*args,**kwargs_2):
            try:
                if kwargs_1 and bool_sum == 0:
                    raise AssertionError
            except AssertionError:
                eso.Update.Shelve_OOP(**kwargs_1)
            else:
                if bool_sum > 0:
                    print("isALE:Host已存在...")
            finally:
                return func(*args,**kwargs_2)

        return wapper
    return outter

@exists_shelve_OOP()
def main_program(url,m3u8_mode=False):
    '''
    :param url: 下载链接
    :param m3u8_mode: 若下载链接是*.m3u8文件，填写位True.
    :return: None
    '''
    if not m3u8_mode:
        host = search("(http|https)://(.*?)/",url).group(2)
        obj_dict = EncapsulationShelveOOP().Read_Shelve_OOP
        try:
            if host in obj_dict.keys():
                raise AssertionError
        except AssertionError:
            pass
        else:
            obj = obj_dict["officials"]
            m3u8_url = obj.run(url)
            if m3u8_url:
                # 异步下载
                m3u8_download_main(m3u8_url)
            else:
                print("isALE:官方模块搜集M3u8超链接失败,请定制...")
    else:
        m3u8_download_main(url)


if __name__ == '__main__':

    # 视频页面
    url = "https://www.nfmovies.com/video/14712-2-2.html"
    # 视频页面，注意：此链接源代码不可直接获得m3u8,官方模块失效
    url2 = "https://www.yst3.com/xijupian/49669/play-2-1.html"
    # 可直接获得,m3u8链接
    m3u8_url1 = "https://wy.bigmao.top/api/GetDownUrlMu/3bb24322f78b47dfb8723c13d46d45ee/7fe5e63ce5844423ac0a8ec97c96d15d.m3u8"
    # 不可直接获得,并且带有斜杠,m3u8链接
    m3u8_url2 = "https:\/\/jingdian.qincai-zuida.com\/20200911\/11082_be11fca7\/index.m3u8"
    # AES加密,ECB模式,m3u8链接
    m3u8_url3 = "https://video.hcyunshang.cn/20210215/cEkErZnB/index.m3u8"
    # 不可直接获得，但也没有m3u8关键字,m3u8链接
    m3u8_url4 = "https://www.kkarm.com:65/20190907/7TbuJfha/index.m3u8"

    #
    result = main_program(url2)
