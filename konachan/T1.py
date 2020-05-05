# EH 批量采集＆更新

import requests
import bs4
# import os
import time
import shelve
# from random import randint
# from pprint import pprint
import copy
# import openpyxl
import sys
# from hashlib import sha1
# from shutil import rmtree

sys.setrecursionlimit(1000000)


# Html download function
# 输入参数raw=1表示直接返回res raw=0则返回res.text
# 若下载失败， 一律返回None
def download(url, num_retries=3, cookie='', params='', raw=0, timeout=40):
    print('Downloading: ', url)
    headers = {
        'user-agent':
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) ' +
        'Gecko/20100101 Firefox/75.0',
        'connection':
        'keep-alive'
    }
    if cookie != '':
        headers['cookie'] = cookie
    try:
        resp = requests.get(url, headers=headers,
                            params=params, timeout=timeout)
        html = resp.text
        if resp.status_code >= 400:
            print('Download error: ', resp.text)
            html = None
            if num_retries and 500 <= resp.status_code < 600:
                return download(url, num_retries-1)
    except requests.exceptions.RequestException:
        print('Download error!!!')
        html = None
        resp = None
    except requests.exceptions.Timeout:
        print('请求超时!')
        html = None
        resp = None
    if raw == 1:
        return resp
    else:
        return html


# 测试
if __name__ == '__main__':
    tags = 'masturbation+order:score'
    startUrl = 'https://konachan.com/post?page=1&tags=' + tags
    endFlag = 0
    pageCnt = 0
    maxPage = 5
    works = []
    url = startUrl
    while endFlag == 0:
        page = download(url=url, raw=0, timeout=40)
        if page is None:
            break
        '''
        pageFile = open('T.html', 'w', encoding='utf-8')
        pageFile.write(page)
        pageFile.close()
        '''

        soup = bs4.BeautifulSoup(page, 'lxml')
        nodeA = soup.findAll(attrs={'id': 'post-list-posts'})
        nodeB = nodeA[0].findAll('li')
        work = {}
        for item in nodeB:
            work['id'] = item.get('id')
            nodeC = item.findAll('img')
            t = nodeC[0].get('alt').split(' ')
            t[t.index('User:'):] = []
            t[0:t.index('Tags:')+1] = []
            work['tags'] = copy.copy(t)
            nodeD = item.findAll(attrs={'class': 'directlink'})
            link = nodeD[0].get('href')
            work['link0'] = link
            if '/jpeg/' in link:
                link = link.replace('/jpeg/', '/image/')
                link = link.replace('.jpg', '.png')
            work['link1'] = link
            work['sample'] = link[0:link.find(
                'Konachan.com')+28].replace('image', 'sample')+'sample.jpg'
            works.append(copy.copy(work))

        for item in works:
            link = item['link1']
            rawPic = download(url=link, raw=1, timeout=60)
            if rawPic is None:
                continue
            picFile = open(item['id']+item['link1'][-4:], 'wb')
            for chunk in rawPic.iter_content(100000):
                picFile.write(chunk)
            picFile.close()
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

        pageCnt += 1
        nodeE = soup.find(attrs={'class': 'next_page'})
        if 'rel' not in nodeE.attrs or pageCnt >= maxPage:
            endFlag = 1
        else:
            url = 'https://konachan.com'+nodeE.get('href')

    # 保存works 于 dicFile
    dicFile = shelve.open('dicFile')
    dicFile['works'] = works
    dicFile.close()

    
