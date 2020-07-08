from elasticsearch import Elasticsearch
from elasticsearch_driver import SignatureES
from pprint import pprint


def main():
    es = Elasticsearch()
    ses = SignatureES(es)
    img_path = r"C:\Users\keven\OneDrive\_Work\Code\Python\konachan\ImageSearch\T6.png"
    res = ses.search_image(img_path)
    pprint(res)


if __name__ == "__main__":
    main()
