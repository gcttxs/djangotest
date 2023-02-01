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
from fastapi import FastAPI, Request, Response
import json


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view(['GET', 'POST'])
@permission_classes((AllowAny,))
def write(request):
    if request.method == 'GET':
        url = request.GET.get('url')
        nodeid = request.GET.get('nodeid')
        value = request.GET.get('value')

        # Write logic here
        client = WriteClient()
        res = client.Write(url, nodeid, value)

        value = server_log.objects.filter(nodeid=str(res[2]))
        for i in value:
            i = str(i)
        i = i.split(",")[1]

        node_id = server_log.objects.filter(value=i)
        for n in node_id:
            n = str(n)
            break
        name = n.split(".")[0]
        node_id = n.split(",")[0]

        server_log.objects.filter(value=i).update(
            operation="write", value=res[0], timestamps=str(res[3])
        )
        #修改djangoplc数据同时修改原始plc
        url = "opc.tcp://192.168.0.1:4840"
        client.Write(url, str(node_id), res[0])

        return HttpResponse(json.dumps({'code': 200}))
    elif request.method == 'POST':
        data = request.data
        url = data.get('url')
        nodeid = data.get('nodeid')
        value = data.get('value')

        # Write logic here
        client = WriteClient()
        res = client.Write(url, nodeid, value)

        value = server_log.objects.filter(nodeid=str(res[2]))
        for i in value:
            i = str(i)
        i = i.split(",")[1]

        node_id = server_log.objects.filter(value=i)
        for n in node_id:
            n = str(n)
            break
        name = n.split(".")[0]
        node_id = n.split(",")[0]

        server_log.objects.filter(value=i).update(
            operation="write", value=res[0], timestamps=str(res[3])
        )

        url = "opc.tcp://192.168.0.1:4840"
        client.Write(url, str(node_id), res[0])

        return HttpResponse(json.dumps({'code': 200}))
