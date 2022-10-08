from django.contrib import messages
from django.shortcuts import render,get_object_or_404,HttpResponse,redirect
from carts.views import _cart_id
from carts.models import CartItem
from .models import Products, ReviewRating
from category.models import Category
from .utils import pagination_products
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
import xlwt
from datetime import datetime
from .forms import ReviewForm
from orders.models import OrderProduct

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
        stock = single_product.stock
        in_cart =CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
    except Exception as e:
        raise e
    
    try:
        orderproduct=OrderProduct.objects.filter(user=request.user,product=single_product.id).exists()
    except OrderProduct.DoesNotExist:
        orderproduct = None
    
    reviews=ReviewRating.objects.filter(product=single_product.id,status=True)
    context={
        'title':(f'{single_product} | page'),
        'single_product':single_product,
        'in_cart':in_cart,
        'stock':stock,
        'orderproduct':orderproduct,
        'reviews':reviews
    }
    return render(request,'store/product_detail.html',context)

def search(request):
    if 'keyword' in request.GET:
        keyword =request.GET['keyword']
    products=Products.objects.filter(
       Q(is_available = True),
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

def submit_review(request,product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        try:
            reviews=ReviewRating.objects.get(user__id=request.user.id,product__id=product_id)
            form = ReviewForm(request.POST or None,instance=reviews)
            form.save()
            messages.success(request, 'Thank you for reviews has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request,'Thank you for reviews has been submited')
                return redirect(url)