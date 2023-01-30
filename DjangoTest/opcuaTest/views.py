from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render,redirect
import opcuaTest.opcuaDemo
from opcuaTest.opcuaDemo import uaClient
import asyncio
import json
import time
from opcuaTest import models
from opcuaTest.direct import cost_time
import _thread
from opcuaTest.writedemo import WriteClient,SubClient,Create_server,Create_server2
from asyncua import Client, Node, ua
# Create your views here.
from opcuaTest.models import server_log,opcuaserver

def modifyTest(request):
    return render(request,'modifyTest.html')

@cost_time
def connectTest(request):
    data=request.POST
    client=uaClient()
    res=asyncio.run(client.myConnect(data['url']))

    # id=res['id']
    # name=res['name']
    # print(len(id))
    # print(len(name))
    nodeid=res[0]
    nodename=res[1]
    nodevalue=str(res[2])
    nodevalue=nodevalue.encode('utf-8')
    # print(f'res[0]:nodeid is {nodeid}')
    # print(f'res[1]:nodename is {nodename}')
    # print(f'res[2]:nodevalue is {nodevalue}')
    url=res[3]
    print(res[1][500])
    res={
        'id':nodeid,
        'name':nodename,
        # 'value':nodevalue
    }
    # for i in range(10):
    # 如果有相同的nodeid先删除
    if (models.opcuaserver.objects.filter(url=url)):
        models.opcuaserver.objects.filter(url=url).delete()
    for i in range(len(nodeid)):
        # print((len(models.opcuaserver.objects.filter(node_id=nodeid[i]))))
        models.opcuaserver.objects.create(url=url,node_id=nodeid[i],node_name=nodename[i],node_value=nodevalue[i])
    return HttpResponse(json.dumps(res))

@cost_time
def writeTest(request):

    data=request.POST
    # client=uaClient()
    client=WriteClient()
    # asyncio.run(WriteClient.Write(data['url'],data['nodeid'],data['value']))
    res=client.Write(data['url'],data['nodeid'],data['value'])
    print(f'res is {res}')
    #判断res[2]：节点id和名称都相同

    value=server_log.objects.filter(nodeid=str(res[2]))
    print(value)
    for i in value:
        i=str(i)
    #获得value
    i=i.split(',')[1]

    node_id=server_log.objects.filter(value=i)
    for n in node_id:
        print(n)
        # ns=3;s="data block_1"."num2",233.3300018310547
        n = str(n)
        print(f'n 是 {n}')
        break
    # # 获得displayname           # name = eval(n.split(".")[1].split(",")[0])
    name = n.split(".")[0]
    node_id= n.split(",")[0]
    print(f'nodeid 是 {name}  ,{i}')
    server_log.objects.filter(value = i).update(operation='write',value=res[0],timestamps=str(res[3]))
    print(f"opc.tcp://192.168.0.1:4840,{str(node_id)},{res[0]}")
    url='opc.tcp://192.168.0.1:4840'

    client.Write(url,str(node_id),res[0])
    # if (len(models.server_log.objects.filter(nodeid=str(res[2])))) >0:
        #删除之前数据
        # models.server_log.objects.filter(nodeid=str(res[2])).delete()
    #创建一条写记录
    # models.server_log.objects.create(value=res[0], url=str(res[1]), nodeid=str(res[2]), operation='write',
    #                                  timestamps=str(res[3]))

    # if str(res[1])!='opc.tcp:':
    #     if models.server_log.objects.filter(value=data['value']):
    #         print(f'value is {value}')
    # if models.server_log.objects.filter(nodeid=)
    return HttpResponse(json.dumps({'code':200}))

@cost_time
def readTest(request):
    data = request.POST
    client=uaClient()
    res=asyncio.run(client.myRead(data['url'],data['nodeid']))
    print(f'res is {res}')
    # for i in range(len(res)):
    #     print(f"res {i} is {res[i]}")
    #判断nodeid相同的情况下删除之前的数值再创建
    if (len(models.server_log.objects.filter(nodeid=str(res[2])))) >0:
        models.server_log.objects.filter(nodeid=str(res[2])).delete()
    models.server_log.objects.create(value=res[0],url=str(res[1]), nodeid=str(res[2]), operation='read', timestamps=str(res[3]))

    # models.connect_temp.objects.create(url=data['url'],nodeid=data['nodeid'],timestamps=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))))
    return HttpResponse(json.dumps({'value':res[0],'code':200}))

def threadTest(request):#接口函数里开启进程
    data = request.POST
    client=SubClient()
    res=client.Sub(data['url'],data['nodeid'])
    return HttpResponse(json.dumps({'value':res,'code':200}))
    # try:
    #     client=uaClient()
    #     _thread.start_new_thread(opcuaTest.opcuaDemo.test())
    #     return HttpResponse("new thread start")
    # except:
    #     print("error")
    #     return HttpResponse("error")


def createserver(request):

    msg=models.server_log.objects.filter(url='opc.tcp://192.168.0.1:4840')
    name_list=[]
    nodeid_list=[]
    value_list=[]
    for i in range(len(msg)):
        newnodeid=str(msg[i])
        # print(newnodeid)                #ns=3;s="data block_1"."num1",333.3299865722656
        res=newnodeid.split(",")
        # print(res[0])

        # 获得nodeid
        nodeid=(res[0].split('.')[0])
        # print(nodeid)
        nodeid_list.append(str(nodeid))
        # 获得名称
        name=eval(res[0].split(".")[1])
        # print(name)
        name_list.append(str(name))
        # 获得数据
        value=res[1]
        # print(value)
        value_list.append(str(value))

    # print(nodeid_list)
    # print(value_list)
    # print(name_list)
    Create_server(nodeid_list,value_list,name_list)
    message = "The service is successfully started"
    # if request.method == "GET":
    print(message)
    # return render(request,'modifyTest.html',{"message":message})
    return redirect("/modifyTest/")


def createserver2(request):
    Create_server2()
    message = "The service is successfully started"
    # if request.method == "GET":
    print(message)
    # return render(request,'modifyTest.html',{"message":message})
    return redirect("/modifyTest/")
