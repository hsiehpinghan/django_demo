from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.index, name='index'),
    path('get_threads/', views.get_threads, name='get_threads'),
    path('add_thread/', views.add_thread, name='add_thread'),
    path('add_message/', views.add_message, name='add_message'),
]
