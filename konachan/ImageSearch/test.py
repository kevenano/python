from elasticsearch import Elasticsearch
from image_match.elasticsearch_driver import SignatureES
from tqdm import tqdm
import os
from pprint import pprint
# import cv2


def imgStoreTest():
    es = Elasticsearch()
    ses = SignatureES(es)
    # 循环处理
    imageDir = r"D:\konachan\thumbnail"
    imageNames = os.listdir(imageDir)
    pbar = tqdm(imageNames[152940:], ncols=100)
    cnt = 0
    for imageName in pbar:
        cnt += 1
        pbar.set_description(f"{cnt} of {len(imageNames)}")
        imagePath = os.path.join(imageDir, imageName)
        # image = cv2.imread(imagePath)
        ses.add_image(path=imagePath)


def imgSearchTest():
    es = Elasticsearch()
    ses = SignatureES(es)
    img_path = r"C:\Users\keven\OneDrive\_Work\Code\Python\konachan\ImageSearch\T6.png"
    res = ses.search_image(img_path)
    pprint(res)


if __name__ == "__main__":
    # imgStoreTest()
    imgSearchTest()
