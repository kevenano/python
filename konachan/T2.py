# 尝试多线程
import threading
import requests
import os
import time


# Html download function
# 输入参数reFlag = 0 返回text, 1 返回content, 2 返回resp
# 若下载失败， 一律返回None
def download(
    url,
    num_retries=3,
    headers={},
    cookie="",
    params="",
    stream=None,
    reFlag=0,
    timeout=(30, 300),
):
    # print("Downloading: ", url)
    if "user-agent" not in headers:
        headers[
            "user-agent"
        ] = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0"
    if cookie != "":
        headers["cookie"] = cookie
    try:
        resp = requests.get(
            url, headers=headers, params=params, stream=stream, timeout=timeout
        )
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
        resp = None
    if reFlag == 0:
        return html
    elif reFlag == 1:
        return content
    else:
        return resp


def downThread(url, start, end, threadNum, mainPath, fileName=None):
    print("线程", threadNum, "正在下载")
    if fileName is None:
        fileName = os.path.basename(url)
    headers = {"Range": f"bytes={start}-{end}", "connection": "close"}
    dtTime = int((end - start) * 100 / (1024 * 1024))
    if dtTime < 60:
        dtTime = 60
    if dtTime > 600:
        dtTime = 600
    content = download(url=url, headers=headers, reFlag=1, timeout=(30, dtTime))
    if content is None:
        print("线程", threadNum, "下载失败")
    else:
        tempPath = os.path.join(mainPath, "temp_" + str(threadNum) + "_" + fileName)
        tempFile = open(tempPath, "wb")
        tempFile.write(content)
        tempFile.close()
        print("线程", threadNum, "下载完成")


def main(url, threadCnt, mainPath, fileName):
    startTime = time.time()
    filePath = os.path.join(mainPath, fileName)
    res = requests.head(url=url)
    try:
        fileSize = int(res.headers["Content-Length"])
    except Exception as e:
        print(e)
        print("检查url或不支持多线程")
        return e

    thList = []
    part = fileSize // threadCnt
    for i in range(threadCnt):
        start = i * part
        if i == threadCnt:
            end = fileSize - 1
        else:
            end = start + part - 1
        dlThread = threading.Thread(
            target=downThread,
            args=(url, start, end, i, mainPath),
            kwargs={"fileName": fileName},
        )
        thList.append(dlThread)
        dlThread.start()
        time.sleep(1)

    for item in thList:
        item.join()

    tempList = [
        os.path.join(mainPath, fn)
        for fn in os.listdir(mainPath)
        if fn.startswith("temp_")
    ]
    tempList.sort(key=lambda fn: int(fn.split("_")[1]))
    with open(filePath, "wb") as fp_final:
        for fn in tempList:
            with open(fn, "rb") as fp_temp:
                fp_final.write(fp_temp.read())
    for fn in tempList:
        os.remove(fn)
    print("下载完成!")
    print("下载用时:", time.time() - startTime)


if __name__ == "__main__":
    url1 = (
        "https://konachan.com/jpeg/b9d90ca73e547e69e9ed88f880345329/Konachan.com%20"
        + "-%20988%20breasts%20navel%20nipples%20open_shirt%20pajamas%20panties%20"
        + "panty_pull%20pubic_hair%20pussy%20taka_tony%20tan_lines%20uncensored%20underwear.jpg"
    )
    url2 = (
        "https://konachan.com/image/2983dd62b91dd22ad84f43303d60479f/Konachan.com%20"
        + "-%2065943%20amatsumi_sora_ni%20blush%20bra%20breasts%20clochette%20"
        + "kiyosumi_serika%20nipples%20panties%20pussy%20red_hair%20scan%20"
        + "shintaro%20thighhighs%20uncensored%20underwear%20undressing.png"
    )
    url3 = (
        "https://konachan.com/image/6ba3476dfec0b17395575994e3f7782d/"
        + "Konachan.com%20-%20251631%20anus%20ass%20ball%20breasts%20"
        + "clouds%20d.va%20flowers%20glasses%20group%20hat%20mecha%20"
        + "navel%20nipples%20nude%20petals%20ponytail%20pussy%20sky%20"
        + "sombra%20tattoo%20tracer%20water%20wink.png"
    )
    url4 = (
        "https://konachan.com/image/7b6da174a72d3b803febe4f13ac3f37c/"
        + "Konachan.com%20-%20231629%205_nenme_no_houkago%20animal%20"
        + "barefoot%20blush%20bunny%20headphones%20kantoku%20kurumi_%28"
        + "kantoku%29%20original%20pink_eyes%20pink_hair%20short_hair%20"
        + "skirt%20twintails.png"
    )
    threadCnt = 10
    mainPath = "D:\\konachan\\test"
    fileName = "231629_10.png"
    main(url4, threadCnt, mainPath, fileName)
