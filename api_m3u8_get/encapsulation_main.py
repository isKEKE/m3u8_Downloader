from officials.pseudo_omnipotent_main import GetU3m8UrlOfficial
import shelve
import os

def Exeist_Create_Shelve_Dir(cls):
    UESR_SHELVE_OOP_PATH = os.path.abspath(".\\cfg")
    if not os.path.exists(UESR_SHELVE_OOP_PATH):
        os.mkdir(UESR_SHELVE_OOP_PATH)
    return cls

@Exeist_Create_Shelve_Dir
class EncapsulationShelveOOP():
    '''
    注:自定义接口返回值：M3u8超链接:str
    '''
    def __init__(self):
        self.path = os.path.abspath(".\\cfg")
        pass
    def Create_Shelve_OOP(self):
        with shelve.open(f"{self.path}\\user_shelve_file") as db:
            db["officials"] = GetU3m8UrlOfficial
    @property
    def Read_Shelve_OOP(self):
        obj_dict = {}
        with shelve.open(f"{self.path}\\user_shelve_file") as db:
            for key in db:
                obj_dict[key] = db[key]
        return obj_dict

    def Update_Shelve_OOP(self,**kwargs):
        '''key=host,value=类对象'''
        with shelve.open(f"{self.path}\\user_shelve_file") as db:
            for key,value in kwargs.items():
                if not key in db.keys():
                    db[key] = value
                else:
                    print("isALE:此域名关键字已存在...")

if __name__ == '__main__':
    eso = EncapsulationShelveOOP()
    # 创建
    eso.Create_Shelve_OOP()
    # 读取
    # obj_dict = eso.Read_Shelve_OOP
    # url = "https://www.nfmovies.com/video/14712-2-2.html"
    # obj_dict["officials"].run(url)
    # 更新
    # obj_dict = {
    #     "www.bilibili.com":GetU3m8UrlOfficial,
    #     "www.baidu.com":GetU3m8UrlOfficial
    # }
    # eso.Update_Shelve_OOP(UESR_SHELVE_OOP_PATH,**obj_dict)