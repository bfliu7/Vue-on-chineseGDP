import time

import pymysql

#连接数据库
conn=pymysql.connect(
    host="127.0.0.1",
    port=3307,
    database="keshihua",
    user="root",
    password="123456"
)
#查询数据库
def readbase(sqll):
    #读数据库
    try:
        time.sleep(0.2)
        with conn.cursor() as cursor:
            #此处写sql语句
            sql=sqll #"select count(*) from gan"
            cursor.execute(sql)
            #此处加上开始处理数据格式
            datas=cursor.fetchall() #获得元组格式(('张三',),('李四',))
            #处理
            result=datas


            #处理，获得想要的格式
    except Exception as e:
        print(e)
        result=None
    finally:
        # conn.close()
        return result

