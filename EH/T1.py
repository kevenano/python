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
    print('下载完成！')
    # 重置工作目录
    os.chdir(inPath)
    return folderPath


# 从html中提取每一件的url
# 输入参数 html所在的文件夹
def getWorkUrl(htmlFolder):
    # 记录入口工作目录
    inPath = os.getcwd()
    # 将当前工作目录移入htmlFolder
    os.chdir(htmlFolder)

    # 循环处理每一页
    # 获取title 和 url
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
            workDic[str(workCnt)] = copy.copy(tempDic)
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

# 主函数


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


# 测试
if __name__ == '__main__':
    os.chdir('/home/kevenano/Pictures/EH')
    main()
