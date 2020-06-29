"""
图片检索算法 测试
感知哈希算法pHash 差值哈希算法dhash
"""
import cv2
import numpy as np
from CLASS_DB import DB
import os
import math
from tqdm import tqdm
import time
import shelve
import threading
from pprint import pprint

# 载入数据
dataFilePath = r"D:\konachan\hashData\hashData"
dataFile = shelve.open(dataFilePath)
datas = dataFile["datas"]
dataFile.close()
# 查询结果
cmpResult = []

# 多线程锁
lock = threading.Lock()


# 感知哈希
def pHash(image, s):
    if s < 2:
        s = 2
    s = math.floor(s)
    image = cv2.resize(image, (s, s), interpolation=cv2.INTER_CUBIC)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #     cv2.imshow('image', image)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()
    # 将灰度图转为浮点型，再进行dct变换
    dct = cv2.dct(np.float32(image))
    #     print(dct)
    # 取左上角的8*8，这些代表图片的最低频率
    # 这个操作等价于c++中利用opencv实现的掩码操作
    # 在python中进行掩码操作，可以直接这样取出图像矩阵的某一部分
    dct_roi = dct[0: math.floor(s / 2), 0: math.floor(s / 2)]
    avreage = np.mean(dct_roi)
    hash = []
    for i in range(dct_roi.shape[0]):
        for j in range(dct_roi.shape[1]):
            if dct_roi[i, j] > avreage:
                hash.append(1)
            else:
                hash.append(0)
    return hash


# 差值哈希
def dHash(image, s):
    if s < 2:
        s = 2
    s = math.floor(s)
    # 缩放9*8
    image = cv2.resize(image, (s + 1, s), interpolation=cv2.INTER_CUBIC)
    # 转换灰度图
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #     print(image.shape)
    hash = []
    # 每行前一个像素大于后一个像素为1，相反为0，生成哈希
    for i in range(s):
        for j in range(s):
            if image[i, j] > image[i, j + 1]:
                hash.append(1)
            else:
                hash.append(0)
    return hash


# 计算汉明距离
def Hamming_distance(hash1, hash2):
    num = 0
    for index in range(len(hash1)):
        if str(hash1[index]) != str(hash2[index]):
            num += 1
    return num


def getData(dataFilePath):
    # 链接到数据库
    # db = DB("localhost", "root", "qo4hr[Pxm7W5", "konachan")
    db = DB("localhost", "kevenano", "qhm2012@@@", "konachan")
    db.connect()
    # t1 = time.time()
    sql = r"SELECT id,pHash,dHash from mark WHERE mark.pHash IS NOT NULL;"
    flag = db.execute(sql)
    if flag != 1:
        db.close()
        print("SQL error!")
        exit()
    datas = db.fetchall()
    # 断开数据库
    db.close()
    dataFile = shelve.open(dataFilePath)
    dataFile["datas"] = datas
    dataFile.close()
    # t2 = time.time()
    # print("SQL time: ", t2-t1)


def cmpData(inPHash, inDHash, dataList):
    global cmpResult
    results = []
    for item in dataList:
        result = [0, 0, 0, 0, 0]
        result[0] = item[0]
        result[1] = Hamming_distance(inPHash, item[1])
        result[2] = Hamming_distance(inDHash, item[2])
        result[3] = 1 - result[1] / len(inPHash)
        result[4] = 1 - result[2] / len(inDHash)
        results.append(result)
    if lock.acquire():
        for item in results:
            cmpResult.append(item)
        lock.release()


def main():
    image_file1 = r"D:\konachan\thumbnail\thumb-308277.jpg"
    # image_file1 = r"C:\Users\keven\OneDrive\_Work\Code\Python\konachan\ImageSearch\T1.png"
    image_file2 = r"D:\konachan\thumbnail\thumb-308289.jpg"
    # image_file2 = r"C:\Users\keven\OneDrive\_Work\Code\Python\konachan\ImageSearch\T2.png"
    img1 = cv2.imread(image_file1)
    img2 = cv2.imread(image_file2)
    hash1 = pHash(img1)
    hash2 = pHash(img2)
    dist = Hamming_distance(hash1, hash2)
    # 将距离转化为相似度
    similarity = 1 - dist * 1.0 / (16 * 16)
    print(dist)
    print(similarity)
    # print(hash1)
    # print(hash2)


def main2():
    # 链接到数据库
    # db = DB("localhost", "root", "qo4hr[Pxm7W5", "konachan")
    db = DB("localhost", "kevenano", "qhm2012@@@", "konachan")
    db.connect()
    # 循环处理
    imageDir = r"D:\konachan\thumbnail"
    imageNames = os.listdir(imageDir)
    pbar = tqdm(imageNames, ncols=100)
    cnt = 0
    for imageName in pbar:
        cnt += 1
        pbar.set_description(f"{cnt} of {len(imageNames)}")
        imageID = imageName[6:-4]
        imagePath = os.path.join(imageDir, imageName)
        image = cv2.imread(imagePath)
        imagePHash = "".join(list(map(str, pHash(image, 16))))
        imageDHash = "".join(list(map(str, dHash(image, 8))))
        db.update("mark", "pHash", imagePHash, f"WHERE id={imageID}")
        db.update("mark", "dHash", imageDHash, f"WHERE id={imageID}")
    # 断开数据库
    db.close()


def test():
    global cmpResult
    # 输入图片
    inImage = r"C:\Users\keven\OneDrive\_Work\Code\Python\konachan\ImageSearch\T5.png"
    inImage = cv2.imread(inImage)
    inPHash = pHash(inImage, 16)
    inDHash = dHash(inImage, 8)
    """ 遍历 """
    t1 = time.time()
    # 单线程方法
    # for item in datas:
    #     result = [0, 0, 0]
    #     result[0] = item[0]
    #     result[1] = Hamming_distance(inPHash, item[1])
    #     result[2] = Hamming_distance(inDHash, item[2])
    #     results.append(result)
    # 多线程方法
    itemCnt = 0
    threadNum = 8
    itemPerThread = math.floor(len(datas) / threadNum)
    thList = []
    while itemCnt < len(datas):
        # 创建多线程任务
        if itemPerThread > len(datas) - itemCnt:
            itemPerThread = len(datas) - itemCnt
        wkThread = threading.Thread(
            target=cmpData,
            args=(inPHash, inDHash, datas[itemCnt: itemCnt + itemPerThread]),
        )
        thList.append(wkThread)
        # wkThread.start()
        itemCnt += itemPerThread
    # 启动线程
    for thread in thList:
        thread.start()
    # 等待线程结束
    for thread in thList:
        thread.join()
    t2 = time.time()
    print("Main process: ", t2 - t1)
    cmpResult.sort(key=lambda s: s[-1], reverse=True)
    pprint(cmpResult[0:10])
    cmpResult.sort(key=lambda s: s[-2], reverse=True)
    pprint(cmpResult[0:10])
    cmpResult.sort(key=lambda s: 2*s[-2]-(1-s[-1]), reverse=True)
    pprint(cmpResult[0:10])


if __name__ == "__main__":
    test()
