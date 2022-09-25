import datetime
import json
from django.shortcuts import render,redirect,HttpResponse
from carts.models import Cart, CartItem
from .forms import OrderForm
from  .models import Order, OrderProduct, Payment
from django.contrib import messages


# Create your views here.
def place_order(request,total=0,quantity=0):
    current_user = request.user

    # if the cart account is less than equal to zero redirect to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <=0:
        return redirect('home')
    grand_total = 0
    tax =0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = round(total * 0.06)
    grand_total = total + tax


    if request.method == "POST":
        form = OrderForm(request.POST or None)
        if form.is_valid():
            # store all the billing information inside order table
            data = Order()
            data.user           = current_user
            data.first_name     = form.cleaned_data['first_name']
            data.last_name      = form.cleaned_data['last_name']
            data.phone          = form.cleaned_data['phone']
            data.email          = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country        = form.cleaned_data['country']
            data.province       = form.cleaned_data['province']
            data.city           = form.cleaned_data['city']
            data.postal_code    = form.cleaned_data['postal_code']
            data.order_note     = form.cleaned_data['order_note']
            data.order_total    = grand_total
            data.tax            = tax
            data.ip             = request.META.get('REMOTE_ADDR')
            data.save()

            # Generate order number 
            current_date = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
            order_number = current_date+str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user,is_ordered=False,order_number=order_number)
            context={
                'order':order,
                'cart_items':cart_items,
                'total':total,
                'tax':tax,
                'grand_total':grand_total,
                'title':'Payment | page',
            }
            return render(request,'orders/payments.html',context)
        else:
            messages.error(request,'Invalid Email')
            return redirect('carts:checkout')


def payments(request):
    body = json.loads(request.body)
    print(body)
    print(request.user)
    order = Order.objects.get(user=request.user,is_ordered=False,order_number=body['orderID'])
    print(order.order_number)
    # store transaction detail inside payments model
    payment = Payment.objects.create(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
        
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    # move the cart items to order product table
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

    # reduce the quantity of the sold product

    # clear cart
    #  send order rechived email to customer

    # send order number and trancsaction id back to send data method  via jsonrespons
    
    return render(request,'orders/payments.html')