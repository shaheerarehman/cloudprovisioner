from django.urls import path
from . import views

urlpatterns = [
     path('main/', views.main, name="main"),
     path('main2/', views.main2, name="main2"),
]