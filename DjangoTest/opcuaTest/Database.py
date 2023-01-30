import pymysql
from opcuaTest import models
class Database(object):
    def __init__(self):
        self.db=pymysql.connect(host='localhost',database='opcua',user='root',password='123456',charset='utf8')
        self.cursor = self.db.cursor()

    def update_connect(self,url,status):
        #sqlword="insert into connect_temp values(%s,%d)"
        sqlword="update connect_temp set status = %s where url= %s "
        data=[status,url]
        data=tuple(data)
        try:
          self.cursor.execute(sqlword,data)
          self.db.commit()

        except Exception as e:
            self.db.rollback()
            print(e)
            print('失败')

    def close(self):
        self.db.close()

    def Log(self,timestamps,operation,url,content):
        sqlword="insert into log values(%s,%s,%s,%s)"
        value = content.split(' ')
        print(f"value is {value}")
        data=[timestamps,operation,url,content]
        data=tuple(data)
        try:
          self.cursor.execute(sqlword,data)
          self.db.commit()

        except Exception as e:
            self.db.rollback()
            print(e)
            print('失败')
    def write_log(self,url,nodeid,value,timestamps):
        data=[url,nodeid,value,timestamps]
        data=tuple(data)
        try:#即时存总命令
            self.cursor.execute("insert into write_temp values(%s,%s,%s,%s)", data)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print(e)
            print('失败')

    def read_log(self,url,nodeid,timestamps):
        data=[url,nodeid,timestamps]
        data=tuple(data)
        try:#即时存总命令
            self.cursor.execute("insert into read_temp values(%s,%s,%s)", data)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print(e)
            print('失败')

    # def server_log(request, url,nodeid,operation,timestamps,value):
    #     print(url,nodeid,operation,timestamps,value)
    #     models.server_log.objects.create(url=url,nodeid=nodeid,operation=operation,timestamps=timestamps,value=value)

    # def server_log(request, url):
    #     print(url)
    #     server=models.server_log.objects.create(url='url',nodeid="132",operation='operation',timestamps='timestamps',value='value')
    #     server.save()

