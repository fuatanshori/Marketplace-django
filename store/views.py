import re
from unicodedata import category
from django.shortcuts import render,get_object_or_404,HttpResponse
from carts.views import _cart_id
from carts.models import CartItem
from .models import Products
from category.models import Category
from .utils import pagination_products
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
import xlwt
from datetime import datetime
import zoneinfo
from django.utils import timezone
import time

def store(request,category_input=None):
    categories = None
    products = None
    if category_input is not None:
        
        categories = get_object_or_404(Category,slug=category_input)
        products = Products.objects.filter(category=categories,is_available=True)
        product_count = products.count()
        
    else:
        products = Products.objects.all().filter(is_available=True).order_by('id')
        product_count = products.count()
 
    custom_range,products, = pagination_products(request,products,True)

    context={
        'title':'Store | Page',
        'products':products,
        'product_count':product_count,
        'custom_range':custom_range,
        
    }
    return render(request,'store/store.html',context)


def product_detail(request,category_input,product_input):

    try:
        single_product=Products.objects.get(category__slug=category_input,slug=product_input)
        in_cart =CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
    except Exception as e:
        raise e
    
    context={
        'title':(f'{single_product} | page'),
        'single_product':single_product,
        'in_cart':in_cart,
        
    }
    return render(request,'store/product_detail.html',context)

def search(request):
    if 'keyword' in request.GET:
        keyword =request.GET['keyword']

    products=Products.objects.filter(
        Q(category__category_name__iexact=keyword)|
        Q(product_name__icontains=keyword)
    ).order_by('category')
    product_count = products.count()
    custom_range,products, = pagination_products(request,products,True)
    
    context={
        'title':'Search | Page',
        'products':products,
        'keyword':keyword,
        'product_count':product_count,
        'custom_range':custom_range,
    }
    return render(request,'store/search.html',context)

@staff_member_required(login_url='accounts:login')
def alldata(request):
    products = Products.objects.all() 
    context={
        'title':'DATA | PAGE',
        'products':products,
    }
    return render(request,'store/data/data.html',context)


@staff_member_required(login_url='accounts:login')
def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    
    response['Content-Disposition'] = 'attachment; filename="data.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Product_Data')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['product name', 'price','quantity','available', 'category','modified date', 'created date']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = Products.objects.all().values_list('product_name', 'price','stock','is_available', "category__category_name",'modified_date', 'created_date')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if isinstance(row[col_num], datetime):
                date_time = row[col_num].strftime('%Y-%m-%d %H:%M:%S')
                ws.write(row_num, col_num, date_time, font_style)
            else:
                ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response