import requests
import my_fake_useragent as mfua


# Html download function
# 输入参数reFlag = 0 返回text, 1 返回content, 2 返回resp
# 如下载错误，将返回resp=None
def download(
    url, num_retries=3, headers={}, cookie="", params="", reFlag=0, timeout=(30, 300),
):
    # print("Downloading: ", url)
    if "user-agent" not in headers:
        headers["user-agent"] = mfua.UserAgent().random()
    if cookie != "":
        headers["cookie"] = cookie
    resp = None
    try:
        resp = requests.get(url, headers=headers,
                            params=params, timeout=timeout)
        resp.close()
        html = resp.text
        content = resp.content
        if resp.status_code >= 400:
            print("Download error: ", resp.text)
            html = None
            content = None
            if num_retries and 500 <= resp.status_code < 600:
                return download(url, num_retries - 1)
    except requests.exceptions.RequestException as e:
        print("Download error!!!")
        print(e)
        html = None
        content = None
        resp = None
    except requests.exceptions.Timeout:
        print("请求超时!")
        html = None
        content = None
    if reFlag == 0:
        return html
    elif reFlag == 1:
        return content
    else:
        return resp