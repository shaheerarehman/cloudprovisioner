from django import forms

class EC2InstanceForm(forms.Form):
    instanceType = forms.CharField(label='Instance Type', max_length=100, required=True)
    ami = forms.CharField(label='AMI', max_length=100, required=True)
    region = forms.CharField(label='Region', max_length=100, required=True)
    accessKey = forms.CharField(label='Access Key', widget=forms.PasswordInput(), required=True)
    secretKey = forms.CharField(label='Secret Access Key', widget=forms.PasswordInput(), required=True)
