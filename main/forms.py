# cloud_app/forms.py
from django import forms

class EC2DeployForm(forms.Form):
    # AWS Credentials
    aws_access_key = forms.CharField(max_length=100, help_text="AWS Access Key ID for authentication")
    aws_secret_key = forms.CharField(max_length=100, help_text="AWS Secret Access Key for authentication")
    
    # EC2 Instance Configuration
    aws_region = forms.CharField(max_length=50, help_text="AWS region where the EC2 instance will be launched")
    instance_type = forms.CharField(max_length=50, help_text="Type of EC2 instance (e.g., t2.micro, m5.large)")
    ami = forms.CharField(max_length=100, help_text="Amazon Machine Image ID for the EC2 instance")

class AzureDeployForm(forms.Form):
    # Azure Credentials
    azure_client_id = forms.CharField(max_length=100, help_text="Azure Client ID for authentication")
    azure_secret_key = forms.CharField(max_length=100, help_text="Azure Secret Key for authentication")
    azure_tenant_id = forms.CharField(max_length=100, help_text="Azure Tenant ID for authentication")
    azure_subscription_id = forms.CharField(max_length=100, help_text="Azure Subscription ID for authentication")

    # Azure VM Configuration
    azure_location = forms.CharField(max_length=50, help_text="Azure region where the VM will be launched")
    vm_size = forms.CharField(max_length=50, help_text="Size of the VM (e.g., Standard_B1s)")
    image_id = forms.CharField(max_length=100, help_text="Image ID for the VM")

class GCPDeployForm(forms.Form):
    # Google Cloud Credentials
    gcp_project_id = forms.CharField(max_length=100, help_text="Google Cloud Project ID for authentication")
    gcp_client_email = forms.EmailField(help_text="Google Cloud Client Email for authentication")
    gcp_private_key = forms.CharField(widget=forms.Textarea, help_text="Google Cloud Private Key for authentication")
    
    # GCP VM Configuration
    gcp_region = forms.CharField(max_length=50, help_text="Google Cloud region where the VM will be launched")
    machine_type = forms.CharField(max_length=50, help_text="Machine type for the VM (e.g., n1-standard-1)")
    image_project = forms.CharField(max_length=100, help_text="Project ID of the image")
    image_family = forms.CharField(max_length=100, help_text="Image family for the VM")
    image_name = forms.CharField(max_length=100, help_text="Image name for the VM")
