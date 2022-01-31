from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('user/', views.UserList.as_view(), name="list_users"),
    path('user/<int:pk>', views.UserDetail.as_view(), name="view_user"),
    # path('update_user/<int:pk>', views.update_user, name="update_user"),
    path('user/delete/<int:pk>', views.UserDelete.as_view(), name="delete_user"),
]
