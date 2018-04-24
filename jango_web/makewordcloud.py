import requests
import re
import json
import time
import pathlib
from jango_web import Instagrams
from bs4 import BeautifulSoup
from jango_web import GetQueryId
from jango_web import displaywords


baseURL='https://www.instagram.com/graphql/query/?query_hash='

headers={
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cookie': 'mid=Wq6HMgALAAEdXyO-bI4pylIzXv4p; datr=Y4euWsG3xGk5J4UtnFsIGaeD; csrftoken=d52GvOkjTOG3N53xIM7JDL7wT8A02muJ; ds_user_id=7317471414; fbm_124024574287414=base_domain=.instagram.com; sessionid=IGSC81e2a2d217c30a3bd0237e8774d8491814730e69c61f9d89e70999151ba171a9%3AZqnP8Ihbq9YTOmBFMAlNdqV1tqj4VYVV%3A%7B%22_auth_user_id%22%3A7317471414%2C%22_auth_user_backend%22%3A%22accounts.backends.CaseInsensitiveModelBackend%22%2C%22_auth_user_hash%22%3A%22%22%2C%22_platform%22%3A4%2C%22_token_ver%22%3A2%2C%22_token%22%3A%227317471414%3Affi3pFfH1RdGHfg4ICZrCogbmBD3howl%3A381b3b08030d694c5015c7a3fbd4b8d3faa4b834e4ca66d5a192b114a0b565f5%22%2C%22last_refreshed%22%3A1523976978.9011130333%7D; rur=FTW; ig_pr=1.25; ig_vh=743; ig_or=landscape-primary; ig_vw=756; urlgen="{\"time\": 1524016388\054 \"140.82.11.142\": 20473}:1f8dDt:uWvzBHfNZCzZbiamDtMQHIyXBa8"; fbsr_124024574287414=yLFB1i2Zkzy44lIKzRPCBcP7O-NiSt_uYyp52TbCYvs.eyJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImNvZGUiOiJBUUFoRmpnQVZueGR1Z1U1NFUycVNnR3VWclBCdmdSajd2YjZZeXFfakFjQTRadFdsZEJ6TzE5QkpLZ3Jsb01xSTg0RGNESnA1anp0cmNzWUpaVHVTYnBRQTU3UnNlcF9HcmVPRDh5LWhDSFUzUC0tMGdrMGlvNGVab2JUUndLMUp5TklhdXRGQjZoTmVha3FnWmFWMHdCMTZoS3FOcVBPVGNGWGRlYklSV2xtcUNqQVRhalBSQUZXalNHaGU1ZXBRWnBpOHNYMmctRWpxQnRnallpTy1teHFVNWYyN0xzSFd2OW9nTFVLa0pIUmQ3S0w4RGxxb3ZSNWJPNFBLUlNfTkZLMzFZbXJNRVNHdG1fY25UQW1IVEJKS0l1SHY2YXhJU2FDNDIzTGw0REZQMWRDRnpLbVpIdGpTUXNWV2VBT2JueE9CY25neUxTcm1PUkExR0I4N3JyTyIsImlzc3VlZF9hdCI6MTUyNDAyMDEyNSwidXNlcl9pZCI6IjEwMDAxNjIxMDg2Nzk4NyJ9',
    'referer': 'https://www.instagram.com/cheer_wr/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'x-instagram-gis': '11f8d46fd05a09c911e7b529c0786be8',
    'x-requested-with': 'XMLHttpRequest'
}


def getJsonData(nickname):

    url='https://www.instagram.com/'+nickname
    #根据首页返回的的内容判断还有没有下一页
    ptr=0
    response=requests.get(url)
    #response.encoding=response.apparent_encoding
    print(url,response.status_code)

    soup=BeautifulSoup(response.content,'lxml')
    realnames=soup.select('head > title')[0]
    realname=realnames.get_text().split('(')[0].strip()

    shortcode=[]
    shortcodes=re.findall(r'\"shortcode\":\".*?\"',response.text)
    for i in range(len(shortcodes)):
        shortcode.append(shortcodes[i].split('\"')[3])

    post_time = []
    post_times = re.findall(r'\"taken_at_timestamp\":.*?,', response.text)
    for i in range(len(post_times)):
        post_time.append(int(post_times[i].split(':')[1].split(',')[0]))

    Data = {
        'shortcode': shortcode,
        'post_time': post_time,
    }
    Instagrams.mthread(Data,nickname,ptr)
    ptr = len(shortcode)

    has_next_page = re.findall(r'\"has_next_page\":.*?,', response.text)[0].split(':')[1].split(',')[0]
    #如果有下一页，构建异步加载请求
    if has_next_page=='true':
        end_cursor=re.findall(r'\"end_cursor\":\".*?\"',response.text)[0].split('\"')[3]
        user_id=re.findall(r'\"id\":\".*?\"',response.text)[0].split('\"')[3]
        queryIds=[]
        GetQueryId.getQueryId(url,queryIds)
        queryId=queryIds[1]

        info={
            'end_cursor':end_cursor,
            'user_id':user_id,
            'queryId':queryId,
        }

        URL = baseURL + info['queryId'] + '&variables=' + '{\"id\":\"' + info['user_id'] + '\",\"first\":12,\"after\":\"' + info['end_cursor'] + '\"}'

        response=requests.get(URL,headers=headers)
        data=json.loads(response.text)

        for i in range(len(data['data']['user']['edge_owner_to_timeline_media']['edges'])):
            shortcode.append(data['data']['user']['edge_owner_to_timeline_media']['edges'][i]['node']['shortcode'])
            post_time.append(data['data']['user']['edge_owner_to_timeline_media']['edges'][i]['node']['taken_at_timestamp'])

        Data = {
            'shortcode': shortcode,
            'post_time': post_time
        }
        Instagrams.mthread(Data, nickname,ptr)
        ptr = len(shortcode)
        More = data['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']

        while More:
            # time.sleep(1)
            end_cursor = data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
            URL=updateURL(info, end_cursor)

            response = requests.get(URL, headers=headers)
            data = json.loads(response.text)
            for i in range(len(data['data']['user']['edge_owner_to_timeline_media']['edges'])):
                shortcode.append(data['data']['user']['edge_owner_to_timeline_media']['edges'][i]['node']['shortcode'])
                post_time.append(data['data']['user']['edge_owner_to_timeline_media']['edges'][i]['node']['taken_at_timestamp'])

            Data = {
                'shortcode': shortcode,
                'post_time': post_time
            }
            Instagrams.mthread(Data, nickname,ptr)
            ptr=len(shortcode)
            More = data['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
    time.sleep(1)
    return realname





def updateURL(info,end_cursor):
    info['end_cursor']=end_cursor
    URL = baseURL + info['queryId'] + '&variables=' + '{\"id\":\"' + info['user_id'] + '\",\"first\":12,\"after\":\"' + info['end_cursor'] + '\"}'
    return URL


# print('input nickname(like cheer_wr):',end='\t')
# nickname=input()
# URL='https://www.instagram.com/'+nickname
# print('挑选一张图片(尽量白底)放到程序所在文件夹中，输入照片名称。(默认为方形，输入0):',end='\t')
# imgname=input()
# path=pathlib.Path(imgname)
# while imgname!='0' and not(path.exists()):
#     print('图片名称错误或不存在！请重新输入：',end='\t')
#     imgname=input()
#     path = pathlib.Path(imgname)
#
# path=pathlib.Path(nickname+'forwordcloud.csv')
# if path.exists():
#     print('本目录已有数据，是否使用现有数据制作词云图（Y/N）：',end='\t')
#     ans=input()
#     while ans!='Y' and ans!='N':
#         print('本目录已有数据，是否使用现有数据制作词云图（Y/N）：', end='\t')
#         ans=input()
#     if ans=='Y':
#         realname=''
#         displaywords.makewordcloud(nickname, realname, imgname)
#         print('Done!(如需修改屏蔽词,在stopwords.txt中修改')
#     else :
#         open(nickname + 'forwordcloud.csv', 'w', encoding='utf-8-sig', newline='')
#         realname = getJsonData(URL, nickname)
#         displaywords.makewordcloud(nickname, realname, imgname)
#         print('Done!(如需修改屏蔽词,在stopwords.txt中修改')
# else:
#     realname=getJsonData(URL,nickname)
#     displaywords.makewordcloud(nickname,realname,imgname)
#     print('Done!(如需修改屏蔽词,在stopwords.txt中修改')
#
#
