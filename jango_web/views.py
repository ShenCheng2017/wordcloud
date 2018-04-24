# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from jango_web.displaywords import makewordcloud
from django import forms
from jango_web.makewordcloud import getJsonData


# Create your views here.
def index(request):
    # f = open('E:/double_c2019.jpg', 'rb')
    # response = HttpResponse(f.read(), content_type='image/jpeg')
    # return response
    # return HttpResponse(u'helloword')
    return render(request,'index.html')

def nickname(request):
    if request.method=='GET':
        open('jango_web/static/nickname.txt','w',encoding='utf-8-sig').write(request.GET['nickname'])
        return render(request,'upload.html')

def filename(request):
    if request.method=='POST':
        obj=request.FILES.get('filename')
        if obj==None:
            open('jango_web/static/imgname.txt', 'w', encoding='utf-8-sig').write('')
        else:
            f=open('jango_web/static/'+obj.name,'wb')
            open('jango_web/static/imgname.txt', 'w', encoding='utf-8-sig').write(obj.name)
            for chunk in obj.chunks():
                f.write(chunk)
            f.close()

        def readFile(fn, buf_size=262144):  # 大文件下载，设定缓存大小
            f = open(fn, "rb")
            while True:  # 循环读取
                c = f.read(buf_size)
                if c:
                    yield c
                else:
                    break
            f.close()

        nickname=open('jango_web/static/nickname.txt','r',encoding='utf-8-sig').read().strip()
        open('jango_web/static/' + nickname + 'forwordcloud.csv', 'w', encoding='utf-8-sig', newline='')
        makewordcloud(nickname,getJsonData(nickname))
        filepath_=nickname+'.jpg'

        response = HttpResponse(readFile(filepath_), content_type='image/jpeg')  # 设定文件头，这种设定可以让任意文件都能正确下载，而且已知文本文件不是本地打开

        return response
