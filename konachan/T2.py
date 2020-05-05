# konachan批量下载 利用API
import requests
import json
import time
import os
from random import randint

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


if __name__ == '__main__':
    # 记录时间 创建工作目录
    startTime = time.time()
    taskId = int(startTime)
    taskPath = os.path.join(os.getcwd(), str(taskId))
    os.mkdir(taskPath)
    jsonPath = os.path.join(taskPath, 'json')
    os.mkdir(jsonPath)
    picPath = os.path.join(taskPath, 'picture')
    os.mkdir(picPath)
    sumPath = os.path.join(taskPath, 'summary.txt')

    # 获取搜索参数
    params = {}
    tags = input('Tags:\n')
    startPage = int(input('Start Page:\n'))
    maxPage = int(input('maxPage:\n'))
    if startPage < 1:
        startPage = 1
    if maxPage < 1:
        maxPage = 1
    url = 'https://konachan.com/post.json'
    params['page'] = startPage
    params['tags'] = tags

    # 初始化相关参数
    picCnt = 0
    pageCnt = 0
    failList = []
    # 循环下载所有页面
    while True:
        # 下载并保存json
        print('Deal with page: ', params['page'])
        page = download(url=url, params=params)
        if page is None or len(page) == 0 or pageCnt == maxPage:
            break
        # 保存json
        pageCnt += 1
        tmpPath = os.path.join(jsonPath, str(pageCnt)+'.json')
        pageFile = open(tmpPath, 'w', encoding='utf-8')
        pageFile.write(page)
        pageFile.close()
        del(tmpPath)
        # json转python
        data = json.loads(page)
        # 循环下载当前页面的文件
        for item in data:
            picCnt += 1
            pic_id = item['id']
            pic_url = item['file_url']
            print('Picture count: ', picCnt, 'ID: ', pic_id)
            rawFile = download(url=pic_url, raw=1, timeout=300)
            if rawFile is None:
                failList.append(pic_id)
                print()
                continue
            tmpPath = os.path.join(picPath, str(pic_id)+pic_url[-4:])
            picFile = open(tmpPath, 'wb')
            for chunk in rawFile.iter_content(100000):
                picFile.write(chunk)
            picFile.close()
            del(tmpPath)
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
            print()
            time.sleep(randint(3, 5))
        # 延时并更新参数
        time.sleep(randint(10, 15))
        params['page'] += 1
        print()

    endTime = time.time()
    spendTime = int(endTime-startTime)
    # 生成任务摘要
    sumFile = open(sumPath, 'w')
    sumFile.write('Task ID:\n')
    sumFile.write(str(taskId)+'\n')
    sumFile.write('Tags:\n')
    sumFile.write(params['tags']+'\n')
    sumFile.write('Pages:\n')
    sumFile.write(str(startPage)+'-'+str(startPage+pageCnt-1)+'\n')
    sumFile.write('Work Count:\n')
    sumFile.write(str(picCnt)+'\n')
    sumFile.write('Failed Count:\n')
    sumFile.write(str(len(failList))+'\n')
    sumFile.write('Faild List:\n')
    sumFile.write(str(failList).replace(',', '\n')+'\n')
    sumFile.write('Start Time:\n')
    sumFile.write(time.strftime('%Y-%m-%d %H:%M:%S',
                                time.localtime(startTime))+'\n')
    sumFile.write('End Time:\n')
    sumFile.write(time.strftime('%Y-%m-%d %H:%M:%S',
                                time.localtime(endTime))+'\n')
    sumFile.write('Time Cost:\n')
    sumFile.write(str(spendTime//3600)+'h')
    sumFile.write(str((spendTime % 3600)//60)+'m')
    sumFile.write(str(spendTime % 60)+'s'+'\n')
    sumFile.close()
    print('All finish!')
