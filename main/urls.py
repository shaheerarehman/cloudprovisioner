from django.urls import path
from . import views

urlpatterns = [
     path('main/', views.main, name="main"),
     path('main2/', views.main2, name="main2"),
     path('deploy/', views.deploy_ec2_instance, name='deploy_ec2'),
]