from django.urls import path

from . import views

app_name = 'household'

urlpatterns = [
    path('<int:pk>/', views.HouseholdViewHousehold.as_view(),name='household'),
    path('register', views.HouseholdCreateHousehold.as_view(), name='household_create'),

]