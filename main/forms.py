from django import forms

class EC2DeployForm(forms.Form):
    aws_access_key = forms.CharField(label='AWS Access Key')
    aws_secret_key = forms.CharField(label='AWS Secret Key', widget=forms.PasswordInput)
    aws_region = forms.CharField(label='AWS Region')
    instance_type = forms.CharField(max_length=100)
    ami = forms.CharField(max_length=100)
    # Add more fields as required for instance creation
