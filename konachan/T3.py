# 写数据库 json to mysql
import json
import pymysql

def creatTable(tableName):
    jsFile = open('like.json','r')
    data = json.load(jsFile)
    data = data[0]
    jsFile.close()

    dic1={}
    dic2={}

    # 数据类型转换 字典python --> mysql
    dic2['int'] = 'int'
    dic2['str'] = 'text'
    dic2['list'] = 'text'
    dic2['bool'] = 'char(10)'

    # 构造mysql建表命令
    for k,v in data.items():
        key = '`'+k+'`'
        dic1[key]=dic2[str(type(v)).replace("""<class '""",'').replace("""'>""",'')]
    
    db = pymysql.connect('localhost','root','qhm2012@@@','konachan')
    cursor = db.cursor()
    sql = """creat table if not exists `"""+tableName+'`'+'('
    for k,v in dic1.items():
        sql=sql+k+' '+v+','
    sql = sql+"""primary key(id))engine=innodb default charset=utf8mb4"""
    
    # 建表
    cursor.execute(sql)
    db.commit();
    db.close()


if __name__ == '__main__':
    creatTable('`mian`')