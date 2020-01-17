# 下载网页
import urllib.request
from urllib.error import URLError, HTTPError, ContentTooShortError


def download(url, user_agent='wswp', num_retries=2):
    print('Downloading:', url)
    request = urllib.request.Request(url)
    request.add_header('User-agent', user_agent)
    try:
        html = urllib.request.urlopen(url).read()
    except (URLError, HTTPError, ContentTooShortError) as e:
        print('Download error:', e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                return download(url, num_retries - 1)
    return html


def test():
    # h1 = download('http://example.python-scraping.com/places/default/index')
    # h2 = download('http://httpstat.us/500')
    h3 = download('https://meetup.com', 'kk')
    return h3
    print(h3)


if __name__ == '__main__':
    a1 = test()
