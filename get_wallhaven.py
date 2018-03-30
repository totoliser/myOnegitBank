import os
import requests
import queue
import time
import threading

from lxml import etree


class Thread_Crawl(threading.Thread):
    def __init__(self,threadName,p,htmlQueue):
        threading.Thread.__init__(self)
        self.threadName = threadName
        self.p = p
        self.htmlQueue = htmlQueue


    def run(self):

        print('启动' + self.threadName)

        self.tupian_spider()
        print('结束'+self.threadName)


    def tupian_spider(self):
        while  not HTML_EIXT:
            if queue.Queue.empty(self.p):
                break
            else:
                page = self.p.get(False)
                print('tupian_spider=',self.threadName,',page=',str(page))

                url = "https://alpha.wallhaven.cc/search?q=%s&search_image=&page=%s"%(commend,str(page))
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',}
                content = requests.get(url=url,headers=headers)
                html = etree.HTML(content.content)
                img_url = html.xpath("//section[@class='thumb-listing-page']//ul//li//a[@class='preview']/@href")
                # print(img_url)
                for imgurl in img_url:
                    print(imgurl)
                    timeout = 4
                    while timeout>0:
                        timeout -=1
                    try:

                        content1 = requests.get(url=imgurl, headers=headers)
                        self.htmlQueue.put(content1.content)
                        break
                    except Exception:
                        print('爬虫部分结束')
                    if timeout<0:
                        print('timeout',imgurl)


class Thread_Parse(threading.Thread):

    def __init__(self,threadName,htmlQueue):
        super(Thread_Parse,self).__init__()
        self.threaName = threadName
        self.htmlQueue = htmlQueue
        # self.lock =lock
        # self.f= f

    def run(self):
        print('启动' + self.threaName)
        # global total,HTML_EIXT
        while not HTML_EIXT:
            try:
                item = self.htmlQueue.get(False)
                if not item:
                    pass
                self.parse(item)
                self.htmlQueue.task_done()
                print('解析线程：'+self.threaName)
            except:
                pass
        print('结束' +self.threaName)

    def parse(self,item):
        global total
        try:
            html = etree.HTML(item)
            image = html.xpath("//div[@class='scrollbox']//img[@id='wallpaper']/@src")

            # with self.lock:
            for strimg in image:
                print('https:'+strimg)


        except:
            pass

        # with self.lock:
        #     total+=1


PAGE_EIXT = False
#html源码队列
#设置线程锁
lock = threading.Lock()
total = 0

HTML_EIXT = False


def main():

    #创建页码队列
    pageQueue = queue.Queue(40)
    for page in range(1,41):
        pageQueue.put(page)

    htmlQueue = queue.Queue()
    global commend
    commend = input('请输入要搜索的图片:')
    #初始化采集线程

    pageThreads = []


    pageList = ['线程1','线程2','线程3']
    for threadName in pageList:
        thread = Thread_Crawl(threadName,pageQueue,htmlQueue)
        thread.start()
        pageThreads.append(thread)

    #初始化解析线程
    parseThreads =[]
    parseList = ['解析线程1','解析线程2','解析线程3']
    #
    for threadName in parseList:
        thread = Thread_Parse(threadName,htmlQueue)
        thread.start()
        parseThreads.append(thread)

    #等待队列清空
    while not pageQueue.empty():
        pass

    #等待所有线程完成后，结束线程
    for p in pageThreads:
        p.join()

    while not htmlQueue.empty():
         pass

    global HTML_EIXT
    HTML_EIXT = True
    #
    for h in pageThreads:
        h.join()

    print('爬取结束')

if __name__ =='__main__':
    main()







