from django.shortcuts import render
from django.http import HttpResponse
import boto3
from .forms import AWSDeployForm, AzureDeployForm, GCPDeployForm
from azure.identity import DefaultAzureCredential, ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
from google.cloud import compute_v1
from google.auth.transport.requests import Request
import json
from google.oauth2 import service_account


#main page, user will choose which cloud provider they wish to proceed with
def choose_cloud(request):
    return render(request, 'choose_cloud.html')

#AWS
def aws_deploy(request):
    if request.method == 'POST':
        form = AWSDeployForm(request.POST)
        if form.is_valid():
            # Get all parameters from the form
            access_key = form.cleaned_data['aws_access_key']
            secret_key = form.cleaned_data['aws_secret_key']
            region = form.cleaned_data['aws_region']
            vm_name = form.cleaned_data['vm_name']
            instance_type = form.cleaned_data['instance_type']
            ami = form.cleaned_data['ami']
            availability_zone = form.cleaned_data['availability_zone']
            user_data = form.cleaned_data['user_data']
            monitoring_enabled = form.cleaned_data['monitoring_enabled']
            
            # VPC and Subnet parameters
            vpc_cidr_block = form.cleaned_data['vpc_cidr_block']
            subnet_cidr_block = form.cleaned_data['subnet_cidr_block']

            # Security Group parameters
            security_group_name = form.cleaned_data['security_group_name']
            security_group_description = form.cleaned_data['security_group_description']

            try:
                # Create VPC
                vpc_response = boto3.client('ec2', region_name=region, aws_access_key_id=access_key, aws_secret_access_key=secret_key).create_vpc(
                    CidrBlock=vpc_cidr_block,
                )
                vpc_id = vpc_response['Vpc']['VpcId']

                # Create Subnet
                subnet_response = boto3.client('ec2', region_name=region, aws_access_key_id=access_key, aws_secret_access_key=secret_key).create_subnet(
                    CidrBlock=subnet_cidr_block,
                    VpcId=vpc_id,
                )
                subnet_id = subnet_response['Subnet']['SubnetId']

                # Create Security Group
                security_group_response = boto3.client('ec2', region_name=region, aws_access_key_id=access_key, aws_secret_access_key=secret_key).create_security_group(
                    GroupName=security_group_name,
                    Description=security_group_description,
                    VpcId=vpc_id,
                )
                security_group_id = security_group_response['GroupId']

                # Create EC2 instance using Boto3
                ec2 = boto3.client('ec2', region_name=region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)

                response = ec2.run_instances(
                    ImageId=ami,
                    MinCount=1,
                    MaxCount=1,
                    InstanceType=instance_type,
                    SubnetId=subnet_id,
                    SecurityGroupIds=[security_group_id],
                    UserData=user_data,
                    Monitoring={'Enabled': monitoring_enabled},
                    Placement={'AvailabilityZone': availability_zone},
                    TagSpecifications=[
                        {
                            'ResourceType': 'instance',
                            'Tags': [
                                {'Key': 'Name', 'Value': vm_name},
                            ]
                        }
                    ]
                )

                instance_id = response['Instances'][0]['InstanceId']

                # Allocate and associate a public IP address
                public_ip_response = ec2.allocate_address(Domain='vpc')
                public_ip = public_ip_response['PublicIp']
                association_response = ec2.associate_address(InstanceId=instance_id, AllocationId=public_ip_response['AllocationId'])

                return HttpResponse(f"EC2 instance created with ID: {instance_id} in VPC: {vpc_id}, Subnet: {subnet_id}, Public IP: {public_ip}, Security Group: {security_group_id}")

            except Exception as e:
                # Handle exceptions appropriately
                return HttpResponse(f"Error: {str(e)}")

    else:
        form = AWSDeployForm()

    return render(request, 'aws_deploy.html', {'form': form})


#Azure
def azure_deploy(request):
    print_output = ""  # Variable to capture print statements

    if request.method == 'POST':
        form = AzureDeployForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data

            client_id = form_data['client_id']
            tenant_id = form_data['tenant_id']
            client_secret = form_data['client_secret']

            credential = ClientSecretCredential(tenant_id, client_id, client_secret)

            print_output += "Azure credential acquired.\n"

            # Obtain the management object for resources using the credentials from the user input
            resource_client = ResourceManagementClient(credential, form_data['subscription_id'])

            # Azure SDK operations for resource group provisioning
            print_output += "Provisioning resource group...\n"
            rg_result = resource_client.resource_groups.create_or_update(form_data['resource_group_name'],
                {
                    "location": form_data['location']
                }
            )
            print_output += f"Provisioned resource group {rg_result.name} in the {rg_result.location} region\n"

            # Azure SDK operations for virtual network provisioning
            network_client = NetworkManagementClient(credential, form_data['subscription_id'])

            print_output += "Provisioning virtual network...\n"
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
            print_output += f"Provisioned virtual network {vnet_result.name} with address prefixes {vnet_result.address_space.address_prefixes}\n"

            # Azure SDK operations for subnet provisioning
            print_output += "Provisioning subnet...\n"
            poller = network_client.subnets.begin_create_or_update(form_data['resource_group_name'], 
                form_data['vnet_name'], form_data['subnet_name'],
                { "address_prefix": form_data['subnet_address_prefix'] }
            )
            subnet_result = poller.result()
            print_output += f"Provisioned virtual subnet {subnet_result.name} with address prefix {subnet_result.address_prefix}\n"

            # Azure SDK operations for public IP provisioning
            print_output += "Provisioning public IP address...\n"
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
            print_output += f"Provisioned public IP address {ip_address_result.name} with address {ip_address_result.ip_address}\n"

            # Azure SDK operations for network interface provisioning
            print_output += "Provisioning network interface client...\n"
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
            print_output += f"Provisioned network interface client {nic_result.name}\n"

            # Azure SDK operations for virtual machine provisioning
            compute_client = ComputeManagementClient(credential, form_data['subscription_id'])

            print_output += "Provisioning virtual machine...\n"
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

            print_output += f"Provisioned virtual machine {vm_result.name}\n"

            return render(request, 'azure_deploy.html', {'form': form, 'print_output': print_output})

    else:
        form = AzureDeployForm()

    return render(request, 'azure_deploy.html', {'form': form})

#GCP
def gcp_deploy(request):
    if request.method == 'POST':
        form = GCPDeployForm(request.POST)
        if form.is_valid():
            # Extract form data
            name = form.cleaned_data['name']
            machine_type = form.cleaned_data['machine_type']
            image_family = form.cleaned_data['image_family']
            image_project = form.cleaned_data['image_project']
            subnet = form.cleaned_data['subnet']
            region = form.cleaned_data['region']
            zone = form.cleaned_data['zone']
            gcp_credentials = form.cleaned_data['gcp_credentials']
            project_name = form.cleaned_data['project_name']

            # Load GCP credentials from JSON string
            credentials_dict = json.loads(gcp_credentials)
            credentials = service_account.Credentials.from_service_account_info(credentials_dict)

            # Create a Compute Engine client using the authenticated credentials
            compute_client = compute_v1.InstancesClient(credentials=credentials)

            # Construct the VM instance resource without tags and metadata
            instance_body = {
                "name": name,
                "machine_type": f"zones/{zone}/machineTypes/{machine_type}",
                "disks": [
                    {
                        "boot": True,
                        "auto_delete": True,
                        "initialize_params": {
                            "source_image": f"projects/{image_project}/global/images/family/{image_family}",
                        },
                    }
                ],
                "network_interfaces" : [
                    {
                    'subnetwork' : f'regions/{region}/subnetworks/{subnet}',
                    'access_configs' : [
                        {
                            'name': 'External NAT'
                        }
                    ]
                    }
                ]
            }

            # Deploy the VM
            operation = compute_client.insert(project = project_name, zone = zone, instance_resource = instance_body)
            operation.result  # Wait for the operation to complete
            return HttpResponse('Success')
        else:
            return HttpResponse('error')
    else:
        form = GCPDeployForm()

    return render(request, 'gcp_deploy.html', {'form': form})