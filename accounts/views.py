# rendering to template
from django.shortcuts import render,redirect,HttpResponse
# database pada model
from accounts.models import Account
# forms
from .forms import RegistrationForm,FormLogin,ForgotPassword,ResetPassword
# authenticate
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout

# verification email
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# authenticate decorator
from django.contrib.auth.decorators import login_required

from carts.models import Cart,CartItem
from carts.views import _cart_id
import requests


#  Create your views here.
# * for registering User.
# ! Important!!! data user has been saved on database, -
# ? but user has not been activate for activating user check program code line 50
def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                phone_number = phone_number,
                email=email,
                username=username,
                password=password,
            )
            user.save()

            # user activation
            current_site = get_current_site(request)
            mail_subject = 'please activate your account'
            message = render_to_string("accounts/verification/account_verification_email.html",{
                'user':user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form = RegistrationForm()
        
    context={
        'title':'Register | Page',
        'forms':form,
    }
    return render(request,'accounts/register.html',context)

# login user
def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    forms = FormLogin(request.POST or None)
    if request.method=='POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = Account.objects.get(email=email)
            if user is not None:
                user = authenticate(request,email=email,password=password)
                if user is not None:
                    try:
                        cart = Cart.objects.get(cart_id=_cart_id(request))
                        is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                        if is_cart_item_exists:
                            cart_item = CartItem.objects.filter(cart=cart)
                            
                            # geting the product variation by cart id
                            product_variation = []
                            for item in cart_item:
                                variation = item.variation.all()
                                product_variation.append(list(variation))
                            # get the cart items from the user access his product variations
                            cart_item = CartItem.objects.filter(user=user)
                            ex_var_list =[]
                            id = []
                            for item in cart_item:
                                existing_variation = item.variation.all()
                                ex_var_list.append(list(existing_variation))
                                id.append(item.id)

                            for pr in product_variation:
                                if pr in ex_var_list:
                                    index = ex_var_list.index(pr)
                                    item_id = id[index]
                                    item = CartItem.objects.get(id=item_id)
                                    item.quantity += 1
                                    item.user = user
                                    item.save()
                                else:
                                    cart_item = CartItem.objects.filter(cart=cart)
                                    for item in cart_item:
                                        item.user = user
                                        item.save()
                    except:
                        pass
                    auth_login(request,user)
                    messages.success(request,'login success')
                    url = request.META.get("HTTP_REFERER")
                    try:
                        query = requests.utils.urlparse(url).query
                        params = dict(
                            x.split('=') for x in query.split('&')
                        )
                        if 'next' in params:
                            nextPage = params['next']
                            return redirect(nextPage)
                    except:
                       return redirect('accounts:dashboard')
                else:
                    messages.error(request,'password is incorrect')
        except:
            messages.error(request,'email does not exist')
    
    
    context={
        'title':'Login | Page',
        'forms':forms
    }
    return render(request,'accounts/login.html',context)


def logout(request):
    auth_logout(request)
    return redirect("accounts:login")


# for authenticate token if true user.is_active = True
def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active =True
        user.save()
        messages.success(request,'congratulations your account is activated')
        return redirect('accounts:login')

    else:
        messages.error(request,'invalid token link')
        return redirect("accounts:register")


# if user not login this website back to User Login
@login_required(login_url="accounts:login")
def dashboard(request):
    return render(request,'accounts/dashboard.html')


# user forgot the password 
def forgotPassword(request):
    forms = ForgotPassword(request.POST or None)
    if request.method == "POST":
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # sending verification code
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string("accounts/verification/reset_password_email.html",{
                'user':user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            return redirect('/accounts/forgotPassword/?command=verification&email='+email)
        else:
            messages.error(request,'email does not exist!')
    context={
        'forms':forms,
        'title':'Forgot Password | Page'
    }
    return render(request,'accounts/forgotPassword.html',context)


# authenticate the token for reset password 
def resetpassword_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.success(request,'please reset your password')
        return redirect("accounts:resetPassword")

    else:
        messages.error(request,'This Token has been expired')
        return redirect("accounts:login")

# reset password
def resetPassword(request):
    forms = ResetPassword(request.POST or None)
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get("uid")
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'password reset successful')
            return redirect("accounts:login")
        else:
            messages.error(request,"password does not match")
    context={
        'forms':forms,
        'title':'Reset Password | Page'
    }
    return render(request,'accounts/resetPassword.html',context)