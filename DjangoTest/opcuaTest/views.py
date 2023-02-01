from django.http import HttpResponse
from django.shortcuts import render,redirect
from opcuaTest.opcuaDemo import uaClient
import asyncio
import json
from opcuaTest import models
from opcuaTest.direct import cost_time
from opcuaTest.writedemo import WriteClient,SubClient,Create_server,Create_server2
from opcuaTest.models import server_log,opcuaserver

from fastapi import FastAPI
app = FastAPI()


def modifyTest(request):
    return render(request,'modifyTest.html')

@app.post("/connect")
@cost_time
def connectTest(request):
    data=request.POST
    client=uaClient()
    res=asyncio.run(client.myConnect(data['url']))
    nodeid=res[0]
    nodename=res[1]
    nodevalue=str(res[2])
    nodevalue=nodevalue.encode('utf-8')
    url=res[3]
    print(res[1][500])
    res={
        'id':nodeid,
        'name':nodename,
    }
    if (models.opcuaserver.objects.filter(url=url)):
        models.opcuaserver.objects.filter(url=url).delete()
    for i in range(len(nodeid)):
        models.opcuaserver.objects.create(url=url,node_id=nodeid[i],node_name=nodename[i],node_value=nodevalue[i])
    return HttpResponse(json.dumps(res))



@cost_time
def writeTest(request):

    data=request.POST
    client=WriteClient()
    res=client.Write(data['url'],data['nodeid'],data['value'])
    # print(f'res is {res}')
    #判断res[2]：节点id和名称都相同

    value=server_log.objects.filter(nodeid=str(res[2]))
    # print(value)
    for i in value:
        i=str(i)
    #获得value
    i=i.split(',')[1]

    node_id=server_log.objects.filter(value=i)
    for n in node_id:
        print(n)
        n = str(n)
        print(f'n 是 {n}')
        break
    name = n.split(".")[0]
    node_id= n.split(",")[0]
    # print(f'nodeid 是 {name}  ,{i}')
    server_log.objects.filter(value = i).update(operation='write',value=res[0],timestamps=str(res[3]))
    # print(f"opc.tcp://192.168.0.1:4840,{str(node_id)},{res[0]}")
    url='opc.tcp://192.168.0.1:4840'

    client.Write(url,str(node_id),res[0])
    return HttpResponse(json.dumps({'code':200}))



@cost_time
def readTest(request):
    data = request.POST
    client=uaClient()
    res=asyncio.run(client.myRead(data['url'],data['nodeid']))
    print(f'res is {res}')
    #判断nodeid相同的情况下删除之前的数值再创建
    if (len(models.server_log.objects.filter(nodeid=str(res[2])))) >0:
        models.server_log.objects.filter(nodeid=str(res[2])).delete()
    models.server_log.objects.create(value=res[0],url=str(res[1]), nodeid=str(res[2]), operation='read', timestamps=str(res[3]))
    return HttpResponse(json.dumps({'value':res[0],'code':200}))

def threadTest(request):#接口函数里开启进程
    data = request.POST
    client=SubClient()
    res=client.Sub(data['url'],data['nodeid'])
    return HttpResponse(json.dumps({'value':res,'code':200}))

def createserver(request):

    msg=models.server_log.objects.filter(url='opc.tcp://192.168.0.1:4840')
    name_list=[]
    nodeid_list=[]
    value_list=[]
    for i in range(len(msg)):
        newnodeid=str(msg[i])
        res=newnodeid.split(",")
        nodeid=(res[0].split('.')[0])
        nodeid_list.append(str(nodeid))
        name=eval(res[0].split(".")[1])
        name_list.append(str(name))
        value=res[1]
        value_list.append(str(value))
    Create_server(nodeid_list,value_list,name_list)
    message = "The service is successfully started"
    print(message)
    return redirect("/modifyTest/")


def createserver2(request):
    Create_server2()
    message = "The service is successfully started"
    print(message)
    return redirect("/modifyTest/")
