autoDown.py:
python autoDown.py
自动查询更新数据库
自动执行：
    1. 数据库中查询 MAX(id) 
    2. 构造URL，下载id > MAX(id) 的json
    3. 新数据写入数据库
    4. 导出新数据的file_url到urls.txt
    5. 写日志log.txt
默认参数：
limit: 50 thread: 5 tableName: "main" order: id
注意：数据库需预先设置好！

downJson.py:
python downJson.py
可多线程批量下载json文件
依次执行：
    1. 交互获取参数
    2. 循环 给定线程 爬取json
    3. 写日志
注意： log中有失败页列表 使用相同参数及该列表可重新下载

insertData.py:
python insertData.py [mainFolder] [tableName]
批量将json文件写入数据库
依次执行：
    1. 获取参数
    2. 链接数据库
    3. 建表
    4. 遍历 mainFolder 将全部json写入数据库
    5. 写日志

-------------------------NOTE-------------------------
typeDic 需要根据服务器端手动更新 否则写数据库操作均无法正常进行
包含未知key的json数据均会被判定为failed
log里面包含了重要信息 是排错的关键 也有承上启下的作用
数据库提前设置好 tablename 默认 main
