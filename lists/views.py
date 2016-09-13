from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse
from django.template.loader import render_to_string
from lists.models import Item


# Create your views here.

def home_page(request):
    # item = request.POST.get('item')
    # return render(request, 'home.html')

    if request.method == 'POST':
        new_item_text = request.POST['item_text']
        Item.objects.create(text=new_item_text)
        return redirect('/')
    # else:
    #     new_item_text = ''

    #     return HttpResponse(request.POST.get['item_text'])
    # item = Item()
    # item.text = request.POST.get('item_text','')
    # item.save()

    # return render(request,'home.html',{'new_item_text':request.POST.get('item_text','')})
    #重构
    # return render(request,'home.html',{'new_item_text':new_item_text})
    items = Item.objects.all()
    return render(request, 'home.html',{'items':items})