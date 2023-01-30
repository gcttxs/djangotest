import asyncio
import json
import sys

import client

# sys.path.insert(0, "..")
from opcuaTest import models
import time
import logging
from asyncua import Client, Node, ua,Server
from opcuaTest import Database
# from opcua import ua, Client
#---------------------------
#读区 写区  订阅
#缓存区存读写命令 是否要返回参数

#订阅 主动发布，mqtt协议

#并发 测试并发量 执行时间 函数执行时间
#server发送数据量
#-------------------------
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')
#尝试回调函数
class SubHandler(object):
    def data_change(self,handle,node,val,attr):
        print('new data change event',handle,node,val,attr)
class uaClient(object):
    def __init__(self):
        self.tag=False
        self.client=None
        self.node_list=[]
        self.node_id_list=[]
        self.node_name_list=[]
        self.node_value_list=[]
        self.url=""
    async def myConnect(self,u):
        self.url = u
        # url = 'opc.tcp://commsvr.com:51234/UA/CAS_UA_Server'
        async with Client(url=self.url) as self.client:
            await self.client.connect()

            mydata=Database.Database()
            mydata.update_connect(self.url,'true')
            mydata.Log(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))),'connect',self.url,'true')
            mydata.close()


            #下面的东西可以不用
            root = self.client.nodes.root
            nodes = [{'id': 1, 'node': root}]
            self.node_list.append(root)
            layer = 1
            while nodes.__len__():
                # nodes = 1
                # await self.client.export_xml('ua-export.xml','C:/Users/Admin/Desktop/DjangoTest/opcuaTest/')
                cur_node = nodes[0]
                del nodes[0]
                list = str(await cur_node['node'].read_node_class()).split('.')
                if list[1] == 'Variable':
                    self.node_list.append(cur_node['node'])
                    name=await cur_node['node'].read_display_name()
                    # print(f'name:------------------------------------------{name}')
                    value=await  cur_node['node'].read_value()
                    # print(f'value:========================================={value}')
                    self.node_name_list.append(str(name.Text))
                    self.node_id_list.append(str(cur_node['node'].nodeid))
                    self.node_value_list.append(await cur_node['node'].read_value())
                # print(f'value_list if {self.node_value_list}')

                if not await cur_node['node'].get_children()==None:
                    list = await cur_node['node'].get_children()

                    for i in list:
                        nodes.insert(0, {'id': cur_node['id'] + 1, 'node': i})
            # print(self.node_name_list)
            self.tag=True
        # print(f'value_list if {self.node_value_list}')
        # print(f'len {len(self.node_value_list)}')
        return self.node_id_list,self.node_name_list,self.node_value_list,self.url
    async def myRead(self,u,nodeid):
        self.url=u
        res=[]
        # models.connect_temp.objects.create(url=self.url,nodeid=nodeid,timestamps=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))))
        async with Client(url=self.url) as self.client:
            mydata = Database.Database()
            mydata.read_log(self.url,nodeid,str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))))
            mynodeid=nodeid.split('/')
            for i in range(len(mynodeid)):
                temp=self.client.get_node(mynodeid[i])          #得到nodeid
                res.append(await temp.read_value())             #res列表里加入值
                #数据库操作,log表，时间，read，url，nodeid，value
                mydata.Log(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))), 'read', self.url,
                   str(mynodeid[i])+' '+str(await temp.read_value()))
                nodeid = str(mynodeid[i])
                timestamps=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
                value=str(await temp.read_value())
                operation="read"
                print(f'url is {self.url},nodeid is {nodeid},opration is read,time is {timestamps},value is {value}')
                # mydata.server_log(self.url)
                # mydata.server_log(self.url,nodeid,operation,timestamps,value)
            stres=""
            for i in res:
                print(i)
                stres+=str(i)
            return stres,self.url,nodeid,timestamps
    #不适用
    # async def myWrite(self,u,nodeid,value):#nodeid和value是含多个元素的字符串形式列表，测试多个节点的写入
    #     self.url=u
    #     print(nodeid,value)
    #     async with Client(url=self.url) as self.client:
    #         mydata = Database.Database()
    #         mydata.write_log(self.url,nodeid,value,str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))))
    #         mynodeid=nodeid.split('/')
    #         myvalue=value.split('/')
    #         for i in range(len(myvalue)):
    #             temp=self.client.get_node(mynodeid[i])
    #             print(f"temp是{temp}")
    #             temp = ua.DataValue(myvalue[i])
    #             await temp.write_value((myvalue[i]))
    #             # dv1 = ua.DataValue(myvalue[i])
    #             # temp.set_value(dv1)
    #             # print(temp.get_value())
    #             mydata.Log(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))), 'write', self.url,
    #                str(mynodeid[i])+' '+str(myvalue[i]))



    # async def mySub(self,u,nodeid):
    #     self.url = u
    #     res = []
    #     async with Client(url=self.url) as self.client:
    #         mynode=self.client.get_node(nodeid)
    #         handler=SubHandler()
    #         sub=self.client.create_subscription(500,handler)
    #         sub.subscribe_data_change(mynode)
    #         print(sub.subscribe_data_change(mynode))
    #         time.sleep(500)


async def get_displayname():
    async with Client(url='opc.tcp://192.168.0.1:4840') as client:
        await client.connect()
        root = client.nodes.root
        nodes = [{'id': 1, 'node': root}]
        node_list.append(root)





