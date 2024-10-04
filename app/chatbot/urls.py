from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.index, name='index'),
    path('add_thread/', views.add_thread, name='add_thread'),
]
