import os
import cv2
from pprint import pprint
import sys
from tqdm import tqdm
import threading
import time
import numpy as np


# 解决cv2.imread不兼容中文路径的问题
def cv_imgread(filePath):
    cv_img = cv2.imdecode(np.fromfile(filePath, dtype=np.uint8), -1)
    return cv_img


# 修改图片大小（加黑边）
def imgResize(image, width, height, color=[0, 0, 0]):
    top, bottom, left, right = (0, 0, 0, 0)

    # 获取图像尺寸
    h, w, _ = image.shape

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
def pic2video(folderPath, videoFPS, width, height, noBar=False):
    fileList = os.listdir(folderPath)
    fileList.sort()

    videoPath = os.path.join(os.path.split(folderPath)[
                             0], os.path.split(folderPath)[1]+'.mp4')
    fourcc = cv2.VideoWriter_fourcc(*"avc1")
    frameSize = (width, height)
    video = cv2.VideoWriter(filename=videoPath, fourcc=fourcc,
                            fps=videoFPS, frameSize=frameSize)

    failList = []
    if noBar is False:
        pbar = tqdm(fileList)
        for item in pbar:
            if item.endswith(('png', 'jpg', 'bmp', 'jpeg')):
                # 显示进度条
                pbar.set_description("Processing %s" % item)
                itemPath = os.path.join(folderPath, item)
                img = cv_imgread(itemPath)
                if img is None:
                    failList.append(item)
                    continue
                imgRe = imgResize(img, width, height)
                video.write(imgRe)
    else:
        for item in fileList:
            if item.endswith(('png', 'jpg', 'bmp', 'jpeg')):
                itemPath = os.path.join(folderPath, item)
                img = cv_imgread(itemPath)
                if img is None:
                    failList.append(item)
                    continue
                imgRe = imgResize(img, width, height)
                video.write(imgRe)
    video.release()
    return failList, videoPath


def run():
    if len(sys.argv) < 5:
        print('Usage: python3 P2V.py [folder] [fps] [width] [height]')
        exit()
    folderPath = sys.argv[1]
    videoFPS = int(sys.argv[2])
    width = int(sys.argv[3])
    height = int(sys.argv[4])
    failList, videoPath = pic2video(folderPath, videoFPS, width, height)
    if len(failList) > 0:
        print('Fiald list:')
        pprint(failList)
    print('Output path:')
    print(videoPath)
    print('Done!')


# 默认处理当前目录下
def batch(mainFolder=os.getcwd(), videoFPS=2):
    folderList = os.listdir(mainFolder)
    pbar = tqdm(folderList)
    for item in pbar:
        # 显示进度条
        pbar.set_description("Processing %s" % item)
        folderPath = os.path.join(mainFolder, item)
        # 获取第二张图片的尺寸，作为视频尺寸
        try:
            itemList = os.listdir(folderPath)
        except NotADirectoryError:
            continue
        itemList.sort()
        mItem = itemList[1]
        mImg = cv_imgread(os.path.join(folderPath, mItem))
        width = mImg.shape[1]
        height = mImg.shape[0]
        # 图片合成视频
        failList, videoPath = pic2video(folderPath, videoFPS, width, height)


# 多线程处理目标函数
def batchPlus(mainFolder, folderList, videoFPS=2, noBar=True):
    pbar = tqdm(folderList)
    for item in pbar:
        # 显示进度条
        pbar.set_description("Processing %s" % item)
        folderPath = os.path.join(mainFolder, item)
        # 获取第二张图片的尺寸，作为视频尺寸
        try:
            itemList = os.listdir(folderPath)
        except NotADirectoryError:
            continue
        itemList.sort()
        mItem = itemList[1]
        mItemPath = os.path.join(folderPath, mItem)
        mImg = cv_imgread(mItemPath)
        width = mImg.shape[1]
        height = mImg.shape[0]
        # 图片合成视频
        failList, videoPath = pic2video(
            folderPath, videoFPS, width, height, noBar=noBar)


# 多线程测试 threading方法
def batchTest(mainFolder=os.getcwd(), videoFPS=2, threads=3):
    # 单线程显示子进度条，否则只显示主进度条
    if threads == 1:
        noBar = False
    else:
        noBar = True
    # 创建文件夹列表
    folderList = os.listdir(mainFolder)
    processingThreads = []
    tasks = len(folderList)//threads + 1
    # 根据线程分配任务
    for i in range(0, len(folderList), tasks):
        processingList = folderList[i:i+tasks]
        processingThread = threading.Thread(
            target=batchPlus, args=(mainFolder, processingList, videoFPS, noBar))
        processingThreads.append(processingThread)
    # 开启任务
    for processingThread in processingThreads:
        processingThread.start()
    # 等待任务结束
    for processingThread in processingThreads:
        processingThread.join()
    print('\n'*(threads))
    print('Done.')


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python3 P2V.py [mainFolder] [fps] [threads]')
        exit()
    mainFolder = sys.argv[1]
    videoFPS = int(sys.argv[2])
    threads = int(sys.argv[3])
    if threads > 5:
        threads = 5

    startTime = time.time()
    batchTest(mainFolder, videoFPS, threads)
    endTime = time.time()
    print('Time cost:', str(endTime-startTime))
    '''
    mainFolder = "D:\\s"
    batchTest(mainFolder, 2, 1)
    '''