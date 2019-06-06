
from bs4 import BeautifulSoup 
import requests
import re
import os


class Download_Novel():
        def __init__(self, url):
                self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'
                }
                self.url = url
        
        def get_html(self):   #获取网页html代码
                response = requests.get(self.url,  headers=self.headers)  
                self.html = response.content.decode('gbk')                
                return self.html


        def get_next_url(self):  #获取下一章网址
                html = self.html
                p = re.compile(r'href="(/\w+/\d+/\d+[.]html)">下一章')
                r = p.findall(html)[0]

                self.url = 'https://www.biqiuge.com' + r

        def get_text(self):   #获取网页内容
                html = self.get_html()
                soup = BeautifulSoup(html, 'html.parser')

                text = soup.get_text()
                p = re.compile(r'read2\(\);(.*)https', re.DOTALL)
                text = p.findall(text)[0]
                if '\xa0' in text:
                        text = re.sub('\xa0'*8, '\n\n', text)
                        self.text = re.sub('\xa0', ' ', text)
                else:
                        self.text = re.sub('\u3000', '\n', text)
                
                title = str(soup.title)
                self.title = re.findall('<title>(.*?)_', title)[0]

        def save_novel(self):    #保存
                with open(self.title+'.txt', 'w') as f:                        
                        f.write(self.title + '\n' + self.text)

        def run(self, folder, num):
                os.mkdir(folder)
                os.chdir(folder)

                for i in range(num):
                        self.get_text()
                        print('{} 正在下载中...'.format(self.title)) 
                        self.save_novel()
                        self.get_next_url()



if __name__ == '__main__':
        url = input('请输入需要开始下载章节网址（笔趣阁https://www.biqiuge.com/）：')
        folder = input('请输入需要创建的文件夹：')
        num = input('请输入需要的小说章数：')
        while True:
                if not num.isdigit():
                        num = input('输入页码错误，请重新输入：')
                else:
                        num = int(num)
                        break
        DN = Download_Novel(url)
        DN.run(folder=folder, num=num)
