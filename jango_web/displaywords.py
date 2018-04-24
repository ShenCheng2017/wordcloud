from wordcloud import WordCloud
import jieba
from scipy.misc import imread
import time

import csv

def makewordcloud(nickname,realname):
    with open('jango_web/static/'+nickname+'forwordcloud.csv','r',encoding='utf-8-sig') as f:
        fr=csv.reader(f)
        items=[item for item in fr]
        contents=[]
        for i in range(len(items)):
            contents.append(items[i][1])


    content=" ".join(contents)
    f=open('jango_web/stopwords.txt', 'a', encoding='utf-8-sig')
    f.write('\n'+realname)
    f.close()
    f=open('jango_web/stopwords.txt','r',encoding='utf-8-sig')
    stop_text=f.read()

    stop_text_list=stop_text.split('\n')
    stop_text_list.append(realname)
    seg_list = jieba.cut(content, cut_all=False, HMM=True)

    mywordlist=[]
    for myword in seg_list:
        if not(myword.strip() in stop_text_list) and len(myword.strip())>1:
            mywordlist.append(myword)

    text=" ".join(mywordlist)
    imgname=open('jango_web/static/imgname.txt','r',encoding='utf-8-sig').read().strip()
    if imgname=='':
        wordcloud = WordCloud(background_color="white", scale=4, font_path=r"C:\FZSTK.TTF",max_words=2000).generate(text)
    else:
        color_mask=imread('jango_web/static/'+imgname)
        wordcloud = WordCloud(background_color="white", mask=color_mask,scale=2, font_path=r"C:\FZSTK.TTF", max_words=2000).generate(text)

    wordcloud.to_file(nickname+'.jpg')

