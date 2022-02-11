from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.UserList.as_view(), name="list_users"),
    path('<int:pk>', views.UserDetail.as_view(), name="view_user"),
    path('update/<int:id>', views.UserUpdate.as_view(), name="update_user"),
    path('delete/<int:id>', views.UserDelete.as_view(), name="delete_user"),
    path('profile/', views.current_user, name="current_user"),
]
