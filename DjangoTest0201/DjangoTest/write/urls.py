from django.urls import path
from . import views

urlpatterns = [
    path('write/', views.write, name='write'),
]
