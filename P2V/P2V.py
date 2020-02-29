import os
import cv2
import time
from pprint import pprint
import sys


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
def pic2video(folderPath, videoFPS, width, height):
    fileList = os.listdir(folderPath)
    fileList.sort()

    videoPath = os.path.join(folderPath, str(int(time.time()))+'.mp4')
    fourcc = cv2.VideoWriter_fourcc(*"avc1")
    frameSize = (width, height)
    video = cv2.VideoWriter(filename=videoPath, fourcc=fourcc,
                            fps=videoFPS, frameSize=frameSize)

    failList = []
    for item in fileList:
        if item.endswith(('png', 'jpg', 'bmp', 'jpeg')):
            print('Deal with', item)
            itemPath = os.path.join(folderPath, item)
            img = cv2.imread(itemPath)
            if img is None:
                print('Fail to open the image!')
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


if __name__ == '__main__':
    run()
