import requests
from re import search
class GetU3m8UrlOfficial:
    def __init__(self):
        pass
    @staticmethod
    def run(url):
        try:
            html = requests.get(url=url).text
            m3u8_url = search("http(.*?)m3u8",html).group(0)
        except AttributeError:
            return None
        else:
            return m3u8_url

if __name__ == '__main__':
    url = "https://www.nfmovies.com/video/14712-2-2.html"
    m3u8 = GetU3m8UrlOfficial.run(url)
