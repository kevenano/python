# EOP 批量采集
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


# 从html中提取每一件的url
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
    print('url title 保存在dicFile中workDic中')
    # 重置工作目录
    os.chdir(inPath)


# 根据 deWork 获取当前作品的所有图片的下载链接
# deWork 是包括 title 和 url 的字典
# 成功返回下载链接列表
# 失败返回空列表
def getPicUrl(deWork):
    # 创建列表 保存作品的picUrl
    picUrl = []
    # 下载详情页
    deUrl = deWork['url']
    dePage = download(url=deUrl)
    if dePage is None:
        print('Fail to download detail page!')
        return picUrl
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
        picUrl.append(curPicUrl)
        # 页间延迟
        time.sleep(randint(1, 3))
    # 返回下载链接列表
    return picUrl


# 批量获取全部picUrl
# 保存在picUrl中picUrlDic中
# 以title SHA1 的后8位为key, url为value
def getPicUrlS():
    # 打开dicFile
    dicFile = shelve.open('dicFile')
    workDic = dicFile['workDic']
    dicFile.close()
    # 循环处理workDic中的全部项
    picUrlDic = {}
    cnt = 1
    for deWork in workDic.values():
        # 提示头
        print('Deal with: ', deWork['title'])
        print(cnt, 'of', len(workDic))
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        urlList = getPicUrl(deWork)
        workSHA1 = sha1(deWork['title'].encode(encoding='UTF-8')).hexdigest()
        picUrlDic[workSHA1[-9:-1]] = urlList
        # 一件作品完成提示
        print('Finish!')
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        print('--------------------------------------------' +
              '--------------------------------------------' +
              '--------------------------------------------')
        cnt += 1
        time.sleep(randint(1, 5))
    # 保存picUrlDic
    picUrl = shelve.open('picUrl')
    picUrl['picUrlDic'] = picUrlDic
    picUrl.close()
    # 提示信息
    print('图片下载链接提取完毕！')
    print('保存在picUrl中')


# 根据picUrl下载图片
def downWork():
    # 记录入口工作目录
    inPath = os.getcwd()
    # 打开picUrl
    picUrl = shelve.open('picUrl')
    picUrlDic = picUrl['picUrlDic']
    picUrl.close()
    # 创建mainFolder保存works
    try:
        os.makedirs('mainFolder')
    except FileExistsError:
        print('MainFolder already exist!')
    os.chdir('mainFolder')
    mainPath = os.getcwd()
    # 以25件work为单位， 创建子文件夹
    cnt = 0
    for workId, workUrls in picUrlDic.items():
        # 提示信息头
        print('Deal with ', workId)
        print(cnt+1, 'of', len(picUrlDic))
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        # 25
        if cnt % 25 == 0:
            os.chdir(mainPath)
            os.makedirs(str(cnt+1))
            os.chdir(str(cnt+1))
        for url in workUrls:
            rawPic = download(url=url, raw=1, timeout=60)
            if rawPic is None:
                print('**')
                continue
            picFile = open(os.path.basename(url), 'wb')
            for chunk in rawPic.iter_content(100000):
                picFile.write(chunk)
            picFile.close()
        # 计数更新
        cnt += 1
        # 分割线
        print('--------------------------------------------' +
              '--------------------------------------------' +
              '--------------------------------------------')
    # 全部下载完毕， 提示信息
    print('All work finish!')
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    # 重置工作区
    os.chdir(inPath)


# 主函数
# 注意： 调用该函数会在当前目录建立新的工作目录 workPath
# 所有文件均保存在新建的工作目录下
def main():
    # 获取搜索参数
    params = getParam()
    # 根据输入参数创建文件夹
    global workPath
    cwPath = os.getcwd()
    workPath = str(params['f_cats']) + str(params['f_search']) +\
        time.strftime('%m-%d-%y', time.localtime())
    workPath = os.path.join(cwPath, workPath)
    try:
        os.makedirs(workPath)
    except FileExistsError:
        print('Folder already exists!')
    os.chdir(workPath)
    # 获取起止页
    startPage = int(input('起始页（从0开始）：'))
    endPage = int(input('终止页:'))
    while startPage > endPage or startPage < 0 or endPage < 0:
        print('输入错误！')
        print('请重新输入!')
        startPage = int(input('起始页:'))
        endPage = int(input('终止页:'))
    # 下载并保存范围内页面
    mainUrl = 'https://e-hentai.org'
    htmlFolder = getSearch(url=mainUrl, params=params,
                           startPage=startPage, endPage=endPage)
    # 从html中提取每一件的url, 保存在字典中
    getWorkUrl(htmlFolder)
    # 批量获取全部picUrl, 保存在字典中
    getPicUrlS()
    # 根据picUrl字典下载图片
    downWork()


# 测试
if __name__ == '__main__':
    main()
