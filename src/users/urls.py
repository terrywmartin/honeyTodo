from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('', views.UsersViewUsers.as_view(), name='users'),
    path('<int:pk>/', views.UsersViewUser.as_view(), name='user_view'),
    path('edit/<int:pk>/', views.UsersEditUser.as_view(), name='user_edit'),
    path('delete/<int:pk>/', views.UsersDeleteUser.as_view(), name='user_delete'),
    path('create/', views.UsersCreateUser.as_view(), name='user_create'),
    path('invite/', views.UsersInviteUser.as_view(), name='user_invite'),
    path('reset-password/<int:pk>/', views.UsersResetPassword.as_view(), name='user_reset_password'),
    path('create-password/<uuid:uuid>/', views.UsersCreatePassword.as_view(), name='user_create_password'),
    #path('profile/<int:pk>/', views.ProfileViewProfile.as_view(), name='view_profile'), 
]
