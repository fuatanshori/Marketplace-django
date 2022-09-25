from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from store.models import Products, Variation
from .models import Cart,CartItem


from django.contrib.auth.decorators import login_required
# Create your views here.

# create sesson id for get cart_id
def _cart_id(request):
    cart = request.session.session_key
    # ? if cart is None 
    if not cart:
        # ?create session id
        cart =request.session.create()
    # todo return cart
    return cart


def add_cart(request,product_id):
    current_user =request.user
    # take product models by id
    product = Products.objects.get(id=product_id)

    # if user is authenticated
    if current_user.is_authenticated:
        # create product variation in list
        product_variation = []

        # if request.method is post
        if request.method == 'POST':
            # ? important!!! takeing all component in request.post
            for item in request.POST:
                # key is partition in request.post
                # key contains about = category value and variations category
                key = item
                # value berisi tentang partisi request.post yaitu color dan size
                value = request.POST[key]
                # coba
                try:
                    # mengambil Variation dengan
                    # mengambil produk by = id_produk,
                    # variation_category = key berisi tentang size dan color, 
                    # variation_value berisi= sesuat yang di inputkan kedalam post yaitu size dan color
                    variation = Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                    # tambahkan variation kedalam list product variation line 23
                    product_variation.append(variation)
                except:
                    pass

    
        # variabel  dibawah dengan value = models CartItem dengan mem filter-
        # product = id dari model Product
        # variabel dengan nilai = pencarian CartItem dengan filter product = id, cart dengan sesion 
        # exists function adalah bolean apakah list didalam CartItem ada
        is_cart_item_exists = CartItem.objects.filter(product=product,user=current_user).exists()
        if is_cart_item_exists:
            # mengambil nilai product dan cart
            # product = id 
            # cart = sesion     
            cart_item = CartItem.objects.filter(product=product,user=current_user)
            ex_var_list =[]
            id = []
            for item in cart_item:
                existing_variation = item.variation.all()
                ex_var_list.append(list(existing_variation))
                stock = item.product.stock
                print(stock)
                id.append(item.id)


            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                item_id_range = id[index]
                item_range = CartItem.objects.get(product=product,id=item_id_range)
                range =item_range.quantity
                if range>=stock:
                    # incraese the cart quantty
                    item_range.quantity +=0
                    item_range.save()
                else:
                    item_range.quantity +=1
                    item_range.save()
            else:
                item = CartItem.objects.create(
                    product = product,
                    quantity = 1,
                    user=current_user,
                )
                # create a new cart
                if len(product_variation)>0:
                    item.variation.clear()
                    item.variation.add(*product_variation)
                item.save()
                # cart_item di simpan
        else:
            # cart item dibikin
            cart_item = CartItem.objects.create(
                # memasukan product 
                product = product,
                quantity = 1,
                user=current_user,
            )
            if len(product_variation)>0:
                cart_item.variation.clear()
                for  item in product_variation:
                    cart_item.variation.add(item)
            # cart item disimpan
            cart_item.save()
            print('\n \n')
        return redirect('carts:cart')

        
    # if user is not authenticated
    else:
        # create product variation in list
        product_variation = []
        # if request.method is post
        if request.method == 'POST':
            # takeing all component in rquest.post
            for item in request.POST:
                # key is partition in request.post
                key = item
                # value berisi tentang partisi request.post yaitu color dan size
                value = request.POST[key]
                # coba
                try:
                    # mengambil Variation dengan
                    # mengambil produk by = id_produk,
                    # variation_category = key berisi tentang size dan color, 
                    # variation_value berisi= sesuat yang di inputkan kedalam post yaitu size dan color
                    variation = Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                    # tambahkan variation kedalam list product variation line 23
                    product_variation.append(variation)
                except:
                    pass
        
        # coba
        try:
            #mengambil Cart by cart_id berisi tentang sesion
            cart = Cart.objects.get(cart_id=_cart_id(request))
            print('\n \n')
            print('session id telah ada : '+_cart_id(request))
        # sesion pada cart_id tidak ada
        except Cart.DoesNotExist:
            # bikin cart model dan isi cart_id dengan seson id pada fungsi _cart_id
            cart = Cart.objects.create(
                # cart id diisi oleh sessi id 
                cart_id = _cart_id(request)
            )
            print('session id dibikin : ' + _cart_id(request))
        # lalu simpan 
        cart.save()
        

        # variabel  dibawah dengan value = models CartItem dengan mem filter-
        # product = id dari model Product
        # variabel dengan nilai = pencarian CartItem dengan filter product = id, cart dengan sesion 
        # exists function adalah bolean apakah list didalam CartItem ada
        is_cart_item_exists = CartItem.objects.filter(product=product,cart=cart).exists()
        if is_cart_item_exists:
            # mengambil nilai product dan cart
            # product = id 
            # cart = sesion     
            cart_item = CartItem.objects.filter(product=product,cart=cart)
            print('ini adalah cart_item : ' + str(cart_item))
            # exising variation -> database
            # currentb variation ->product variations
            # item_id -> database

            # variable xisting dengan nilaai list
            ex_var_list =[]
            # variable id dengan nilai list
            id = []

            for item in cart_item:
                existing_variation = item.variation.all()
                ex_var_list.append(list(existing_variation))
                stock = item.product.stock
                print(stock)
                id.append(item.id)


            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                item_id_range = id[index]
                item_range = CartItem.objects.get(product=product,id=item_id_range)
                range =item_range.quantity
                if range>=stock:
                    # incraese the cart quantity
                    item_range.quantity +=0
                    item_range.save()
                else:

                    item_range.quantity +=1
                    item_range.save()
            else:
                item = CartItem.objects.create(
                    product = product,
                    quantity = 1,
                    cart = cart
                )
                # create a new cart
                if len(product_variation)>0:
                    item.variation.clear()
                    item.variation.add(*product_variation)
                item.save()
                # cart_item di simpan
        else:
            # cart item dibikin
            cart_item = CartItem.objects.create(
                # memasukan product 
                product = product,
                quantity = 1,
                cart=cart,
            )
            if len(product_variation)>0:
                cart_item.variation.clear()
                for  item in product_variation:
                    cart_item.variation.add(item)
            # cart item disimpan
            cart_item.save()
            print('\n \n')
        return redirect('carts:cart')


def remove_cart(request,product_id,cart_item_id):
    current_user = request.user
    product = get_object_or_404(Products,id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(
                user = current_user,
                product=product,
                id=cart_item_id,
            )
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(
                cart = cart,
                product=product,
                id=cart_item_id,
            )
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
    except:
        pass
    return redirect('carts:cart')


def remove_cart_item(request,product_id,cart_item_id):
    product = get_object_or_404(Products,id=product_id)
    if request.user.is_authenticated:
        user = request.user
        cart_item = CartItem.objects.get(user=user,product=product,id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(cart=cart,product=product,id=cart_item_id)
    
    cart_item.delete()
    return redirect('carts:cart')

def cart(request,total=0,quantity=0,cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user,is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart,is_active=True)
        
        # memcah cart_items menjadi cart_item
        for cart_item in cart_items:
            # total = total(harga product * quantity)
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
    except:
        pass

    tax = round(total * 0.06)
    grand_total = total + tax
    context={
        'title':'Cart | Page',
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
    }
    return render(request,'carts/carts.html',context)


# ! important!!! if user not login point to login page
@login_required(login_url="accounts:login")
def checkout(request,total=0,quantity=0,cart_items=None):
    
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user,is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart,is_active=True)
        # memcah cart_items menjadi cart_item
        for cart_item in cart_items:
            # total = total(harga product * quantity)
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
    except:
        pass

    tax = round(total * 0.06)
    grand_total = total + tax
    context={
        'title':'Cart | Page',
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
    }
    return render(request,'carts/checkout.html',context)
