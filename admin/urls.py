from django.urls import path

from . import views

urlpatterns = [
    path('advisor/', views.create_advisor, name = 'create_advisor'),
]
