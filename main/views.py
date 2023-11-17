from django.shortcuts import render
from django.http import JsonResponse
from .forms import EC2InstanceForm
import subprocess
import os

def ec2_form(request):
    form = EC2InstanceForm()
    return render(request, 'ec2_form.html', {'form': form})

def deploy_ec2(request):
    if request.method == 'POST':
        form = EC2InstanceForm(request.POST)

        if form.is_valid():
            instance_type = form.cleaned_data['instanceType']
            ami = form.cleaned_data['ami']
            region = form.cleaned_data['region']
            access_key = form.cleaned_data['accessKey']
            secret_key = form.cleaned_data['secretKey']

            # Generate Terraform script
            terraform_script = f'''
            provider "aws" {{
                region = "{region}"
                access_key = "{access_key}"
                secret_key = "{secret_key}"
            }}

            resource "aws_instance" "example" {{
                ami           = "{ami}"
                instance_type = "{instance_type}"
            }}
            '''

            # Save Terraform script to a file (e.g., temp.tf)
            with open('temp.tf', 'w') as file:
                file.write(terraform_script)

            # Execute Terraform script
            try:
                subprocess.run(['terraform', 'init'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                subprocess.run(['terraform', 'apply', '-auto-approve'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                message = 'EC2 instance deployed successfully!'
            except subprocess.CalledProcessError as e:
                message = f'Error: {e.stderr.decode()}'

            # Clean up: remove the temporary Terraform script
            os.remove('temp.tf')

            return JsonResponse({'message': message})

        else:
            return JsonResponse({'message': 'Form validation failed'})

    return JsonResponse({'message': 'Invalid request method'})
