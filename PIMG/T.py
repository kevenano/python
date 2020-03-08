# 批量提取pimg文件夹中的tlg文件
import os
from tqdm import tqdm


# 字符串长度规范化
def modiStr(mes, length):
    mesLen = len(mes)
    if mesLen < length:
        return mes+' '*(length-mesLen)
    elif mesLen > length:
        return mes[0:length-2]+'..'
    else:
        return mes


# 遍历目录树，获取文件列表
def getFileList(mainDir, suffix):
    fileList = []
    for folderName, _, filenames in os.walk(mainDir):
        for file in filenames:
            if file.endswith(suffix):
                fileList.append(os.path.join(folderName, file))
    return fileList


# 批量处理
def extraTLG(fileList, outputDir, minSize=500000):
    flag = b'\x54\x4c\x47\x35\x2e\x30\x00\x72'
    pbar = tqdm(fileList, ncols=150)
    for file in pbar:
        fileName = os.path.basename(file)
        # 显示进度条
        pbar.set_description("Processing %s" % modiStr(fileName, 15))
        # 处理
        f = open(file, 'rb')
        content = f.read()
        f.close()
        sp = content.split(sep=flag)
        del sp[0]
        for i in range(len(sp)):
            if len(sp[i]) < minSize:
                continue
            outFile = open(os.path.join(
                outputDir, fileName.replace('.pimg', '_'+str(i)+'.tlg')), 'wb')
            outFile.write(flag)
            outFile.write(sp[i])
            outFile.close()


if __name__ == '__main__':
    mainDir = '/home/kevenano/Pictures/喫茶ステラと死神の蝶/t'
    outputDir = '/home/kevenano/Pictures/喫茶ステラと死神の蝶/output'
    fileList = getFileList(mainDir, 'pimg')
    extraTLG(fileList, outputDir, minSize=1000000)
    print('Done!')
