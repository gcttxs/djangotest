# Generated by Django 3.2.16 on 2022-12-13 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opcuaTest', '0006_auto_20221211_2329'),
    ]

    operations = [
        migrations.CreateModel(
            name='opcua_server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=255, verbose_name='服务链接')),
                ('nodeid', models.CharField(max_length=255, verbose_name='节点空间')),
                ('nodename', models.CharField(max_length=255, verbose_name='节点名称')),
                ('nodevalue', models.CharField(max_length=255, verbose_name='数值')),
            ],
        ),
    ]
