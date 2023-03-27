from django.urls import path

from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.TodoViewTodos.as_view(), name='todo'),
]
