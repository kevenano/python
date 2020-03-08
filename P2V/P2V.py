import os
import cv2
import sys
from tqdm import tqdm
import threading
import time
import numpy as np
# from PIL import Image


# 解决cv2.imread不兼容中文路径的问题
def cv_imgread(filePath):
    cv_img = cv2.imdecode(np.fromfile(filePath, dtype=np.uint8), 1)
    '''
    cv_img = cv2.imread(filePath)
    '''
    return cv_img


# 判断是否为支持的图片格式（后缀名方法）
def isPicture(itemName):
    sufixList = ('png', 'jpg', 'bmp', 'jpeg')
    if itemName.lower().endswith(sufixList):
        return True
    else:
        return False


# 字符串长度规范化
def modiStr(mes, length):
    mesLen = len(mes)
    if mesLen < length:
        return mes+' '*(length-mesLen)
    elif mesLen > length:
        return mes[0:length-2]+'..'
    else:
        return mes


# 修改图片大小（加黑边）
def imgResize(image, width, height, color=[0, 0, 0]):
    top, bottom, left, right = (0, 0, 0, 0)

    # 获取图像尺寸
    h = image.shape[0]
    w = image.shape[1]

    # 计算需要添加的像素的大小
    if (w/h) < (width/height):
        dw = round((width/height) * h - w)
        left = dw // 2
        right = dw - left
    elif (w/h) > (width/height):
        dh = round((height/width) * w - h)
        top = dh // 2
        bottom = dh - top
    else:
        pass

    # 给图像加边界， 使图像比例符合给定比例， cv2.BORDER_CONSTANT指定边界颜色由value指定
    constant = cv2.copyMakeBorder(
        image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)

    # 调整图像大小并返回
    return cv2.resize(constant, (width, height))


# 图片合成视频
def pic2video(outPath, itemList, videoFPS, width, height, noBar=False):
    videoPath = outPath+'.mp4'
    fourcc = cv2.VideoWriter_fourcc(*"avc1")
    frameSize = (width, height)
    video = cv2.VideoWriter(filename=videoPath, fourcc=fourcc,
                            fps=videoFPS, frameSize=frameSize)
    failList = []
    if noBar is False:
        pbar = tqdm(itemList, ncols=100)
        for item in pbar:
            # 显示进度条
            pbar.set_description("Processing %s" %
                                 modiStr(os.path.split(item)[-1], 20))
            img = cv_imgread(item)
            if img is None:
                failList.append(item)
                continue
            imgRe = imgResize(img, width, height)
            video.write(imgRe)
    else:
        for item in itemList:
            img = cv_imgread(item)
            if img is None:
                failList.append(item)
                continue
            imgRe = imgResize(img, width, height)
            video.write(imgRe)
    video.release()
    return failList, videoPath


# 单目录处理
def singleProcess(folderPath, videoFPS=2, noBar=False):
    if os.path.isdir(folderPath) is False:
        return 'Not a folder!'
    # 遍历目录树，获取文件列表
    itemList = []
    for folderName, _, filenames in os.walk(folderPath):
        for file in filenames:
            if isPicture(file):
                itemList.append(os.path.join(folderName, file))
    itemList.sort()
    # 若符合条件的图片少于5张 返回
    if len(itemList) < 5:
        return 'Too little picture!'
    # 获取第二张图片的尺寸，作为视频尺寸<------------------------------------------------有待改进
    mItem = itemList[1]
    mItemPath = os.path.join(folderPath, mItem)
    mImg = cv_imgread(mItemPath)
    width = mImg.shape[1]
    height = mImg.shape[0]
    failList, videoPath = pic2video(
        folderPath, itemList, videoFPS, width, height, noBar)
    return 1


# 多目录批处理函数 多线程处理目标函数
def batchPlus(folderList, videoFPS=2, noBar=True):
    pbar = tqdm(folderList, ncols=100)
    for folder in pbar:
        # 显示进度条
        pbar.set_description("Processing %s" %
                             modiStr(os.path.split(folder)[-1], 20))
        # 处理item文件夹
        singleProcess(folder, videoFPS, noBar)


# 多线程处理主函数 threading方法
def batchMain(mainFolder, videoFPS=2, threads=2):
    # 单线程显示子进度条，否则只显示主进度条
    if threads == 1:
        noBar = False
    else:
        noBar = True
    # 创建文件夹列表
    folderList = os.listdir(mainFolder)
    tempList = []
    for folder in folderList:
        folderPath = os.path.join(mainFolder, folder)
        if os.path.isdir(folderPath):
            tempList.append(folderPath)
    folderList = tempList
    del tempList
    # 建立多线程任务
    processingThreads = []
    tasks = len(folderList)//threads + 1
    # 根据线程分配任务
    for i in range(0, len(folderList), tasks):
        processingList = folderList[i:i+tasks]
        processingThread = threading.Thread(
            target=batchPlus, args=(
                processingList, videoFPS, noBar))
        processingThreads.append(processingThread)
        processingThread.start()
    # 等待任务结束
    for processingThread in processingThreads:
        processingThread.join()
    print('\n'*(threads - 1))


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print(
            'Usage: python3 P2V.py [batchFlag] [mainFolder] [fps] [threads]')
        exit()
    batchFlag = int(sys.argv[1])
    mainFolder = sys.argv[2]
    videoFPS = int(sys.argv[3])
    threads = int(sys.argv[4])
    if threads > 5:
        threads = 5
    if threads < 1:
        threads = 1
    startTime = time.time()
    if batchFlag == 1:
        batchMain(mainFolder, videoFPS, threads)
    elif batchFlag == 0:
        singleProcess(mainFolder, videoFPS)
    else:
        print('[batchFlag] = 1 for multifolder process')
        print('[batchFlag] = 0 for singlefolder process')
        exit()
    endTime = time.time()
    print('Done!')
    print('Time cost:', str(endTime-startTime))
    '''
    mainFolder = '/mnt/hgfs/D/t'
    singleProcess(mainFolder)
    '''
