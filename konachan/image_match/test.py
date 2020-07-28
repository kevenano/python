from elasticsearch import Elasticsearch
from elasticsearch_driver import SignatureES
from pprint import pprint
import os


def main():
    es = Elasticsearch()
    ses = SignatureES(es)
    img_path = r"C:\Users\keven\OneDrive\_Work\Code\Python\konachan\ImageSearch\T6.png"
    res = ses.search_image(img_path)
    pprint(res)


def imgStoreTest():
    es = Elasticsearch()
    ses = SignatureES(es)
    imagePath = r"D:\konachan\thumbnail\thumb-311479.jpg"
    imageID = int(os.path.basename(imagePath).split(".")[0][6:])
    # pbar.set_description(f"Deal with {imageID}")
    # image = cv2.imread(imagePath)
    metadata = {"imageID": imageID}
    ses.add_image(path=imagePath, metadata=metadata)


if __name__ == "__main__":
    imgStoreTest()
