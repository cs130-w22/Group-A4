from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('user/', views.UserList.as_view(), name="list_users"),
    path('user/<int:pk>', views.UserDetail.as_view(), name="view_user"),
    path('user/update/<int:pk>', views.UserUpdate.as_view(), name="update_user"),
    path('user/delete/<int:pk>', views.UserDelete.as_view(), name="delete_user"),
]
