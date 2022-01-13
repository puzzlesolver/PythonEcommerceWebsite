from BackendCode.views import CustomerViews as views
from django.urls import path

urlpatterns = [
    path('profile/', views.getProfile, name="users-profile"),
    path('profile/update/', views.updateProfile, name="user-profile-update"),
    path('', views.getUsers, name="users"),
    path('login/', views.MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('register/', views.userRegistration, name='register'),
    path('<str:pk>/', views.getID, name='user'),
    path('update/<str:pk>/', views.updateUser, name='user-update'),
    path('delete/<str:pk>/', views.deleteUser, name='user-delete'),
]
