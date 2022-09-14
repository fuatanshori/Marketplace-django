
from django.shortcuts import render
from store.models import Products
from .utils import paginatorproducts
def home(request):
    products = Products.objects.all().filter(is_available=True).order_by('category')
    custom_range,products,page = paginatorproducts(request,products,True)
    context={
        'title':'Home | Page',
        'products_home':products,
        'custom_range_home':custom_range,
        'page_count':page
    }
    return render(request,'home.html',context)