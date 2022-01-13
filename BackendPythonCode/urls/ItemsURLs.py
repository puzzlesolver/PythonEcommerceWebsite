from BackendCode.views import ItemsViews as views
from django.urls import path

urlpatterns = [
    path('<str:pk>/reviews/', views.createItemReview, name="create-review"),
    path('top/', views.getHighlyRatedItems, name='top-items'),
    path('<str:pk>/', views.getSingleItem, name="item"),
    path('', views.getItems, name="items"),
    path('create/', views.createItem, name="item-create"),
    path('upload/', views.uploadItemImage, name="image-upload"),
    path('update/<str:pk>/', views.updateItem, name="item-update"),
    path('delete/<str:pk>/', views.deleteItem, name="item-delete"),
]
