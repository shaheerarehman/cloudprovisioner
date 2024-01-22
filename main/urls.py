from django.urls import path
from . import views

urlpatterns = [
    path('', views.choose_cloud, name='choose_cloud'),
    path('aws/', views.aws_deploy, name='aws_deploy'),
    path('azure/', views.azure_deploy, name='azure_deploy'),
    path('gcp/', views.gcp_deploy, name='gcp_deploy'),
]


