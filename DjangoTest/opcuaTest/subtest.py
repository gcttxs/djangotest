import asyncio
import sys
# sys.path.insert(0, "..")
import time
import logging
#from asyncua import Client, Node, ua
from opcuaTest import Database
from opcua import Client
class SubHandler(object):
    def data_change(selfself,handle,node,val,attr):
        print('python',handle,node,type(val),attr)

client=Client('opc.tcp://127.0.0.1:4840/anqu_opcua_server')
client.connect()
my=client.get_node('ns=2;i=2')
valuetmp=my.get_value()
print(valuetmp)
handler=SubHandler()
sub=client.create_subscription(500,handler)
sub.subscribe_data_change(my)

time.sleep(100000)
client.disconnect()