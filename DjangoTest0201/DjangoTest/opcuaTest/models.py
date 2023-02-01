from django.db import models




class server_log(models.Model):
    url = models.CharField(verbose_name="服务链接", max_length=255)
    nodeid=models.CharField(verbose_name="节点名称", max_length=255)
    operation = models.CharField(verbose_name="操作", max_length=255)
    timestamps = models.CharField(verbose_name="操作时间", max_length=255)
    value = models.CharField(verbose_name="数值", max_length=255)

    def __str__(self):
        # nodeid=str(self.nodeid)
        # nodeid+=" value="
        # value=str(self.value)
        # nodeid+=value
        msg=f'{self.nodeid},{self.value}'
        return msg

class opcuaserver(models.Model):
    url = models.CharField(verbose_name="服务链接", max_length=255)
    node_id = models.CharField(verbose_name="节点空间", max_length=255)
    node_name = models.CharField(verbose_name="节点名称", max_length=255)
    node_value = models.CharField(verbose_name="数值", max_length=255)
    #
    # def __str__(self):
    #     return self.node_value

# class opcua_change(models.Model):
#     url = models.CharField(verbose_name="服务链接", max_length=255)
#     nodeid=models.CharField(verbose_name="节点名称", max_length=255)
#     operation = models.CharField(verbose_name="操作", max_length=255)
#     timestamps = models.CharField(verbose_name="操作时间", max_length=255)
#     value = models.CharField(verbose_name="数值", max_length=255)
#     name = models.CharField(verbose_name="名称", max_length=255)