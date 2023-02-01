from django.urls import path
from . import views

urlpatterns = [
    path('read/', views.readTest, name='read'),
]