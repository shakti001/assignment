from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse

from .models import *
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

User = get_user_model()
# Create your views here.
def signup(request):
    try:
        if request.method=="POST":
            username = request.POST.get('username')
            email = request.POST.get('email')
            mobile_number = request.POST.get('mobile_number')
            password = request.POST.get('password')
            repassword = request.POST.get('repassword')
            if username and email and mobile_number and password:
                if password == repassword:
                    user = User.objects.create(username=username,email=email,mobile_number=mobile_number,password=make_password(password))
                    messages.success(request, "Login Please !!")
                    return redirect('/login/')
                else:
                    messages.error(request, "Password does not same !!")
                    return redirect('/signup/')
            else:
                messages.error(request, "all filed required !!")
                return redirect('/signup/')
    except:
        messages.error(request, "Something went wrong !!")
        return redirect('/signup/')

    return render(request,"userpanel/auth/signup.html")

def login(request):
    try:
        if request.method == "POST":
            email = request.POST.get("email")
            password = request.POST.get("password")
            if User.objects.filter(email=email).exists():
                user = auth.authenticate(email=email, password=password)
                if user is None:
                    messages.error(request, "Invalid email & passsword")
                    return redirect('/login/')
                elif user.is_superuser == False:
                    auth.login(request, user)
                    return redirect("/")
                else:
                    messages.error(request, "Invalid email & passsword")
                    return redirect('/login/')
            else:
                messages.error(request, "Invalid email & passsword")
                return redirect('/login/')
    except:
        messages.error(request, "Something went wrong !!")
        return redirect('/login/')
    return render(request,"userpanel/auth/login.html")

@login_required(login_url="/login")
def logout(request):
    auth.logout(request)
    messages.success(request, "Logout SuccessFully !!!")
    return redirect("/")

def homePage(request):
    try:
        product = Product.objects.all()
    except:
        messages.error(request, "something went worng !!!")
        return redirect('/')
    return render(request, "userpanel/index.html",{'product':product,})

def productDetails(request,slug):
    try:
        product = Product.objects.get(slug=slug)
        tag_data = ProductTags.objects.all()
        tag_data.filter(product = product.id)
    except:
        messages.error(request, "something went worng !!!")
        return redirect('/product-details/'+str(slug))
    return render(request, "userpanel/product/shop-detail.html",{'product':product,'tag_data':tag_data})

def addToCart(request):
    try:
        if request.method=="POST":
            qty = request.POST.get('qty')
            product_id = request.POST.get('product_id')
            user_id = request.POST.get('user_id')
            product_price = request.POST.get('product_price')
            if qty and product_id and user_id:
                if CartProduct.objects.filter(product_id=product_id,user_id=user_id).exists():
                    return JsonResponse({'status':'error', 'message':'Product Allready in cart'})
                total = int(qty) * int(product_price)
                data = CartProduct.objects.create(qty=qty,product_id=product_id,user_id=user_id,total_amount=total)
                return JsonResponse({'status':'success', 'message':'Product added in to cart'})
            else:
                return JsonResponse({'status':'error', 'message':'Please login first !!'})
            
        else:
            return JsonResponse({'status':'error', 'message':'Please login first!!'})
    except:
        messages.error(request, "something went worng !!!")
        return redirect('/add-cart/')

def cart(request):
    cart = CartProduct.objects.filter(user_id = request.user.id)
    cartTotal = CartProduct.objects.filter(user_id = request.user.id).aggregate(Sum('total_amount'))
   
    return render(request, 'userpanel/cart.html',{'cart':cart,'cartTotal':cartTotal})

@login_required(login_url="/login")  
def removeCartItems(request,slug):
    cart = CartProduct.objects.get(slug=slug)
    cart.delete()
    messages.success(request, "item removed from cart !!")
    return redirect('/cart/')

    
