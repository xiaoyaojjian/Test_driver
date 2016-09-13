from django.shortcuts import render,redirect
from django.http import HttpRequest
from django.template.loader import render_to_string


# Create your views here.

def home_page(request):
    item = request.POST.get('item')
    return render(request, 'home.html')