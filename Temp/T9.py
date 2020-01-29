# beautifulsoup
# 一键打开多个搜索页
import requests
import bs4
import sys
import webbrowser
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Input check
if len(sys.argv) > 1:
    searchObject = sys.argv[1:]
else:
    print('Usage: pthon3 T9.py searchObject')
    exit()

# Searching
print('Searching...')
# URL构成
url = 'https://cn.bing.com' + '/search?q=' + \
    ''.join(searchObject) + '&ensearch=0'
logging.debug('\n\tURL:'+url)
# 获取搜索页
res = requests.get(url)
res.raise_for_status()
logging.debug('\n\t'+str(len(res.text)))
resSoup = bs4.BeautifulSoup(res.text, features="lxml")
# 定位地址元素
linkElems = resSoup.select('cite')
# 提取全部地址
links = []
for i in range(len(linkElems)):
    links.append(linkElems[i].getText())
# 设置一次性打开的数量
numOpen = min(5, len(linkElems))
for i in range(numOpen):
    webbrowser.open(links[i])
