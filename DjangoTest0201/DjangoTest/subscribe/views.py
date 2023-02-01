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

import asyncio
from opcua import ua

from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from opcuaTest.opcuaDemo import uaClient
import asyncio
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import JsonResponse
from opcuaTest.writedemo import SubClient

from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@api_view(['GET'])
@permission_classes((AllowAny,))
def subscribe(request):
    url = request.GET.get('url')
    nodeid = request.GET.get('nodeid')
    # 这里可以调用订阅的代码，代码内容根据实际情况编写
    client=SubClient()
    value=client.Sub(url,nodeid)

    return JsonResponse({'value': value, 'code': 200})


