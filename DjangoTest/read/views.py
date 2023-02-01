from django.http import JsonResponse
from opcuaTest.opcuaDemo import uaClient
import asyncio

from opcuaTest.models import server_log,opcuaserver
from fastapi import FastAPI
app = FastAPI()
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


@api_view(['GET', 'POST'])
@permission_classes((AllowAny,))
def readTest(request):
    data = request.GET
    client = uaClient()
    res = asyncio.run(client.myRead(data['url'], data['nodeid']))
    print(f'res is {res}')
    # 判断nodeid相同的情况下删除之前的数值再创建
    if len(server_log.objects.filter(nodeid=str(res[2]))) > 0:
        server_log.objects.filter(nodeid=str(res[2])).delete()
    server_log.objects.create(value=res[0], url=str(res[1]), nodeid=str(res[2]), operation='read', timestamps=str(res[3]))
    return JsonResponse({'url':str(res[1]),'nodeid':str(res[2]),'value': res[0], 'code': 200})