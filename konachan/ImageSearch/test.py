from elasticsearch import Elasticsearch
from image_match.elasticsearch_driver import SignatureES
from tqdm import tqdm
import os
from pprint import pprint
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
# import cv2


def storeImage(inDir):
    es = Elasticsearch()
    ses = SignatureES(es)
    # 获取文件列表
    fileList = []
    for folderName, subfolders, fileNames in os.walk(inDir):
        for fileName in fileNames:
            if fileName.endswith(("jpg", "png", "jpeg", "gif")):
                fileList.append(os.path.join(folderName, fileName))
    # 循环处理
    pbar = tqdm(fileList[240119:], ncols=100)
    cnt = 0
    for imagePath in pbar:
        cnt += 1
        # imageID = int(os.path.basename(imagePath).split(".")[0])
        imageID = int(os.path.basename(imagePath).split(".")[0][6:])
        pbar.set_description(f"Deal with {imageID}")
        # image = cv2.imread(imagePath)
        metadata = {"imageID": imageID}
        ses.add_image(path=imagePath, metadata=metadata)


def imgSearchTest():
    es = Elasticsearch()
    ses = SignatureES(es)
    img_path = r"C:\Users\keven\OneDrive\_Work\Code\Python\konachan\ImageSearch\T6.png"
    res = ses.search_image(img_path)
    pprint(res)


if __name__ == "__main__":
    inDir = r"D:\konachan\thumbnail"
    storeImage(inDir)
