from django.shortcuts import render
from django.http import HttpResponse

def main(request):
    return render(request, 'main.html')

def main2(request):
    return render(request, 'navbar.html')