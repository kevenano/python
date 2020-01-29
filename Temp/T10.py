# 批量下载 秋空 fail
import requests
import bs4
# import webbrowser
# import pprint
# import sys
# import os
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# TODO: Download html
headers = {
    'user-agent':
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) ' +
    'Gecko/20100101 Firefox/72.0'
}
print('Downloading...')
mainUrl = 'http://www.90mh.com/manhua/qiusezhikong/41481.html'
mainHtml = requests.get(url=mainUrl, headers=headers)
mainHtml.raise_for_status()
logging.DEBUG('\n\tHtml size: '+str(len(mainHtml.text)))

# TODO: Get img url
mainSoup = bs4.BeautifulSoup(mainHtml.text, features='lxml')
linkElems = mainSoup.select

# TODO: Save img
