def azure_deploy(request):
    if request.method == 'POST':
        form = AzureDeployForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data

            client_id = form_data['client_id']
            tenant_id = form_data['tenant_id']
            client_secret = form_data['client_secret']

            credential = ClientSecretCredential(tenant_id, client_id, client_secret)






            # Use DefaultAzureCredential for authentication
            #credential = DefaultAzureCredential(client_id=form_data['client_id'],
            #                                    client_secret=form_data['client_secret'],
            #                                    tenant_id=form_data['tenant_id'])

            # Obtain the management object for resources using the credentials from the user input
            resource_client = ResourceManagementClient(credential, form_data['subscription_id'])

            # Azure SDK operations for resource group provisioning
            rg_result = resource_client.resource_groups.create_or_update(form_data['resource_group_name'],
                {
                    "location": form_data['location']
                }
            )

            # Azure SDK operations for virtual network provisioning
            network_client = NetworkManagementClient(credential, form_data['subscription_id'])

            poller = network_client.virtual_networks.begin_create_or_update(form_data['resource_group_name'],
                form_data['vnet_name'],
                {
                    "location": form_data['location'],
                    "address_space": {
                        "address_prefixes": [form_data['vnet_address_prefix']]
                    }
                }
            )

            vnet_result = poller.result()

            poller = network_client.subnets.begin_create_or_update(form_data['resource_group_name'], 
                form_data['vnet_name'], form_data['subnet_name'],
                { "address_prefix": form_data['subnet_address_prefix'] }
            )

            subnet_result = poller.result()

            poller = network_client.public_ip_addresses.begin_create_or_update(form_data['resource_group_name'],
                form_data['ip_name'],
                {
                    "location": form_data['location'],
                    "sku": { "name": form_data['ip_sku'] },
                    "public_ip_allocation_method": form_data['ip_allocation_method'],
                    "public_ip_address_version" : form_data['ip_address_version']
                }
            )

            ip_address_result = poller.result()

            poller = network_client.network_interfaces.begin_create_or_update(form_data['resource_group_name'],
                form_data['nic_name'], 
                {
                    "location": form_data['location'],
                    "ip_configurations": [ {
                        "name": form_data['ip_config_name'],
                        "subnet": { "id": subnet_result.id },
                        "public_ip_address": {"id": ip_address_result.id }
                    }]
                }
            )

            nic_result = poller.result()

            # Azure SDK operations for virtual machine provisioning
            compute_client = ComputeManagementClient(credential, form_data['subscription_id'])

            poller = compute_client.virtual_machines.begin_create_or_update(form_data['resource_group_name'],
                form_data['vm_name'],
                {
                    "location": form_data['location'],
                    "storage_profile": {
                        "image_reference": {
                            "publisher": form_data['image_publisher'],
                            "offer": form_data['image_offer'],
                            "sku": form_data['image_sku'],
                            "version": form_data['image_version']
                        }
                    },
                    "hardware_profile": {
                        "vm_size": form_data['vm_size']
                    },
                    "os_profile": {
                        "computer_name": form_data['vm_name'],
                        "admin_username": form_data['admin_username'],
                        "admin_password": form_data['admin_password']
                    },
                    "network_profile": {
                        "network_interfaces": [{
                            "id": nic_result.id,
                        }]
                    }
                }
            )

            vm_result = poller.result()

            return HttpResponse('success')

    else:
        form = AzureDeployForm()

    return render(request, 'azure_deploy.html', {'form': form})




def aws_deploy(request):
    if request.method == 'POST':
        form = AWSDeployForm(request.POST)
        if form.is_valid():
            access_key = form.cleaned_data['aws_access_key']
            secret_key = form.cleaned_data['aws_secret_key']
            region = form.cleaned_data['aws_region']
            instance_type = form.cleaned_data['instance_type']
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
        form = AWSDeployForm()

    return render(request, 'aws_deploy.html', {'form': form})


{% extends 'base.html' %}
{% block content %}
  <h2>AWS Deployment Form</h2>
  <form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Deploy</button>
  </form>
{% endblock %}



class AWSDeployForm(forms.Form):
    #AWS Credentials
    aws_access_key = forms.CharField(label='AWS Access Key', max_length=100, required=True, help_text='Your AWS access key ID')
    aws_secret_key = forms.CharField(label='AWS Secret Key', max_length=100, required=True, help_text='Your AWS secret access key')
    
    #AWS Region and Instance Details
    aws_region = forms.CharField(label='AWS Region', max_length=100, required=True, help_text='The AWS region to deploy the instance')
    availability_zone = forms.CharField(label='Availability Zone', max_length=100, required=True, help_text='The desired availability zone for the instance')
    instance_type = forms.CharField(label='Instance Type', max_length=100, required=True, help_text='The type of EC2 instance to launch')
    ami = forms.CharField(label='AMI ID', max_length=100, required=True, help_text='The ID of the Amazon Machine Image (AMI) to launch')
    key_name = forms.CharField(label='Key Name', max_length=100, required=True, help_text='The name of the key pair to use for the instance')
    
    #User Data and Optional Settings
    user_data = forms.CharField(label='User Data', widget=forms.Textarea, required=False, help_text='Optional user data to configure the instance')
    monitoring_enabled = forms.BooleanField(label='Monitoring Enabled', required=False, help_text='Enable detailed monitoring for the instance')
    iam_instance_profile = forms.CharField(label='IAM Instance Profile', max_length=100, required=False, help_text='The name of the IAM instance profile')
    
    #VPC and Optional settings
    vpc_cidr_block = forms.CharField(label='VPC CIDR Block', max_length=100, required=True, help_text='The CIDR block for the Virtual Private Cloud (VPC)')
    subnet_cidr_block = forms.CharField(label='Subnet CIDR Block', max_length=100, required=True, help_text='The CIDR block for the subnet')

    # Security Group Details
    security_group_name = forms.CharField(label='Security Group Name', max_length=100, required=True, help_text='The name of the security group for the instance')
    security_group_description = forms.CharField(label='Security Group Description', widget=forms.Textarea, required=True, help_text='A description for the security group')