from django.shortcuts import render
from django.http import HttpResponse
import boto3
from .forms import EC2DeployForm, AzureDeployForm, GCPDeployForm

def main(request):
    return render(request, 'main.html')


def choose_cloud(request):
    return render(request, 'choose_cloud.html')

def aws_deploy(request):
    if request.method == 'POST':
        form = EC2InstanceForm(request.POST)

        if form.is_valid():
            access_key = form.cleaned_data['aws_access_key']
            secret_key = form.cleaned_data['aws_secret_key']
            region = form.cleaned_data['aws_region']
            instance_type = form.cleaned_data['instanceType']
            ami = form.cleaned_data['ami']

            # Create EC2 instance using Boto3
            ec2 = boto3.client('ec2', region_name=region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)

            response = ec2.run_instances(
                ImageId=ami,
                MinCount=1,
                MaxCount=1,
                InstanceType=instance_type,
            )

            instance_id = response['Instances'][0]['InstanceId']
            return HttpResponse(f"EC2 instance created with ID: {instance_id}")
    else:
        form = EC2DeployForm()

    return render(request, 'aws_deploy.html', {'form': form})



def azure_deploy(request):
    return render(request, 'templates/azure_deploy.html', {'form': form})

def gcp_deploy(request):
    return render(request, 'templates/gcp_deploy.html', {'form': form})

