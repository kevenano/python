# EOP 批量采集
# 方案二
import requests
import bs4
import os
import time
import shelve
import re
from random import randint
from pprint import pprint
import copy
import openpyxl
import sys
from hashlib import sha1

sys.setrecursionlimit(1000000)


# Html download function
# 输入参数raw=1表示直接返回res raw=0则返回res.text
# 若下载失败， 一律返回None
def download(url, num_retries=3, cookie='', params='', raw=0, timeout=40):
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


# 获取搜索参数
def getParam():
    # 构造搜索参数
    params = {}
    params['page'] = 0          # 页数（从零开始）
    params['f_cats'] = ''       # 类别
    params['f_search'] = ''     # 搜索字段
    params['advsearch'] = 1     # 高级筛选
    params['f_sname'] = 'on'    # Search Gallery Name
    params['f_stags'] = 'on'    # Search Gallery Tags
    params['f_sr'] = 'on'       # Rating
    params['f_srdd'] = 4        # Minimum Rating
    # 可选类别
    cats = {}
    cats['Doujinshi'] = 1021
    cats['Manga'] = 1019
    cats['Artist CG'] = 1015
    cats['Game CG'] = 1007
    cats['Non-H'] = 767
    cats['Image Set'] = 991
    cats['Cosplay'] = 959
    # 获取搜索类别
    inTemp = input('搜索类别：')
    while inTemp not in cats:
        print('输入错误！')
        inTemp = input('请重新输入：')
        if inTemp == 'exit' or inTemp == 'quit':
            exit()
    params['f_cats'] = cats[inTemp]
    inTemp = ''
    # 获取搜索字段
    inTemp = input('关键词:')
    params['f_search'] = inTemp
    inTemp = ''
    # 最低评分
    inTemp = input('最低评分:')
    while int(inTemp) > 5 or int(inTemp) < 0:
        print('输入错误！')
        inTemp = input('请重新输入：')
        if inTemp == 'exit' or inTemp == 'quit':
            exit()
    params['f_srdd'] = int(inTemp)
    del inTemp
    return params


# 下载并保存搜索结果页
# 返回本地html所在的位置path
def getSearch(url, params, startPage, endPage):
    # 记录入口工作目录
    inPath = os.getcwd()
    # 创建文件夹保存搜索页
    try:
        os.makedirs('scHtml')
    except FileExistsError:
        print('scHtml folder already exists!')
    os.chdir('scHtml')
    folderPath = os.getcwd()
    # 循环下载搜索页
    pageCnt = startPage
    while pageCnt <= endPage:
        print('Deal with page ', pageCnt)
        params['page'] = pageCnt
        scHtml = download(url=url, params=params, raw=0, timeout=40)
        if scHtml is None:
            continue
        scFile = open(str(pageCnt)+'.html', 'w')
        scFile.write(scHtml)
        scFile.close()
        pageCnt += 1
    print('搜索结果页下载完成！')
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    # 重置工作目录
    os.chdir(inPath)
    return folderPath


# 从搜索页html中提取每一件的url
# 保存在dicFile中
# 以title的SHA1的后8为作为字典的key
# 包含title url SHA1
# 输入参数 html所在的文件夹
def getWorkUrl(htmlFolder):
    # 记录入口工作目录
    inPath = os.getcwd()
    # 将当前工作目录移入htmlFolder
    os.chdir(htmlFolder)
    # 循环处理每一页
    # 获取title 和 url 计算title的SHA1
    workDic = {}
    workCnt = 1
    htmlList = os.listdir()
    for page in htmlList:
        tempDic = {}
        htmlFile = open(page, 'r')
        mainSoup = bs4.BeautifulSoup(htmlFile, 'lxml')
        htmlFile.close()
        nodeA = mainSoup.find('table', attrs={'class': 'gltc'})
        nodeB = nodeA.find_all('td', attrs={'class': 'glname'})
        for item in nodeB:
            tempDic['url'] = item.find('a').get('href')
            tempDic['title'] = item.find(
                'div', attrs={'class': 'glink'}).getText()
            workSHA1 = sha1(tempDic['title'].encode(
                encoding='UTF-8')).hexdigest()
            tempDic['SHA1'] = workSHA1
            workDic[workSHA1[-9:-1]] = copy.copy(tempDic)
            workCnt += 1

    # 回到work对应的工作目录保存workDic
    os.chdir(workPath)
    dicFile = shelve.open('dicFile')
    dicFile['workDic'] = workDic
    dicFile.close()
    print('Url 提取完毕！')
    print('保存在dicFile中workDic中')
    # 重置工作目录
    os.chdir(inPath)


# 主下载函数
# 输入参数： deWork 一件work的字典
# 返回值：  成功返回１，　否则返回None
def downWork(deWork):
    # 记录入口工作目录
    inPath = os.getcwd()
    # 创建该作品的文件夹
    try:
        os.mkdir(deWork['SHA1'][-9:-1])
    except FileExistsError:
        print('Work already exist!')
        return None
    os.chdir(deWork['SHA1'])
    # 下载详情页
    deUrl = deWork['url']
    dePage = download(url=deUrl)
    if dePage is None:
        print('Fail to download detail page!')
        return None
    # 提取第一页的地址
    deSoup = bs4.BeautifulSoup(dePage, 'lxml')
    nodeA = deSoup.find('div', attrs={'class': 'gdtm'})
    iniPageUrl = nodeA.find('a').get('href')
    # 循环下载每一页并提取图片的下载链接及下一页的地址
    curPageUrl = ''
    nextPageUrl = iniPageUrl
    pageCnt = 0
    # 循环获取全部
    while nextPageUrl != curPageUrl:
        pageCnt += 1
        print('Deal with page ', pageCnt)
        curPageUrl = nextPageUrl
        curPage = download(url=curPageUrl)
        if curPage is None:
            print('Fail to download page ', pageCnt)
            continue
        curSoup = bs4.BeautifulSoup(curPage, 'lxml')
        nodeA = curSoup.find('div', attrs={'id': 'i3'})
        curPicUrl = nodeA.find('img').get('src')
        nextPageUrl = nodeA.find('a').get('href')
        # 根据curPicUrl 下载保存图片
        rawPic = download(url=curPicUrl, raw=1, timeout=60)
        if rawPic is None:
            print('**')
            continue
        picFile = open(os.path.basename(curPicUrl), 'wb')
        for chunk in rawPic.iter_content(100000):
            picFile.write(chunk)
        picFile.close()
        # 页间延迟
        time.sleep(randint(1, 3))
    # 下载完成， 重置工作目录
    print('Finish!')
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    os.chdir(inPath)
    return 1


# 批量下载函数
def downWorkS():
    # 记录入口工作目录
    inPath = os.getcwd()
    # 打开包含详情页的workDic
    dicFile = shelve.open('dicFile')
    workDic = dicFile['workDic']
    dicFile.close()
    # 创建mainFolder保存works
    try:
        os.makedirs('mainFolder')
    except FileExistsError:
        print('MainFolder already exist!')
    os.chdir('mainFolder')
    mainPath = os.getcwd()
    # 循环处理每一件work
    workCnt = 0
    folderCnt = 1
    failCnt = []
    for work in workDic.values():
        # 25为单位创建子文件夹
        if workCnt % 25 == 0:
            os.chdir(mainPath)
            os.makedirs(str(folderCnt))
            os.chdir(str(folderCnt))
            folderCnt += 1
        workCnt += 1
        # 提示信息头
        print('Deal with: ', work['title'])
        print(work['SHA1'][-9:-1]+'\t', workCnt, 'of', len(workDic))
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        # 下载该作品
        res = downWork(work)
        if res is None:
            failCnt.append(work['SHA1'])
        # 分割线
        print('--------------------------------------------' +
              '--------------------------------------------' +
              '--------------------------------------------')
        # 延时
        time.sleep(randint(5, 10))
    # 全部下载完毕， 提示信息
    print('All work finish!')
    print('Faild work:')
    pprint(failCnt)
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    # 重置工作区
    os.chdir(inPath)


# 主函数
# 注意： 调用该函数会在当前目录建立新的工作目录 workPath
# 所有文件均保存在新建的工作目录下
def main():
    # 获取搜索参数
    print('设置搜索参数：')
    params = getParam()
    # 获取起止页
    startPage = int(input('起始页（从0开始）：'))
    endPage = int(input('终止页:'))
    while startPage > endPage or startPage < 0 or endPage < 0:
        print('输入错误！')
        print('请重新输入!')
        startPage = int(input('起始页:'))
        endPage = int(input('终止页:'))
    # 根据输入参数创建文件夹
    global workPath
    cwPath = os.getcwd()
    workPath = str(params['f_cats']) + str(params['f_search']) +\
        '-P'+str(startPage)+'-to'+'-P'+str(endPage)+'-' +\
        time.strftime('%m-%d-%y', time.localtime())
    workPath = os.path.join(cwPath, workPath)
    try:
        os.makedirs(workPath)
    except FileExistsError:
        print('Folder already exists!')
    os.chdir(workPath)
    # 分割线
    print('--------------------------------------------' +
          '--------------------------------------------' +
          '--------------------------------------------')
    # 下载并保存范围内页面
    print('下载搜索结果页:')
    mainUrl = 'https://e-hentai.org'
    htmlFolder = getSearch(url=mainUrl, params=params,
                           startPage=startPage, endPage=endPage)
    # 分割线
    print('--------------------------------------------' +
          '--------------------------------------------' +
          '--------------------------------------------')
    # 从搜索页html中提取每一件work的入口url, 保存在字典中
    print('提取入口url:')
    getWorkUrl(htmlFolder)
    # 分割线
    print('--------------------------------------------' +
          '--------------------------------------------' +
          '--------------------------------------------')
    # 批量下载所有的work
    print('批量下载：')
    downWorkS()


# 测试
if __name__ == '__main__':
    main()
