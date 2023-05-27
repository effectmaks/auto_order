from django.urls import path
from . import views

urlpatterns = [
    path('', views.orders_list, name='orders_list'),
    path('<int:pk>/', views.order_detail, name='order_detail'),
    path('add/', views.add_order, name='order_add'),
    path('delete/<int:pk>', views.delete_order, name='order_delete'),


]

