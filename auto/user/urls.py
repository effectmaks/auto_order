from django.urls import path
from . import views

urlpatterns = [
    path('user/list/', views.user_list, name='user_list'),
    path('user/<int:pk>/', views.user_detail, name='user_detail'),
    path('register/', views.register_view, name='register'),
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
]




