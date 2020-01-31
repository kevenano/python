# EOP 批量采集
import requests
import bs4
import os
import time
import shelve
import re
from random import randint
import copy

Cookie = 'menunew=0-0-0-0; ' +\
    'username=kevenano; ' +\
    'password=qhm2012%40%40%40; ' + \
    'remember=1; ' +\
    'huiyuan=' +\
    '7f39Vfi514lH9dndqdzF3wpjjvZy1TiC9eReu%2FmI2RXQTumC1OpKxh7MrBE; ' +\
    'FWE_getuser=kevenano; ' +\
    'FWE_getuserid=161673; ' +\
    'login_mima=9161d8bd2056459a0a96f80f2e6a818d; ' +\
    'PHPSESSID=75e2ed7a61e14459313010386cb2ecdc; ' +\
    'think_language=en-US'
workPath = '/home/kevenano/Music/EOP'


# Html download function
def download(url, num_retries=3, cookie='', raw=0):
    print('Downloading: ', url)
    headers = {
        'user-agent':
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0)' +
        ' Gecko/20100101 Firefox/72.0',
        'connection':
        'keep-alive'
    }
    if cookie != '':
        headers['cookie'] = cookie
    try:
        resp = requests.get(url, headers=headers)
        html = resp.text
        if resp.status_code >= 400:
            print('Download error: ', resp.text)
            html = None
            if num_retries and 500 <= resp.status_code < 600:
                return download(url, num_retries-1)
    except requests.exceptions.RequestException:
        print('Download error')
        html = None
    if raw == 1:
        return resp
    else:
        return html


# 获取关键头
def getKey(save_html=0):
    pageCnt = 0
    pageAll = 230
    keys = []
    try:
        os.makedirs('Html')
    except FileExistsError:
        print('Folder already exist!')
    while pageCnt < pageAll:
        # Download & Save Html File
        pageCnt += 1
        print('Deal with page ', pageCnt)
        pageUrl = 'https://www.everyonepiano.cn/' +\
            'Music-class12-?%3F%3F%3F_html%3Fcome=web&p=' +\
            str(pageCnt) +\
            '&canshu=clicks&word=&author=&jianpu=&paixu=desc&username='
        pageHtml = download(url=pageUrl, cookie=Cookie)
        if pageHtml is None:
            continue
        if bool(save_html):
            htmlFile = open('Html/listPage'+str(pageCnt)+'.html', 'w')
            htmlFile.write(pageHtml)
            htmlFile.close()
        # 提取Key
        pageSoup = bs4.BeautifulSoup(pageHtml, 'lxml')
        allElem = pageSoup.find_all('a', attrs={'class': 'Title'})
        if len(allElem) < 2:
            continue
        for i in range(1, len(allElem)):
            keys.append(allElem[i].get('href').replace('/Music-', ''))
        # 延时
        print('Sleeping...')
        time.sleep(randint(1, 5))

    # 保存keys变量
    keyFile = shelve.open('keyFile')
    keyFile['keys'] = keys
    keyFile.close()
    print('Keys saved to keyFile!')


# 构造资源下载页URL字典
# 字典保存在 urlFile 中 workDic 字典变量中
#  以id 为索引
# 包括: pdf midi eopn eopm title id
def buildUrl():
    # 获取keys
    keyFile = shelve.open('keyFile')
    keys = keyFile['keys']
    # 构造URL 字典
    workDic = {}
    urlDic = {}
    titleReg = re.compile(r'\d+-(.+)\.html')
    idReg = re.compile(r'(\d+)')
    for urlKey in keys:
        pdfPage = 'https://www.everyonepiano.cn/PDF-'+urlKey
        midiPage = 'https://www.everyonepiano.cn/Midi-'+urlKey
        eopnPage = 'https://www.everyonepiano.cn/Eopn-down-'+urlKey
        eopmPage = 'https://www.everyonepiano.cn/Eopm-down-'+urlKey
        title = titleReg.search(urlKey).group(1)
        workId = idReg.search(urlKey).group(1)
        urlDic['pdf'] = pdfPage
        urlDic['midi'] = midiPage
        urlDic['eopn'] = eopnPage
        urlDic['eopm'] = eopmPage
        urlDic['title'] = title
        urlDic['id'] = workId
        workDic[workId] = copy.copy(urlDic)  # 小心！！！！！！！
    # 保存字典
    urlFile = shelve.open('urlFile')
    urlFile['workDic'] = workDic
    urlFile.close()
    print('Page urls saved to urlFile!')


# 从资源下载页 获取直接资源下载链接 同时下载相应资源
def getDown():
    # 打开work字典
    urlFiel = shelve.open('urlFile')
    workDic = urlFiel['workDic']
    # 创建住文件夹
    os.makedirs('mainFolder')
    count = -1
    subFolder = 0
    # 获取下载url 保存在downUrl
    downUrl = {}
    for work in workDic.values():
        # 重置主工作区
        os.chdir(workPath+'/mainFolder')
        # 提示信息头
        print('Deal with '+work['title'])
        print(count+2, 'of', len(workDic))
        # 以40个项目为单位，创建子文件夹
        count += 1
        if count % 40 == 0:
            subFolder += 1
            os.makedirs(str(subFolder))
            if count > 1:
                # 休息1~2分钟
                print('Long sleeping...')
                time.sleep(randint(60, 120))
        # 进入subFolder
        os.chdir(str(subFolder))
        # 在子文件夹下创建当前work对应的文件夹
        # 同时将工作区移入
        os.makedirs(work['id']+'_'+work['title'])
        os.chdir(work['id']+'_'+work['title'])

        # 用于暂存的字典
        # 包括 pdfS  pdfN midi eopn eopm
        #     五线谱 简谱
        itemUrl = {}

        # TODO: pdf down
        # 创建pdf文件夹 保存pdf相关资源
        os.makedirs('pdf')
        pdfHtml = download(url=work['pdf'], cookie=Cookie)
        if pdfHtml is None:
            # 若网页为空 设置对应下载链接为空
            itemUrl['pdfS'] = ''
            itemUrl['pdfN'] = ''
        else:
            # 保存网页
            htmlFile = open('pdf/'+work['id']+'.html', 'w')
            htmlFile.write(pdfHtml)
            htmlFile.close()
            # 提取下载链接
            pdfSoup = bs4.BeautifulSoup(pdfHtml, 'lxml')
            urlElem = pdfSoup.find_all('a', attrs={'class': 'btn-success'})
            pdfS = 'https://www.everyonepiano.cn' +\
                urlElem[0].get('href')
            pdfN = 'https://www.everyonepiano.cn' +\
                urlElem[1].get('href')
            # 将链接存入字典
            itemUrl['pdfS'] = pdfS
            itemUrl['pdfN'] = pdfN

            # 直接下载
            # 五线谱
            pdfSRes = download(url=pdfS, cookie=Cookie, raw=1)
            pdfSFile = open('pdf/'+work['title']+'-五线谱'+'.pdf', 'wb')
            for chunk in pdfSRes.iter_content(100000):
                pdfSFile.write(chunk)
            pdfSFile.close()
            # 简谱
            pdfNRes = download(url=pdfN, cookie=Cookie, raw=1)
            pdfNFile = open('pdf/'+work['title']+'-简谱'+'.pdf', 'wb')
            for chunk in pdfNRes.iter_content(100000):
                pdfNFile.write(chunk)
            pdfNFile.close()

        # TODO: midi down
        # 创建midi文件夹 保存midi资源
        os.makedirs('midi')
        midiHtml = download(url=work['midi'], cookie=Cookie)
        if midiHtml is None:
            itemUrl['midi'] = ''
        else:
            # 保存html
            htmlFile = open('midi/'+work['id']+'.html', 'w')
            htmlFile.write(midiHtml)
            htmlFile.close()
            # 提取下载链接
            midiSoup = bs4.BeautifulSoup(midiHtml, 'lxml')
            urlElem = midiSoup.find_all('a', attrs={'class': 'btn-success'})
            midi = 'https://www.everyonepiano.cn' +\
                urlElem[0].get('href')
            # 写入字典
            itemUrl['midi'] = midi

            # 直接下载
            midiRes = download(url=midi, cookie=Cookie, raw=1)
            midiFile = open('midi/'+work['title']+'.mid', 'wb')
            for chunk in midiRes.iter_content(100000):
                midiFile.write(chunk)
            midiFile.close()

        # TODO: eopn down
        # 创建eopn文件夹 保存eopn资源
        os.makedirs('eopn')
        eopnHtml = download(url=work['eopn'], cookie=Cookie)
        if eopnHtml is None:
            itemUrl['eopn'] = ''
        else:
            # 保存html
            htmlFile = open('eopn/'+work['id']+'.html', 'w')
            htmlFile.write(eopnHtml)
            htmlFile.close()
            # 提取下载链接
            eopnSoup = bs4.BeautifulSoup(eopnHtml, 'lxml')
            urlElem = eopnSoup.find_all('a', attrs={'class': 'btn-success'})
            eopn = 'https://www.everyonepiano.cn' +\
                urlElem[0].get('href')
            # 写入字典
            itemUrl['eopn'] = eopn

            # 直接下载
            eopnRes = download(url=eopn, cookie=Cookie, raw=1)
            eopnFile = open('eopn/'+work['title']+'.eopn', 'wb')
            for chunk in eopnRes.iter_content(100000):
                eopnFile.write(chunk)
            eopnFile.close()

        # TODO: eopm down
        # 创建eopm文件夹 保存eopm资源
        os.makedirs('eopm')
        eopmHtml = download(url=work['eopm'], cookie=Cookie)
        if eopnHtml is None:
            itemUrl['eopm'] = ''
        else:
            # 保存html
            htmlFile = open('eopm/'+work['id']+'.html', 'w')
            htmlFile.write(eopmHtml)
            htmlFile.close()
            # 提取下载链接
            eopmSoup = bs4.BeautifulSoup(eopmHtml, 'lxml')
            urlElem = eopmSoup.find_all('a', attrs={'class': 'btn-success'})
            eopm = 'https://www.everyonepiano.cn' +\
                urlElem[0].get('href')
            # 写入字典
            itemUrl['eopm'] = eopm

            # 直接下载
            eopmRes = download(url=eopm, cookie=Cookie, raw=1)
            eopmFile = open('eopm/'+work['title']+'.eopm', 'wb')
            for chunk in eopmRes.iter_content(100000):
                eopmFile.write(chunk)
            eopmFile.close()

        # 将当前资源的所有下载链接写入字典 downUrl
        downUrl[work['id']] = itemUrl
        # 休息3~10秒
        print('Sleeping...')
        time.sleep(randint(3, 10))

    # 全部下载完成
    # 保存下载地址字典变量
    os.chdir(workPath)
    downFile = shelve.open('downFile')
    downFile['downUrl'] = downUrl
    print('Misiion all accomplish!')


# 测试
if __name__ == '__main__':
    os.chdir(workPath)
    getDown()


# MAIN: https://www.everyonepiano.cn/Music-class12-%E5%8A%A8%E6%BC%AB.html?
#       canshu=clicks&word=&author=&come=web
# DETA: https://www.everyonepiano.cn/Music-1801-%E5%8D%83%E6%9C%AC%E6%A8%B1-
#       %E5%88%9D%E9%9F%B3%E6%9C%AA%E6%9D%A5.html
# PDF0: https://www.everyonepiano.cn/PDF-1801-%E5%8D%83%E6%9C%AC%E6%A8%B1-
#       %E5%88%9D%E9%9F%B3%E6%9C%AA%E6%9D%A5.html
# MIDI: https://www.everyonepiano.cn/Midi-1801-%E5%8D%83%E6%9C%AC%E6%A8%B1-
#       %E5%88%9D%E9%9F%B3%E6%9C%AA%E6%9D%A5.html
# EOPN: https://www.everyonepiano.cn/Eopn-down-1801-
#       %E5%8D%83%E6%9C%AC%E6%A8%B1-%E5%88%9D%E9%9F%B3%E6%9C%AA%E6%9D%A5.html
# EOPM: https://www.everyonepiano.cn/Eopm-down-1801-
#       %E5%8D%83%E6%9C%AC%E6%A8%B1-%E5%88%9D%E9%9F%B3%E6%9C%AA%E6%9D%A5.html
# PAGE: https://www.everyonepiano.cn/Music-class12-?%3F%3F%3F_html
#       %3Fcome=web&p=1&canshu=clicks&word=&author=&jianpu=&paixu=desc&username=
