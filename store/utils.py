from unicodedata import category
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from .models import Products



def pagination_products(request,products,results):
    page = request.GET.get('page')
    results = 6
    paginator = Paginator(products,results)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        page=1
        products = paginator.page(page)
    except EmptyPage:
        page= paginator.num_pages
        products = paginator.page(page)
    
    left_index =(int(page)-1)
    if left_index < 1:
        left_index = 1
    
    right_index = (int(page)+2)

    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_range =range(left_index,right_index)

    
    return custom_range,products
