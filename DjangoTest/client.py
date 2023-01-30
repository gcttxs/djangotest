import asyncio
import sys
# sys.path.insert(0, "..")
import logging
from asyncua import Client, Node, ua

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')


async def main():
    # url = 'opc.tcp://localhost:4841/freeopcua/server/'
    url = 'opc.tcp://127.0.0.1:4842/anqu_opcua_server'
    # url = 'opc.tcp://commsvr.com:51234/UA/CAS_UA_Server'
    async with Client(url=url) as client:
        # Client has a few methods to get proxy to UA nodes that should always be in address space such as Root or Objects
        # Node objects have methods to read and write node attributes as well as browse or populate address space
        mytags = await client.nodes.root.get_children()
        print(mytags)
        # 获取根目录下所有node节点
        _logger.info('孩子 of root children are: %r', mytags)
        # 获取根目录节点
        _logger.info('孩子 of root are: %r', client.get_root_node())
        mytag1 = await mytags[0].get_children()
        print(mytag1)
        mytag2 = await mytag1[1].get_children()
        print(mytag2)
        # 获取指定node下所有node节点,没有返回"[]"
        _logger.info('孩子 of root are: %r', mytag2[0])

        # uri = 'http://examples.freeopcua.github.io'
        # idx = await client.get_namespace_index(uri)
        # # get a specific node knowing its node id
        # var2 = await client.get_node("i=84").get_children()
        # # var2tmp = var2.get_children()
        # # _logger.info('Children of root are: %r', var2tmp)
        # # var = client.get_node("ns=3;i=2002")
        # var = await client.nodes.root.get_child(["0:Objects", f"{idx}:MyObject", f"{idx}:MyVariable"])
        # # 读取一个node的变量值
        # print("My variable", var, await mytag2[0].read_value())
        # mytag3 = await mytag2[0].get_children()
        # print(var2)
        # # 写入一个node的变量值
        # await mytag2[0].write_value(3.9)
        # # print(var)
        # # await var.read_data_value() # get value of node as a DataValue object
        # # await var.read_value() # get value of node as a python builtin
        # # await var.write_value(ua.Variant([23], ua.VariantType.Int64)) #set node value using explicit data type
        # # await var.write_value(3.9) # set node value using implicit data type


if __name__ == '__main__':
    asyncio.run(main())
