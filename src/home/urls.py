from django.urls import path

from . import views

app_name = 'home'

urlpatterns = [
    path('', views.HomeIndex.as_view(),name='index'),
    
]