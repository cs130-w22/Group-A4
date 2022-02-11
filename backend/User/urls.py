from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    # admin CRUD
    path('', views.UserList.as_view(), name="list_users"),
    path('profile/<int:pk>/', views.UserDetail.as_view(), name="view_user"),
    path('update/<int:pk>/', views.UserUpdate.as_view(), name="update_user"),
    path('delete/<int:pk>/', views.UserDelete.as_view(), name="delete_user"),
    # regular user CRUD (only on current logged in user)
    path('profile/', views.CurrentUserDetail.as_view(), name="view_current_user"),
    path('profile/update/', views.CurrentUserUpdate.as_view(), name="update_current_user"),
]
