from django.shortcuts import render
from django.http import HttpResponse 

# Create your views here.
def home(request):
    return render(request, 'home.html')
def main(request):
    return render(request, 'psiu/main.html')
def user_info(request):
    return render(request, 'psiu/user_info.html')