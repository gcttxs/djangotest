from opcua import ua, Client,Server
from django.shortcuts import render,redirect
import time
from opcuaTest import models
import json
from opcuaTest.direct import cost_time
from opcuaTest import Database
from opcuaTest.opcuaDemo import uaClient
from django.http import HttpResponse
import asyncio
import xml

class WriteClient(object):
    def Write(self,u,nodeid,value):#nodeid和value是含多个元素的字符串形式列表，测试多个节点的写入
        # myvalue = value.split('/')
        value=str(value)
        print(type(value))
        print(f'u是{u}；nodeid是{nodeid}； 写入value是{value}')
        self.url=u
        client = Client(u)
        # 连接客户端
        client.connect()
        mydata = Database.Database()
        mydata.write_log(self.url, nodeid, value, str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))))
        try:
            value=int(value)
        except:
            value=float(value)
        # 读写一个bool值
        # 寻找节点上的变量
        var = client.get_node(nodeid)           #获得nodeid=nodeid
        # 通过get_value读值
        print(f'原本该节点数值为{var.get_value()}')                  #获取nodeid原本数据
        # 判断写入的数据类型进行操作
        if value =="False":
            print("布尔类型写入")
            dv1 = ua.DataValue(False)
            var.set_value(dv1)
        if value =="True":
            print("布尔类型写入")
            dv1 = ua.DataValue(True)
            var.set_value(dv1)
        if isinstance(value,float) ==True:
            print("浮点类型写入")
            var_float =float(value)
            # var = client.get_node(nodeid)
            print(var.get_value())
            dv = ua.DataValue(ua.Variant(var_float, ua.VariantType.Float))
            ##数据类型要这样写入,尽量不要出现Double和Float两种类型
            # dv = ua.DataValue(ua.Variant(var_float, ua.VariantType.Float))
            # 写入var
            var.set_value(dv)
            # print(var.get_value())
        if isinstance(value,int) ==True:
            print("整形写入")
            var_int = int(value)
            dv = ua.DataValue(ua.Variant(var_int, ua.VariantType.Int16))
            var.set_value(dv)
        else:
            print("数据类型识别失败")
        timestamps=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
        print(f'最后结果{var.get_value()}')
        return value,self.url,nodeid,timestamps
        # 读写一个int值
        # double_node = client.get_node('ns=3;s="数据块_1"."num5"')
        # print(double_node .get_value())
        # dv = ua.DataValue(ua.Variant(200.0, ua.VariantType.Double))
        # double_node .set_value(dv)
        # print(double_node .get_value())
        #能写入的函数
        # double_node = client.get_node('ns=3;s="数据块_1"."num5"')
        # print(double_node.get_value())
        # dv = ua.DataValue(ua.Variant(200.9, ua.VariantType.Double))
        # double_node.set_value(dv)
        # print(double_node.get_value())
class SubHandler(object):
    def data_change(self, handle, node, val, attr):
        print("Python: New data change event", handle, node, val, attr)
        print(val)

class SubClient(object):
    def Sub(self,u,nodeid):
        self.url = u
        res = []
        client = Client(u)
        client.connect()
        # # 获取object对象
        # objects = client.get_objects_node()
        # # 获取根对象
        # root = client.get_root_node()
        subvar = client.get_node(nodeid)
        # 获取变量当前值
        subvalue = subvar.get_value()
        print(f'当前数值{subvalue}')
        # 注册到服务器的变量订阅，变量逢变触发
        handler = SubHandler()
        sub = client.create_subscription(500, handler)      #时期，方法
        sub.subscribe_data_change(subvar)
        res.append(subvar.get_value())
        stres=""
        for i in res:
            print(i)
            stres += str(i)
        return stres

        time.sleep(100000)
        client.disconnect()


##通过纯python代码生成的server
def Create_server(nodeid_list,value_list,name_list):
    # print(nodeid_list)
    # print(value_list)
    # print(name_list)
    server = Server()
    server.set_endpoint("opc.tcp://127.0.0.1:4841/anqu_opcua_server")

    # 设置我们自己的命名空间，不是真正必要的，但应该作为规范
    uri = "http://automan.freeopcua.github.io"
    idx = server.register_namespace(uri)

    # plc 1500
    uri1 = 'urn:SIMATIC.S7-1500.OPC-UA.Application:PLC_1'
    uri2 = 'http://opcfoundation.org/UA/DI/'
    uri3 = 'http://www.siemens.com/simatic-s7-opcua'

    idx1 = server.register_namespace(uri1)  # 注册地址空间
    idx2 = server.register_namespace(uri2)
    idx3 = server.register_namespace(uri3)
    # idx决定ns
    # print(idx,idx1,idx2,idx3)
    # 获取对象节点，这是我们应该放置节点的位置
    objects = server.get_objects_node()
    # print(objects)
    # populating our address space
    #遍历获取数据表中的名和value
    #先写入数据表
    # row_object = models.read_temp.objects.all()
    # print(row_object)
    myobj = objects.add_object(idx, "DeviceSet")
    myobj2 = objects.add_object(idx2, "PLC_1")
    models.server_log.objects.filter()
    # name_list = [4, 5, 6]
    for i in range(len(name_list)):
        name = name_list[i]
        print(i)
        value=value_list[i]
        myvar = myobj.add_variable(idx, name, value)
        myvar.set_writable()  # 设置为可由客户端写入

    # starting!
    server.start()
    # try:
    #     count = 0
    #     while True:
    #         time.sleep(1)
    #         count += 0.1
    #         myvar.set_value(count)
    # finally:
    #     # 关闭连接，删除订阅等
    #     server.stop()



##通过配置xml文件生成的server
def Create_server2():
    server = Server()
    server.set_endpoint("opc.tcp://127.0.0.1:4842/anqu_opcua_server")  # 设定服务器URI
    # uri = 'http://examples.freeopcua.github.io'
    uri1 = 'urn:SIMATIC.S7-1500.OPC-UA.Application:PLC_1'
    uri2 = 'http://opcfoundation.org/UA/DI/'
    uri3 = 'http://www.siemens.com/simatic-s7-opcua'


    # idx = server.register_namespace(uri)  # 注册地址空间
    idx1 = server.register_namespace(uri1)  # 注册地址空间
    idx2 = server.register_namespace(uri2)
    idx3 = server.register_namespace(uri3)

    server.import_xml("C:/Users/Admin/Desktop/DjangoTest/opcuaTest/server.xml")  # 导入自定义的节点类型

    my_sensor_type = server.get_root_node().get_child([
        "0:Types", "0:ObjectTypes", "0:BaseObjectType", "0:TemperatureSensorType"]).nodeid
    my_sensor = server.nodes.objects.add_object(idx2, "PLC_1", my_sensor_type)
    my_sensor = server.nodes.objects.add_object(idx3, "DeviceSet", my_sensor_type)
    server.start()

##通过配置xml文件生成的server
# def Create_server2():
#     server = Server()
#     server.set_endpoint("opc.tcp://127.0.0.1:4842/anqu_opcua_server")  # 设定服务器URI
#     uri = 'http://examples.freeopcua.github.io'
#     idx = server.register_namespace(uri)  # 注册地址空间
#
#     server.import_xml("C:/Users/Admin/Desktop/DjangoTest/opcuaTest/server.xml")  # 导入自定义的节点类型
#
#     my_sensor_type = server.get_root_node().get_child([
#         "0:Types", "0:ObjectTypes", "0:BaseObjectType", "0:TemperatureSensorType"]).nodeid
#     my_sensor = server.nodes.objects.add_object(idx, "PLC_1", my_sensor_type)
#     my_sensor = server.nodes.objects.add_object(idx, "DeviceSet", my_sensor_type)
#
#
#     server.start()


def closeserver():
    server = Server()
    server.set_endpoint("opc.tcp://127.0.0.1:4841/anqu_opcua_server")
    server.stop()












