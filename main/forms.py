# cloud_app/forms.py
from django import forms

class AWSDeployForm(forms.Form):
    #AWS Credentials
    aws_access_key = forms.CharField(label='AWS Access Key', max_length=100, required=True, help_text='Your AWS access key ID')
    aws_secret_key = forms.CharField(label='AWS Secret Key', max_length=100, required=True, help_text='Your AWS secret access key')
    
    #AWS Region and Instance Details
    vm_name = forms.CharField(max_length=100, help_text="Enter a name for your VM")
    aws_region = forms.CharField(label='AWS Region', max_length=100, required=True, help_text='The AWS region to deploy the instance')
    availability_zone = forms.CharField(label='Availability Zone', max_length=100, required=True, help_text='The desired availability zone for the instance')
    instance_type = forms.CharField(label='Instance Type', max_length=100, required=True, help_text='The type of EC2 instance to launch')
    ami = forms.CharField(label='AMI ID', max_length=100, required=True, help_text='The ID of the Amazon Machine Image (AMI) to launch')
    
    #User Data and Optional Settings
    user_data = forms.CharField(label='User Data', widget=forms.Textarea, required=False, help_text='Optional user data to configure the instance')
    monitoring_enabled = forms.BooleanField(label='Monitoring Enabled', required=False, help_text='Enable detailed monitoring for the instance')
    
    #VPC and Optional settings
    vpc_cidr_block = forms.CharField(label='VPC CIDR Block', max_length=100, required=True, help_text='The CIDR block for the Virtual Private Cloud (VPC)')
    subnet_cidr_block = forms.CharField(label='Subnet CIDR Block', max_length=100, required=True, help_text='The CIDR block for the subnet')

    # Security Group Details
    security_group_name = forms.CharField(label='Security Group Name', max_length=100, required=True, help_text='The name of the security group for the instance')
    security_group_description = forms.CharField(label='Security Group Description', widget=forms.Textarea, required=True, help_text='A description for the security group')

class AzureDeployForm(forms.Form):
    # Azure AD Authentication
    client_id = forms.CharField(max_length=100, help_text='Azure AD Application Client ID')
    client_secret = forms.CharField(max_length=100, help_text='Azure AD Application Client Secret')
    tenant_id = forms.CharField(max_length=100, help_text='Azure AD Tenant ID')

    # Azure Subscription Information
    subscription_id = forms.CharField(max_length=100, help_text='Azure Subscription ID')

    # Resource Group Details
    resource_group_name = forms.CharField(max_length=100, help_text='Name for the Azure Resource Group')
    location = forms.CharField(max_length=100, help_text='Azure region where resources will be deployed')

    # Virtual Network Details
    vnet_name = forms.CharField(max_length=100, help_text='Name for the Azure Virtual Network')
    vnet_address_prefix = forms.CharField(max_length=100, help_text='Address prefix for the Virtual Network')

    # Subnet Details
    subnet_name = forms.CharField(max_length=100, help_text='Name for the Azure Subnet')
    subnet_address_prefix = forms.CharField(max_length=100, help_text='Address prefix for the Subnet')

    # Public IP Address Details
    ip_name = forms.CharField(max_length=100, help_text='Name for the Azure Public IP Address')
    ip_sku = forms.CharField(max_length=100, help_text='SKU for the Public IP Address')
    ip_allocation_method = forms.CharField(max_length=100, help_text='Allocation method for the Public IP Address (e.g., Static)')
    ip_address_version = forms.CharField(max_length=100, help_text='IP Address version (e.g., IPV4)')

    # IP Configuration Details
    ip_config_name = forms.CharField(max_length=100, help_text='Name for the Azure IP Configuration')

    # Network Interface Details
    nic_name = forms.CharField(max_length=100, help_text='Name for the Azure Network Interface')

    # Virtual Machine Details
    vm_name = forms.CharField(max_length=100, help_text='Name for the Azure Virtual Machine')
    image_publisher = forms.CharField(max_length=100, help_text='Publisher for the VM image (e.g., Canonical)')
    image_offer = forms.CharField(max_length=100, help_text='Offer for the VM image (e.g., UbuntuServer)')
    image_sku = forms.CharField(max_length=100, help_text='SKU for the VM image (e.g., 18.04-LTS)')
    image_version = forms.CharField(max_length=100, help_text='Version for the VM image (e.g., latest)')
    vm_size = forms.CharField(max_length=100, help_text='Size for the Virtual Machine (e.g., Standard_DS2_v2)')

    # Admin Details
    admin_username = forms.CharField(max_length=100, help_text='Admin username for the Virtual Machine')
    admin_password = forms.CharField(max_length=100, widget=forms.PasswordInput, help_text='Admin password for the Virtual Machine')

class GCPDeployForm(forms.Form):
    name = forms.CharField(max_length=255, help_text="Enter a unique name for your VM instance.")
    machine_type = forms.CharField(max_length=255, help_text="Specify the type of machine to use for the VM.")
    image_family = forms.CharField(max_length=255, help_text="Specify the operating system image family for the VM.")
    image_project = forms.CharField(max_length=255, help_text="Specify the project that contains the image family.")
    network = forms.CharField(max_length=255, help_text="Specify the network for the VM.")
    subnet = forms.CharField(max_length=255, help_text="Specify the subnet for the VM.")
    region = forms.CharField(max_length=255, help_text="Specify the region for the VM.")
    zone = forms.CharField(max_length=255, help_text="Specify the zone for the VM.")
    gcp_credentials = forms.CharField(widget=forms.Textarea, help_text="Paste the JSON-formatted GCP service account credentials.")
    startup_script = forms.CharField(widget=forms.Textarea, required=False)
    tags = forms.CharField(widget=forms.Textarea, required=False)
    project_name = forms.CharField(max_length=255, help_text="Specify the project name")
   
    

