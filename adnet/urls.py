from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from . import views

urlpatterns = [
    path('register/', views.CreateUser.as_view(), name = 'create_user'),
    path('login/', views.login, name = 'login'),
    path('<int:user_id>/advisor/', views.get_ad, name = 'get_ad'),
    path('<int:user_id>/advisor/<int:advisor_id>/', views.book, name = 'book'),
    path('<int:user_id>/advisor/booking/', views.get_book, name = 'get_book'),
    path('auth/', obtain_jwt_token, name = 'auth'),
    path('token-refresh/', refresh_jwt_token)
]
