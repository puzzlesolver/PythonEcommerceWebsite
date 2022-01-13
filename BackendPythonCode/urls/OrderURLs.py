from BackendCode.views import OrderViews as views
from django.urls import path

urlpatterns = [
    path('<str:pk>/deliver/', views.updateOrderDelivery, name='order-delivered'),
    path('<str:pk>/', views.getOrderById, name='user-order'),
    path('<str:pk>/pay/', views.updateOrderPayment, name='pay'),
    path('', views.getOrders, name='orders'),
    path('add/', views.addItems, name='orders-add'),
    path('myorders/', views.getMyOrders, name='myorders'),
]
