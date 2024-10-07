from django.urls import path
from . import views

app_name = 'workflow'

urlpatterns = [
    path('', views.index, name='index'),
    path('get_html/', views.get_html, name='get_html'),
]
