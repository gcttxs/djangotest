"""DjangoTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from django.urls import path
from opcuaTest.views import modifyTest,connectTest,writeTest,readTest,threadTest,createserver,createserver2
urlpatterns = [
    path('', include('write.urls')),
    path('', include('read.urls')),
    path('', include('subscribe.urls')),
    path('admin/', admin.site.urls),
    path('modifyTest/',modifyTest),
    path('connectTest/',connectTest),
    path('writeTest/',writeTest),
    path('readTest/',readTest),
    path('threadTest/',threadTest),
    path('createserver/',createserver),
    path('createserver2/',createserver2)

]

# myobj = objects.add_object(idx, "MyObject")
# name_list = [1, 2, 3]
# for i in name_list:
#     name = str(i)
#     print(i)
#     myvar = myobj.add_variable(idx, name, 6.7)
#     myvar.set_writable()  # 设置为可由客户端写入
