from django.urls import path
from . import views

urlpatterns = [
     path('deploy/', views.ec2_form, name='deploy_ec2'),
]