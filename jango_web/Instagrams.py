import requests
from bs4 import BeautifulSoup
import csv
import time
import random
import threading

headersURL={
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}

proxy={
    'http':'159.89.175.86'
}


def instagram(shortcode,post_time,nickname):
    # for item in range(ptr,len(Data['shortcode'])):
        url = 'https://www.instagram.com/p/'+shortcode+'/?taken-by='+nickname

        response=requests.get(url)
        print(url,response.status_code)

        # post_time = time.strftime('%Y-%m-%d %H.%M.%S ', time.localtime(Data['post_time'][item]))
        get_time=time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime(post_time))
        soup=BeautifulSoup(response.content,'lxml')
        titles=soup.select('head > title')
        title=titles[0].get_text()
        data={
            'get-time':get_time,
            'title':title
        }
        with open('jango_web/static/'+nickname+'forwordcloud.csv','a',encoding='utf-8-sig',newline='') as f:
            fieldnames=['get-time','title']
            writer = csv.DictWriter(f,fieldnames=fieldnames)
            writer.writerow(data)

        # time.sleep(random.uniform(0.5,1))

def mthread(Data,nickname,ptr):
    threads=[]
    for item in range(ptr,len(Data['shortcode'])):
        shortcode=Data['shortcode'][item]
        post_time=Data['post_time'][item]
        thread = threading.Thread(target=instagram,args=(shortcode,post_time,nickname))
        thread.setDaemon(True)  ##设置守护线程
        thread.start()  ##启动线程
        threads.append(thread)

